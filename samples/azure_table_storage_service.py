import asyncio

from azure_python.hosting import container
from azure_python.protocols.i_azure_table_storage_service import (
    IAzureTableStorageService,
)
from samples.utils import set_log_level

TBL_NAME = "TestTable"
PART_KEY = "partition1"
ROW_KEY = "row1"


async def main() -> None:
    svc = container[IAzureTableStorageService]
    await svc.create_table(table_name="TestTable")
    exists = await svc.is_table_exist(table_name="TestTable")
    assert exists is True

    await svc.insert_entity(
        table_name=TBL_NAME,
        entity={"PartitionKey": PART_KEY, "RowKey": ROW_KEY, "Data": "SampleData"},
    )

    entity = await svc.get_entity(
        table_name=TBL_NAME,
        partition_key=PART_KEY,
        row_key=ROW_KEY,
    )
    print(f"Retrieved entity: {entity}")

    entities = await svc.list_entities(TBL_NAME)
    print(f"Entities in 'TestTable': {entities}")

    await svc.update_entity(
        table_name=TBL_NAME,
        entity={"PartitionKey": PART_KEY, "RowKey": ROW_KEY, "Data": "UpdatedData"},
    )

    await svc.upsert_entity(
        table_name=TBL_NAME,
        entity={"PartitionKey": PART_KEY, "RowKey": "row2", "Data": "UpsertedData"},
    )

    response = await svc.query_entities(
        table_name=TBL_NAME,
        filter_query="PartitionKey eq 'partition1'",
    )
    print(f"Query result: {response}")

    await svc.delete_entity(
        table_name=TBL_NAME,
        partition_key=PART_KEY,
        row_key=ROW_KEY,
    )
    await svc.delete_table(table_name=TBL_NAME)


if __name__ == "__main__":
    set_log_level("INFO")
    asyncio.run(main())
