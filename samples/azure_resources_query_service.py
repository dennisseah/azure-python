from azure_python.hosting import container
from azure_python.protocols.i_azure_resources_query_service import (
    IAzureResourcesQueryService,
)


async def main():
    svc = container[IAzureResourcesQueryService]
    resources = await svc.fetch_resources("<subscription_id>")
    print(f"Fetched {len(resources)} resources")
    print(resources)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
