import asyncio

from azure_python.common.log_utils import set_log_level
from azure_python.hosting import container


async def main() -> None:
    from azure_python.protocols.i_azure_blob_storage_service import (
        IAzureBlobStorageService,
    )

    svc = container[IAzureBlobStorageService]
    datasets = await svc.list_blobs(container_name="datasets")

    print("Blobs in 'datasets' container:")
    for name in datasets:
        print(f"- {name}")


if __name__ == "__main__":
    set_log_level("DEBUG")
    asyncio.run(main())
