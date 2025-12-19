import asyncio

from azure_python.hosting import container
from azure_python.protocols.i_azure_managed_redis_service import (
    IAzureManagedRedisService,
)


async def main() -> None:
    svc = container[IAzureManagedRedisService]

    ping = await svc.ping()
    assert ping is True
    await svc.set("my_key", "my_value")
    assert await svc.get("my_key") == "my_value"


if __name__ == "__main__":
    asyncio.run(main())
