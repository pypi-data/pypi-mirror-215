"""Module to manage resource items in a PostgreSQL database."""

import asyncio
import asyncpg
import contextvars
import dataclasses
import fondat.codec
import fondat.error
import fondat.sql
import json
import logging
import types
import typing
import uuid

from collections.abc import AsyncIterator, Iterable, Mapping, Sequence
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from fondat.codec import Codec, DecodeError, JSONCodec
from fondat.data import datacls
from fondat.sql import Expression, Param
from fondat.types import is_optional, is_subclass, literal_values, strip_annotations
from fondat.validation import validate, validate_arguments
from types import NoneType
from typing import Annotated, Any, Generic, Literal, TypeVar, get_args, get_origin
from uuid import UUID


_logger = logging.getLogger(__name__)


PT = TypeVar("PT")  # python type
ST = TypeVar("ST")  # sql type


Schema = TypeVar("Schema")
T = TypeVar("T")


class PostgreSQLCodec(Codec[PT, Any]):
    """Base class for PostgreSQL codecs."""

    _cache = {}


class _PassthroughCodec(Generic[PT]):
    """..."""

    @validate_arguments
    def encode(self, value: PT) -> PT:
        return value

    @validate_arguments
    def decode(self, value: PT) -> PT:
        return value


class StrCodec(_PassthroughCodec[str], PostgreSQLCodec[str]):
    sql_type = "TEXT"

    @staticmethod
    def handles(python_type: Any) -> bool:
        python_type = strip_annotations(python_type)
        return is_subclass(python_type, str)


class FloatCodec(_PassthroughCodec[float], PostgreSQLCodec[float]):
    sql_type = "DOUBLE PRECISION"

    @staticmethod
    def handles(python_type: Any) -> bool:
        python_type = strip_annotations(python_type)
        return is_subclass(python_type, float)


class DecimalCodec(_PassthroughCodec[Decimal], PostgreSQLCodec[Decimal]):
    sql_type = "NUMERIC"

    @staticmethod
    def handles(python_type: Any) -> bool:
        python_type = strip_annotations(python_type)
        return is_subclass(python_type, Decimal)


class BytesCodec(_PassthroughCodec[bytes], PostgreSQLCodec[bytes]):
    sql_type = "BYTEA"

    @staticmethod
    def handles(python_type: Any) -> bool:
        python_type = strip_annotations(python_type)
        return is_subclass(python_type, bytes)


class BytearrayCodec(_PassthroughCodec[bytearray], PostgreSQLCodec[bytearray]):
    sql_type = "BYTEA"

    @staticmethod
    def handles(python_type: Any) -> bool:
        python_type = strip_annotations(python_type)
        return is_subclass(python_type, bytearray)

    @validate_arguments
    def decode(self, value: bytes | bytearray) -> bytearray:
        return value if isinstance(value, bytearray) else bytearray(value)


class IntCodec(_PassthroughCodec[int], PostgreSQLCodec[int]):
    sql_type = "BIGINT"

    @staticmethod
    def handles(python_type: Any) -> bool:
        python_type = strip_annotations(python_type)
        return is_subclass(python_type, int) and not is_subclass(python_type, bool)


class BoolCodec(_PassthroughCodec[bool], PostgreSQLCodec[bool]):
    sql_type = "BOOLEAN"

    @classmethod
    def handles(cls, python_type: Any) -> bool:
        python_type = strip_annotations(python_type)
        return is_subclass(python_type, bool)

    @validate_arguments
    def decode(self, value: int | bool) -> bool:
        return bool(value)


class DateCodec(_PassthroughCodec[date], PostgreSQLCodec[date]):
    sql_type = "DATE"

    @classmethod
    def handles(cls, python_type: Any) -> bool:
        python_type = strip_annotations(python_type)
        return is_subclass(python_type, date) and not is_subclass(python_type, datetime)


