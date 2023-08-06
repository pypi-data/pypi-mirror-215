from ...integration.validator import AbstractDatabaseValidator
from typing import Optional

from ...dap_types import VersionedSchema
from ...integration.connection import AbstractDatabaseConnection
from ...integration.database_errors import DatabaseConnectionError
from ...integration.meta_table import AbstractMetaTableManager
from ...integration.validator import AbstractDatabaseValidator
from ...integration.processor import AbstractInitProcessor, AbstractSyncProcessor
from .validator import DatabaseValidator
from ...integration.plugin import DatabasePlugin
from ...integration.processor import AbstractInitProcessor, AbstractSyncProcessor
from ..sqlalchemy.connection import SqlAlchemyConnection
from .init_processor import InitProcessor
from .meta_table import MetaTableManager
from .sync_processor import SyncProcessor


class PostgresPlugin(DatabasePlugin):
    
    _connection: Optional[SqlAlchemyConnection]

    def __init__(self) -> None:
        self._connection = None

    def connect(self, connection_string: str) -> None:
        if self._connection is not None:
            raise DatabaseConnectionError("already connected to the database")

        self._connection = SqlAlchemyConnection(
            connection_string, {"postgresql": "asyncpg"}
        )

    def get_connection(self) -> AbstractDatabaseConnection:
        if self._connection is None:
            raise DatabaseConnectionError("not connected to the database")
        return self._connection

    def create_metatable_manager(
        self, namespace: str, table: str
    ) -> AbstractMetaTableManager:
        if self._connection is None:
            raise DatabaseConnectionError("not connected to the database")
        return MetaTableManager(self._connection, namespace, table)

    def create_init_processor(
        self,
        namespace: str,
        table: str,
        schema: VersionedSchema,
    ) -> AbstractInitProcessor:
        if self._connection is None:
            raise DatabaseConnectionError("not connected to the database")
        return InitProcessor(self._connection, namespace, table, schema)

    def create_sync_processor(
        self,
        namespace: str,
        table: str,
        schema: VersionedSchema,
    ) -> AbstractSyncProcessor:
        if self._connection is None:
            raise DatabaseConnectionError("not connected to the database")
        return SyncProcessor(self._connection, namespace, table, schema)
    
    def create_database_validator(
        self,
        namespace: str,
        table: str
    ) -> AbstractDatabaseValidator:
        if self._connection is None:
            raise DatabaseConnectionError("not connected to the database")
        return DatabaseValidator(self._connection, namespace, table)
