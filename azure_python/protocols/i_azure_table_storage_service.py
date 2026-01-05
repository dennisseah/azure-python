from typing import Protocol


class IAzureTableStorageService(Protocol):
    async def list_tables(self) -> list[str]:
        """List all tables in the storage account

        :return: List of table names
        """
        ...

    async def is_table_exist(self, table_name: str) -> bool:
        """Check if a table exists

        :param table_name: The name of the table to check
        :return: True if the table exists.
        """
        ...

    async def create_table(self, table_name: str) -> bool:
        """Create a table

        :param table_name: The name of the table to create
        :return: True if the table was created successfully.
        """
        ...

    async def insert_entity(self, table_name: str, entity: dict) -> None:
        """Insert an entity into a table

        :param table_name: The name of the table
        :param entity: The entity to insert
        """
        ...

    async def delete_table(self, table_name: str) -> bool:
        """Delete a table

        :param table_name: The name of the table to delete
        :return: True if the table was deleted successfully.
        """
        ...

    async def delete_entity(
        self, table_name: str, partition_key: str, row_key: str
    ) -> None:
        """Delete an entity from a table

        :param table_name: The name of the table
        :param partition_key: The partition key of the entity
        :param row_key: The row key of the entity
        """
        ...

    async def get_entity(
        self, table_name: str, partition_key: str, row_key: str
    ) -> dict | None:
        """Get an entity from a table

        :param table_name: The name of the table
        :param partition_key: The partition key of the entity
        :param row_key: The row key of the entity
        :return: The entity if found, None otherwise.
        """
        ...

    async def list_entities(self, table_name: str) -> list[dict]:
        """List all entities in a table

        :param table_name: The name of the table
        :return: List of entities
        """
        ...

    async def update_entity(self, table_name: str, entity: dict) -> None:
        """Update an entity in a table

        :param table_name: The name of the table
        :param entity: The entity to update
        """
        ...

    async def upsert_entity(self, table_name: str, entity: dict) -> None:
        """Upsert an entity in a table

        :param table_name: The name of the table
        :param entity: The entity to upsert
        """
        ...

    async def query_entities(self, table_name: str, filter_query: str) -> list[dict]:
        """Query entities in a table

        :param table_name: The name of the table
        :param filter_query: The filter query string
        :return: List of entities matching the query
        """
        ...