class DatetimeCodec(_PassthroughCodec[datetime], PostgreSQLCodec[datetime]):
    sql_type = "TIMESTAMP WITH TIME ZONE"

    @classmethod
    def handles(cls, python_type: Any) -> bool:
        python_type = strip_annotations(python_type)
        return is_subclass(python_type, datetime)


class UUIDCodec(_PassthroughCodec[UUID], PostgreSQLCodec[UUID]):
    sql_type = "UUID"

    @classmethod
    def handles(cls, python_type: Any) -> bool:
        python_type = strip_annotations(python_type)
        return is_subclass(python_type, UUID)


class ArrayCodec(PostgreSQLCodec[PT]):
    """..."""

    _AVOID = str | bytes | bytearray | Mapping | tuple

    @classmethod
    def handles(cls, python_type: Any) -> bool:
        python_type = strip_annotations(python_type)
        origin = get_origin(python_type) or python_type
        args = get_args(python_type)
        return (
            is_subclass(origin, Iterable)
            and not is_subclass(origin, cls._AVOID)
            and len(args) == 1
        )

    def __init__(self, python_type: Any):
        super().__init__(python_type)
        python_type = strip_annotations(python_type)
        self.codec = PostgreSQLCodec.get(get_args(python_type)[0])
        self.sql_type = f"{self.codec.sql_type}[]"

    def encode(self, value: PT) -> Any:
        return [self.codec.encode(v) for v in value]

    def decode(self, value: Any) -> PT:
        return self.python_type(self.codec.decode(v) for v in value)


class UnionCodec(PostgreSQLCodec[PT]):
    """
    Codec that encodes/decodes a UnionType, Union or optional value to/from a compatible SQL
    value. For an optional type, it will use the codec for its type, otherwise it will
    encode/decode as JSONB.
    """

    @staticmethod
    def handles(python_type: Any) -> bool:
        python_type = strip_annotations(python_type)
        return typing.get_origin(python_type) in {typing.Union, types.UnionType}

    def __init__(self, python_type: type[PT]):
        super().__init__(python_type)
        raw_type = strip_annotations(python_type)
        args = typing.get_args(raw_type)
        self.is_nullable = is_optional(raw_type)
        args = [a for a in args if a is not NoneType]
        self.codec = PostgreSQLCodec.get(args[0]) if len(args) == 1 else JSONBCodec(python_type)
        self.sql_type = self.codec.sql_type

    def encode(self, value: PT) -> Any:
        if value is None:
            return None
        return self.codec.encode(value)

    def decode(self, value: Any) -> PT:
        if value is None and self.is_nullable:
            return None
        return self.codec.decode(value)


class LiteralCodec(PostgreSQLCodec[PT]):
    """
    Codec that encodes/decodes a Literal value to/from a compatible SQL value. If all literal
    values share the same type, then it will use a codec for that type, otherwise it will
    encode/decode as JSONB.
    """

    @staticmethod
    def handles(python_type: Any) -> bool:
        python_type = strip_annotations(python_type)
        return typing.get_origin(python_type) is Literal

    def __init__(self, python_type: type[PT]):
        super().__init__(python_type)
        self.literals = literal_values(python_type)
        types = list({type(literal) for literal in self.literals})
        self.codec = (
            PostgreSQLCodec.get(types[0]) if len(types) == 1 else JSONBCodec(python_type)
        )
        self.is_nullable = is_optional(python_type) or None in self.literals
        self.sql_type = self.codec.sql_type

    def encode(self, value: PT) -> Any:
        if value is None:
            return None
        return self.codec.encode(value)

    def decode(self, value: Any) -> PT:
        if value is None and self.is_nullable:
            return None
        result = self.codec.decode(value)
        if result not in self.literals:
            raise DecodeError
        return result


