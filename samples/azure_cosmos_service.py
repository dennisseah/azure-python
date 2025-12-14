from azure_python.hosting import container


async def main() -> None:
    from azure_python.protocols.i_azure_cosmos_service import IAzureCosmosService

    svc = container[IAzureCosmosService]
    print(await svc.list_containers("sample-db"))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
