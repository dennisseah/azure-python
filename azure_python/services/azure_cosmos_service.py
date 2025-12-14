import asyncio
import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncIterator

from azure.cosmos.aio import CosmosClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from azure.cosmos.partition_key import PartitionKey
from azure.identity.aio import DefaultAzureCredential
from lagom.environment import Env

from azure_python.protocols.i_azure_cosmos_service import IAzureCosmosService


class AzureCosmosServiceEnv(Env):
    """Configuration for the Cosmos Service."""

    azure_cosmos_host: str
    azure_cosmos_key: str | None = None


@dataclass
class AzureCosmosService(IAzureCosmosService):
    env: AzureCosmosServiceEnv
    logger: logging.Logger

    @asynccontextmanager
    async def get_cosmos_client(self) -> AsyncIterator[CosmosClient]:
        client = CosmosClient(
            self.env.azure_cosmos_host,
            (
                DefaultAzureCredential()
                if self.env.azure_cosmos_key is None
                else {"masterKey": self.env.azure_cosmos_key}
            ),
            connection_verify=False,
        )

        try:
            yield client
        finally:
            await client.close()

    async def list_databases(self) -> list[str]:
        self.logger.debug("[BEGIN] list_databases")
        async with self.get_cosmos_client() as client:
            databases = client.list_databases()
            database_ids = [database["id"] async for database in databases]
            self.logger.debug(f"[COMPLETED] list_databases, count: {len(database_ids)}")
            return database_ids

    async def list_containers(self, database_name: str) -> list[str]:
        self.logger.debug("[BEGIN] list_containers")
        async with self.get_cosmos_client() as client:
            database = client.get_database_client(database_name)
            containers = database.list_containers()  # type: ignore
            container_ids = [container["id"] async for container in containers]
            self.logger.debug(
                f"[COMPLETED] list_containers, count: {len(container_ids)}"
            )

            return container_ids

    async def create_container(
        self, database_name: str, container_name: str, partition_key="/id"
    ) -> None:
        self.logger.debug("[BEGIN] create_container")
        async with self.get_cosmos_client() as client:
            database = client.get_database_client(database_name)
            await database.create_container(
                id=container_name, partition_key=PartitionKey(path=partition_key)
            )
            self.logger.debug("[COMPLETED] create_container")

    async def delete_container(self, database_name: str, container_name: str) -> None:
        self.logger.debug("[BEGIN] delete_container")
        async with self.get_cosmos_client() as client:
            database = client.get_database_client(database_name)
            try:
                await database.delete_container(container_name)
            except CosmosResourceNotFoundError:
                self.logger.info(f"container {container_name} not found")

            self.logger.debug("[COMPLETED] delete_container")

    async def list_items(
        self, database_name: str, container_name: str
    ) -> list[dict[str, Any]]:
        self.logger.debug("[BEGIN] list_items")
        async with self.get_cosmos_client() as client:
            database = client.get_database_client(database_name)
            container = database.get_container_client(container_name)
            items = container.query_items(query="SELECT * FROM c")
            data = [item async for item in items]
            self.logger.debug(f"[COMPLETED] list_items, count: {len(data)}")
            return data

    async def query(
        self,
        database_name: str,
        container_name: str,
        query: str,
        parameters: list[Any] = [],
    ) -> list[Any]:
        self.logger.debug("[BEGIN] query")
        async with self.get_cosmos_client() as client:
            database = client.get_database_client(database_name)
            container = database.get_container_client(container_name)
            items = container.query_items(query=query, parameters=parameters)
            data = [item async for item in items]
            self.logger.debug(f"[COMPLETED] query, count: {len(data)}")
            return data

    async def create_item(
        self, database_name: str, container_name: str, item: dict[str, Any]
    ) -> dict[str, Any]:
        self.logger.debug("[BEGIN] create_item")
        async with self.get_cosmos_client() as client:
            database = client.get_database_client(database_name)
            container = database.get_container_client(container_name)
            created_item = await container.create_item(body=item)
            self.logger.debug("[COMPLETED] create_item")
            return created_item

    async def create_items(
        self, database_name: str, container_name: str, items: list[dict[str, Any]]
    ) -> None:
        self.logger.debug(f"[BEGIN] create_items, count {len(items)}")
        async with self.get_cosmos_client() as client:
            database = client.get_database_client(database_name)
            container = database.get_container_client(container_name)

            async def fn_create(item):
                return await container.create_item(body=item)

            await asyncio.gather(*[fn_create(item) for item in items])
            self.logger.debug(f"[COMPLETED] create_items, count {len(items)}")

    async def update_item(
        self, database_name: str, container_name: str, item: dict[str, Any]
    ) -> dict[str, Any]:
        self.logger.debug("[BEGIN] update_item")
        async with self.get_cosmos_client() as client:
            database = client.get_database_client(database_name)
            container = database.get_container_client(container_name)
            updated_item = await container.upsert_item(body=item)
            self.logger.debug("[COMPLETED] update_item")
            return updated_item