class JSONBCodec(PostgreSQLCodec[PT]):
    """
    Codec that encodes/decodes a value to/from a SQL JSONB value. This is the "fallback" codec,
    which handles any type not handled by any other codec.
    """

    sql_type = "JSONB"

    @staticmethod
    def handles(python_type: Any) -> bool:
        python_type = strip_annotations(python_type)
        for other in (c for c in PostgreSQLCodec.__subclasses__() if c is not JSONBCodec):
            if other.handles(python_type):
                return False
        return True

    def __init__(self, python_type: Any):
        super().__init__(python_type)
        self.codec = JSONCodec.get(python_type)

    def encode(self, value: PT) -> Any:
        return json.dumps(self.codec.encode(value))

    def decode(self, value: Any) -> PT:
        return self.codec.decode(json.loads(value))


class _Results(AsyncIterator[T]):
    __slots__ = {"statement", "result", "rows", "codecs"}

    def __init__(self, statement, result, rows):
        self.statement = statement
        self.result = result
        self.rows = rows
        self.codecs = {
            k: PostgreSQLCodec.get(t)
            for k, t in typing.get_type_hints(result, include_extras=True).items()
        }

    def __aiter__(self):
        return self

    async def __anext__(self) -> T:
        row = await anext(self.rows)
        build = {}
        for key in self.codecs:
            with DecodeError.path_on_error(key):
                build[key] = self.codecs[key].decode(row[key])
        result = self.result(**build)
        validate(result, self.result)
        return result


# fmt: off
@datacls
class Config:
    """PostgreSQL connection pool configuration."""
    dsn: Annotated[str | None, "connection arguments in libpg connection URI format"]
    min_size: Annotated[int | None, "number of connections to initialize pool with"]
    max_size: Annotated[int | None, "maximum number of connections in the pool"]
    max_queries: Annotated[int | None, "number of queries before connection is replaced"]
    max_inactive_connection_lifetime: Annotated[float | None, "seconds after inactive connection closed"]
    host: Annotated[str | None, "database host address"]
    port: Annotated[int | None, "port number to connect to"]
    user: Annotated[str | None, "the name of the database role used for authentication"]
    password: Annotated[str | None, "password to be used for authentication"]
    passfile: Annotated[str | None, "the name of the file used to store passwords"]
    database: Annotated[str | None, "the name of the database to connect to"]
    timeout: Annotated[float | None, "connection timeout in seconds"]
    ssl: Literal["disable", "prefer", "require", "verify-ca", "verify-full"] | None
# fmt: on


@asynccontextmanager
async def _async_null_context():
    yield


