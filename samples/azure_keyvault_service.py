import asyncio

from azure_python.hosting import container
from azure_python.protocols.i_azure_keyvault_service import (
    IAzureKeyVaultService,
)
from samples.utils import set_log_level


async def main() -> None:
    svc = container[IAzureKeyVaultService]

    await svc.set_secret("mySecret", "mySecretValue")
    assert await svc.get_secret("mySecret") == "mySecretValue"


if __name__ == "__main__":
    set_log_level("INFO")
    asyncio.run(main())
