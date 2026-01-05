import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

from azure.data.tables.aio import TableServiceClient
from azure.identity.aio import DefaultAzureCredential
from lagom.environment import Env

from azure_python.protocols.i_azure_table_storage_service import (
    IAzureTableStorageService,
)


class AzureTableStorageServiceEnv(Env):
    azure_table_storage_url: str


@dataclass
class AzureTableStorageService(IAzureTableStorageService):
    """
    Azure Blob Storage Service implementation.
    """

    logger: logging.Logger
    env: AzureTableStorageServiceEnv

    @asynccontextmanager
    async def get_client(self) -> AsyncIterator[TableServiceClient]:
        """Get a blob service client with proper connection management.

        :return:BlobStorageClient
        """
        credential = None
        client = None

        try:
            credential = DefaultAzureCredential()
            client = TableServiceClient(
                self.env.azure_table_storage_url,
                credential=credential,
            )
            yield client
        finally:
            # Ensure proper cleanup order: client first, then credential
            if client:
                try:
                    await client.close()
                except Exception as e:
                    self.logger.warning(f"Error closing blob client: {e}")

            if credential:
                try:
                    await credential.close()
                except Exception as e:
                    self.logger.warning(f"Error closing credential: {e}")

    async def is_table_exist(self, table_name: str) -> bool:
        async with self.get_client() as client:
            try:
                table_client = client.get_table_client(table_name)
                await table_client.get_table_access_policy()
                return True
            except Exception:
                return False

    async def create_table(self, table_name: str) -> bool:
        async with self.get_client() as client:
            await client.create_table_if_not_exists(table_name=table_name)
            return True

    async def delete_table(self, table_name: str) -> bool:
        async with self.get_client() as client:
            table_client = client.get_table_client(table_name)
            await table_client.delete_table()
            return True

    async def list_tables(self) -> list[str]:
        async with self.get_client() as client:
            tables = client.list_tables()
            table_names = [table.name async for table in tables]
            return table_names

    async def insert_entity(self, table_name: str, entity: dict) -> None:
        async with self.get_client() as client:
            table_client = client.get_table_client(table_name)
            await table_client.create_entity(entity=entity)

    async def delete_entity(
        self, table_name: str, partition_key: str, row_key: str
    ) -> None:
        async with self.get_client() as client:
            table_client = client.get_table_client(table_name)
            await table_client.delete_entity(
                partition_key=partition_key,
                row_key=row_key,
            )

    async def get_entity(
        self, table_name: str, partition_key: str, row_key: str
    ) -> dict | None:
        async with self.get_client() as client:
            table_client = client.get_table_client(table_name)
            entity = await table_client.get_entity(
                partition_key=partition_key,
                row_key=row_key,
            )
            return entity

    async def list_entities(self, table_name: str) -> list[dict]:
        async with self.get_client() as client:
            table_client = client.get_table_client(table_name)
            entities = table_client.list_entities()
            results: list[dict] = []

            async for entity in entities:
                results.append(entity)

            return results
