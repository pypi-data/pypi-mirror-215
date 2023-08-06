from dataclasses import dataclass
from typing import Any, Dict

try:
    from redis.asyncio import ConnectionPool, Redis
except ImportError as e:
    import sys

    print("Install extra webapi to use Redis extension.", file=sys.stderr)
    raise e

from piaf.ptf import Extension


@dataclass(eq=True, frozen=True)
class RedisExtensionSettings:
    """
    A set of settings to configure an instance of the :class:`RedisConnectionPoolExtension` type.
    """

    redis_host: str
    redis_user: str
    redis_password: str
    redis_db: int = 0
    redis_max_connections: int = 10
    redis_scheme: str = "redis"


class RedisConnectionPoolExtension(Extension):
    """
    An extension providing a pool of Redis connections.

    The user is responsible of closing its session (connection) once the work is finished.
    """

    def __init__(self, settings: RedisExtensionSettings) -> None:
        """
        Create a new :class:`RedisConnectionPoolExtension` instance.

        The pool is not bound.

        :param settings: extension settings used to setup the pool.
        """
        self._settings = settings
        self._pool: ConnectionPool | None = None

    async def on_start(self) -> None:
        """
        Initialize the pool and test the connection.

        :raise ConnectionError: Unable to establish a connection to Redis.
        """
        options: Dict[str, Any] = {
            "decode_responses": True,
            "max_connections": self._settings.redis_max_connections,
        }
        if self._settings.redis_user and self._settings.redis_password:
            options.update(
                {
                    "username": self._settings.redis_user,
                    "password": self._settings.redis_password,
                }
            )
        if self._settings.redis_db:
            options["db"] = self._settings.redis_db

        self._pool = ConnectionPool.from_url(
            f"{self._settings.redis_scheme}://{self._settings.redis_host}", **options
        )

        try:
            client: Redis = self.client
            await client.ping()  # Ping to test the connection
            await client.close()
        except Exception as e:
            await client.close()
            if self._pool is not None:
                await self._pool.disconnect()
            raise ConnectionError("Redis instance is not reachable.") from e

    async def on_stop(self) -> None:
        """Disconnect all connections and close the pool."""
        if self._pool is not None:
            await self._pool.disconnect()

    @property
    def client(self) -> Redis:
        """
        Get a Redis session.

        :raise ConnectionError: the pool is not bound yet.
        :return: a session
        """
        if self._pool is None:
            raise ConnectionError("Connection pool is not initialized.")
        return Redis(connection_pool=self._pool)
