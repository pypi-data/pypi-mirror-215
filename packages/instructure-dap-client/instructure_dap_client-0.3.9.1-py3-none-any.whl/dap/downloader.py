import logging
from dataclasses import dataclass
from datetime import datetime
from typing import AsyncContextManager, Awaitable, Callable

from .api import DAPSession, DownloadError
from .concurrency import wait_n
from .dap_types import (
    Format,
    GetTableDataResult,
    IncrementalQuery,
    Object,
    SnapshotQuery,
    VersionedSchema,
)
from .integration.database_errors import SchemaVersionMismatchError
from .integration.processor import (
    AbstractInitProcessor,
    AbstractSyncProcessor,
    ContextAwareObject,
)
from .payload import get_json_lines_from_gzip_stream

logger = logging.getLogger("dap")

CONCURRENCY: int = 4

DatabaseLock = Callable[[], AsyncContextManager]
SnapshotDownloader = Callable[[DatabaseLock, AbstractInitProcessor], Awaitable[None]]


@dataclass(frozen=True)
class SnapshotClient:
    table_data: GetTableDataResult
    table_schema: VersionedSchema
    download: SnapshotDownloader


class SnapshotClientFactory:
    _sessions: DAPSession
    _namespace: str
    _table: str

    def __init__(self, session: DAPSession, namespace: str, table: str) -> None:
        self._session = session
        self._namespace = namespace
        self._table = table

    async def get_client(self) -> SnapshotClient:
        query = SnapshotQuery(format=Format.JSONL, filter=None)
        table_data = await self._session.get_table_data(
            self._namespace, self._table, query
        )

        table_schema = await self._session.get_table_schema(
            self._namespace, self._table
        )
        if table_schema.version != table_data.schema_version:
            raise SchemaVersionMismatchError(
                table_schema.version, table_data.schema_version
            )

        object_count = len(table_data.objects)
        job_id = table_data.job_id

        async def download(
            db_lock: DatabaseLock, processor: AbstractInitProcessor
        ) -> None:
            async def logged_download_and_save(obj: Object, object_index: int) -> None:
                context_aware_object = ContextAwareObject(
                    id=obj.id,
                    index=object_index,
                    job_id=job_id,
                    total_count=object_count,
                )
                await self._download(db_lock, context_aware_object, processor=processor)

            await wait_n(
                [
                    logged_download_and_save(obj, obj_index)
                    for obj_index, obj in enumerate(table_data.objects)
                ],
                concurrency=CONCURRENCY,
            )

            await processor.close()

        return SnapshotClient(
            table_schema=table_schema, table_data=table_data, download=download
        )

    async def _download(
        self,
        db_lock: DatabaseLock,
        obj: ContextAwareObject,
        processor: AbstractInitProcessor,
    ) -> None:
        resource_array = await self._session.get_resources([Object(id=obj.id)])
        if len(resource_array) != 1:
            raise DownloadError("unable to get resource URLs for objects")

        logger.info(f"Downloading {obj}")

        resource = resource_array[0]
        async with self._session.stream_resource(resource) as stream:
            records = get_json_lines_from_gzip_stream(stream)
            async with db_lock():
                await processor.process(obj, records)


IncrementalDownloader = Callable[[DatabaseLock, AbstractSyncProcessor], Awaitable[None]]


@dataclass(frozen=True)
class IncrementalClient:
    table_data: GetTableDataResult
    table_schema: VersionedSchema
    download: IncrementalDownloader


class IncrementalClientFactory:
    _session: DAPSession
    _namespace: str
    _table: str
    _query: IncrementalQuery

    def __init__(
        self, session: DAPSession, namespace: str, table: str, since: datetime
    ) -> None:
        self._session = session
        self._namespace = namespace
        self._table = table
        self._query = IncrementalQuery(
            format=Format.JSONL, filter=None, since=since, until=None
        )

    async def get_client(self) -> IncrementalClient:
        table_data = await self._session.get_table_data(
            self._namespace, self._table, self._query
        )

        table_schema = await self._session.get_table_schema(
            self._namespace, self._table
        )
        if table_schema.version != table_data.schema_version:
            raise SchemaVersionMismatchError(
                table_schema.version, table_data.schema_version
            )

        job_id = table_data.job_id
        object_count = len(table_data.objects)

        async def download(
            db_lock: DatabaseLock, processor: AbstractSyncProcessor
        ) -> None:
            for object_index, obj in enumerate(table_data.objects):
                context_aware_object = ContextAwareObject(
                    id=obj.id,
                    index=object_index,
                    job_id=job_id,
                    total_count=object_count,
                )
                await self._download_and_save(db_lock, context_aware_object, processor)

            await processor.close()

        return IncrementalClient(
            download=download, table_data=table_data, table_schema=table_schema
        )

    async def _download_and_save(
        self,
        db_lock: DatabaseLock,
        obj: ContextAwareObject,
        processor: AbstractSyncProcessor,
    ) -> None:
        "Reads JSON records from a stream and makes them upserted or deleted via the processor."

        resource_array = await self._session.get_resources([Object(id=obj.id)])
        if len(resource_array) != 1:
            raise DownloadError("unable to get resource URLs for objects")

        resource = resource_array[0]
        async with self._session.stream_resource(resource) as stream:
            records = get_json_lines_from_gzip_stream(stream)
            async with db_lock():
                await processor.process(obj, records)
