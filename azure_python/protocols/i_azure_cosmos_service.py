from typing import Any, Protocol


class IAzureCosmosService(Protocol):
    """Protocol for Cosmos Service."""

    async def list_databases(self) -> list[str]:
        """List all databases within the given Cosmos instance."""
        ...

    async def list_containers(self, database_name: str) -> list[str]:
        """List all containers within the given database.

        :param database_name: The name of the database.
        :return: A list of container names.
        """
        ...

    async def create_container(
        self, database_name: str, container_name: str, partition_key="/id"
    ) -> None:
        """Create a container within the given database.

        :param database_name: The name of the database.
        :param container_name: The name of the container.
        :param partition_key: The partition key.
        """
        ...

    async def delete_container(self, database_name: str, container_name: str) -> None:
        """Delete a container within the given database.

        :param database_name: The name of the database.
        :param container_name: The name of the container.
        """
        ...

    async def list_items(
        self, database_name: str, container_name: str
    ) -> list[dict[str, Any]]:
        """List all items within the given container.

        :param database_name: The name of the database.
        :param container_name: The name of the container.
        :return: A list of items.
        """
        ...

    async def query(
        self,
        database_name: str,
        container_name: str,
        query: str,
        parameters: list[Any] = [],
    ) -> list[Any]:
        """Query the container with the given query and parameters.

        :param database_name: The name of the database.
        :param container_name: The name of the container.
        :param query: The query to execute.
        :param parameters: The parameters to use in the query.
        :return: A list of results.
        """
        ...

    async def create_item(
        self, database_name: str, container_name: str, item: dict[str, Any]
    ) -> dict[str, Any]:
        """Create an item in the given container.

        :param database_name: Database name to create item.
        :param container_name: Container name to create item.
        :param item: Item to create.
        :return: Created item.
        """
        ...

    async def create_items(
        self, database_name: str, container_name: str, items: list[dict[str, Any]]
    ) -> None:
        """Create multiple items in the given container.

        :param database_name: Database name to create items.
        :param container_name: Container name to create items.
        :param items: Items to create.
        """
        ...

    async def update_item(
        self, database_name: str, container_name: str, item: dict[str, Any]
    ) -> dict[str, Any]:
        """Update an item in the given container.

        :param database_name: Database name to update item.
        :param container_name: Container name to update item.
        :param item: Item to update.
        :return: Updated item.
        """
        ...