class Database(fondat.sql.Database):
    """
    Manages access to a PostgreSQL database.

    Parameters:
    • config: connection pool configuration

    The connection pool will be initialized on the first connection request, or it can be
    explicitly initialized using the `init` method.
    """

    def __init__(self, config: Config):
        self._config = config
        self._conn = contextvars.ContextVar("fondat_postgresql_conn", default=None)
        self._txn = contextvars.ContextVar("fondat_postgresql_txn", default=None)
        self._task = contextvars.ContextVar("fondat_postgresql_task", default=None)
        self._pool = None

    @classmethod
    async def new(cls, config: Config) -> "Database":
        """Deprecated."""
        self = cls(config)
        await self.init()
        return self

    @classmethod
    async def create(cls, config: Config) -> "Database":
        """Deprecated."""
        self = cls(config)
        await self.init()
        return self

    async def init(self) -> None:
        """Create database connection pool."""
        if not self._pool:
            _logger.debug("create connection pool")
            self._pool = await asyncpg.create_pool(
                **{k: v for k, v in dataclasses.asdict(self._config).items() if v is not None}
            )

    async def close(self) -> None:
        """Close database connection pool."""
        if self._pool:
            await self._pool.close()
        self._pool = None

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[None]:
        task = asyncio.current_task()
        if self._conn.get() and self._task.get() is task:
            yield  # connection already established
            return
        await self.init()
        _logger.debug("acquire connection from pool")
        self._task.set(task)
        async with self._pool.acquire(timeout=self._config.timeout) as connection:
            self._conn.set(connection)
            try:
                yield
            finally:
                _logger.debug("release connection to pool")
                self._conn.set(None)

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        """
        Return an asynchronous context manager, which scopes a transaction in which
        statement(s) are executed. Upon exit of the context, if an exception was raised,
        changes will be rolled back; otherwise changes will be committed.
        """
        txid = uuid.uuid4().hex
        _logger.debug("transaction begin %s", txid)
        token = self._txn.set(txid)
        async with self.connection():
            connection = self._conn.get()
            transaction = connection.transaction()
            await transaction.start()

            async def commit():
                _logger.debug("transaction commit %s", txid)
                await transaction.commit()

            async def rollback():
                _logger.debug("transaction rollback %s", txid)
                await transaction.rollback()

            try:
                yield
            except GeneratorExit:  # explicit cleanup of asynchronous generator
                await commit()
            except Exception:
                await rollback()
                raise
            else:
                await commit()
            finally:
                self._txn.reset(token)

    async def execute(
        self,
        statement: Expression,
        result: type[T] = None,
    ) -> AsyncIterator[T] | None:
        """
        Execute a SQL statement.

        Parameters:
        • statement: SQL statement to excute
        • result: the type to return a query result row

        If the statement is a query that generates results, each row can be returned in
        a dataclass or TypedDict object, whose type is specifed in the `result` parameter.
        Rows are provided via a returned asynchronous iterator.

        Must be called within a database transaction context.
        """
        if not self._txn.get():
            raise RuntimeError("transaction context required to execute statement")
        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug(str(statement))
        text = []
        args = []
        for fragment in statement:
            if isinstance(fragment, str):
                text.append(fragment)
            else:
                args.append(PostgreSQLCodec.get(fragment.type).encode(fragment.value))
                text.append(f"${len(args)}")
        text = "".join(text)
        conn = self._conn.get()
        if result is None:
            await conn.execute(text, *args)
        else:  # expecting results
            return _Results(statement, result, conn.cursor(text, *args).__aiter__())

    def sql_type(self, type: Any) -> str:
        """Return the SQL type string that corresponds with the specified Python type."""
        return PostgreSQLCodec.get(type).sql_type


class Table(fondat.sql.Table[Schema]):
    """..."""

    async def upsert(self, value: Schema):
        """
        Upsert table row. Must be called within a database transaction context.
        """
        stmt = Expression(
            f"INSERT INTO {self.name} (",
            ", ".join(self.columns),
            ") VALUES (",
            Expression.join(
                (
                    Param(getattr(value, name), python_type)
                    for name, python_type in self.columns.items()
                ),
                ", ",
            ),
            f") ON CONFLICT ({self.pk}) DO UPDATE SET ",
            Expression.join(
                (
                    Expression(f"{name} = ", Param(getattr(value, name), python_type))
                    for name, python_type in self.columns.items()
                    if name != self.pk
                ),
                ", ",
            ),
            ";",
        )
        await self.database.execute(stmt)


@dataclass
class Index(fondat.sql.Index):
    """
    Represents an index on a table in a PostgreSQL database.

    Parameters:
    • name: name of index
    • table: table that the index defined for
    • keys: index keys (typically column names with optional order)
    • unique: is index unique
    • method: indexing method
    """

    method: str | None = None

    async def create(self, execute: bool = True) -> Expression:
        """
        Generate statement to create index in database.

        Parameters:
        • execute: execute statement

        Statement must be executed within a database transaction context.
        """
        stmt = Expression()
        stmt += "CREATE "
        if self.unique:
            stmt += "UNIQUE "
        stmt += f"INDEX {self.name} ON {self.table.name} "
        if self.method:
            stmt += f"USING {self.method} "
        stmt += "("
        stmt += ", ".join(self.keys)
        stmt += ");"
        if execute:
            await self.table.database.execute(stmt)
        return stmt
