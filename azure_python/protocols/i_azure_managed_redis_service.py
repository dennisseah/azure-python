from typing import Any, Protocol


class IAzureManagedRedisService(Protocol):
    async def ping(self) -> bool:
        """Ping the Redis cache to check connectivity.

        :return: True if the Redis cache is reachable, False otherwise.
        """
        ...

    async def set(self, key: str, value: Any) -> None:
        """Set a value in the Redis cache.

        :param key: The key under which the value is stored.
        :param value: The value to store.
        """
        ...

    async def get(self, key: str) -> Any:
        """Get a value from the Redis cache.

        :param key: The key whose value is to be retrieved.
        :return: The value stored under the given key.
        """
        ...
