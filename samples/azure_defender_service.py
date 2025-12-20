from azure_python.hosting import container
from azure_python.protocols.i_azure_defender_service import IAzureDefenderService


async def main():
    svc = container[IAzureDefenderService]
    results = await svc.get_compliance_results("<resource_id>")
    print(results)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
