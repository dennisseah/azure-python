import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient
from lagom.environment import Env

from azure_python.protocols.i_azure_blob_storage_service import (
    IAzureBlobStorageService,
)


class AzureBlobStorageServiceEnv(Env):
    azure_blob_storage_url: str


@dataclass
class AzureBlobStorageService(IAzureBlobStorageService):
    """
    Azure Blob Storage Service implementation.
    """

    logger: logging.Logger
    env: AzureBlobStorageServiceEnv

    @asynccontextmanager
    async def get_storage_client(self) -> AsyncIterator[BlobServiceClient]:
        """Get a blob service client with proper connection management.

        :return:BlobStorageClient
        """
        credential = None
        client = None

        try:
            credential = DefaultAzureCredential()

            client = BlobServiceClient(
                self.env.azure_blob_storage_url,
                credential=credential,
                connection_timeout=30,  # 30 second timeout
                read_timeout=60,  # 60 second read timeout
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

    async def is_blob_exists(self, container_name: str, blob_name: str) -> bool:
        """Return True if a blob exists in the storage account.

        :param container_name: Name of the container.
        :param blob_name: Name of the blob.
        :return: True if the blob exists, False otherwise.
        """
        self.logger.debug(
            f"[BEGIN] is_blob_exists, container_name: {container_name}, blob_name: {blob_name}"  # noqa E501
        )

        async with self.get_storage_client() as blob_storage_client:
            blob_client = blob_storage_client.get_blob_client(
                container=container_name, blob=blob_name
            )
            exist = await blob_client.exists()
            self.logger.debug(
                f"[COMPLETED] is_blob_exists, container_name: {container_name}, blob_name: {blob_name}, exist: {exist}"  # noqa E501
            )
            return exist

    async def list_blobs(
        self,
        container_name: str,
        name_starts_with: str | None = None,
    ) -> list[str]:
        """Return list of blob names in the storage account.

        :param container_name: Name of the container.
        :param name_starts_with: Optional. Filters the results to return only
            blobs whose names starts with this string"
        :return: List of blob names
        """
        self.logger.debug(f"[BEGIN] list_blobs, container_name: {container_name}")

        async with self.get_storage_client() as blob_storage_client:
            container_client = blob_storage_client.get_container_client(container_name)
            results: list[str] = []

            async for blob in container_client.list_blobs(
                name_starts_with=name_starts_with
            ):
                results.append(blob.name)

            self.logger.debug(
                f"[COMPLETED] list_blobs, container_name: {container_name}, count: {len(results)}"  # noqa E501
            )
            return results

    async def upload_blob(
        self, container_name: str, blob_name: str, content: str
    ) -> None:
        """Upload string content to a blob in the storage account.

        :param container_name: Name of the container.
        :param blob_name: Name of the blob.
        :param content: Content to upload.
        :return: Blob contents.
        """
        self.logger.debug(
            f"[BEGIN] upload_blob, container_name: {container_name}, blob_name: {blob_name}"  # noqa E501
        )

        async with self.get_storage_client() as blob_storage_client:
            blob_client = blob_storage_client.get_blob_client(
                container=container_name, blob=blob_name
            )

            await blob_client.upload_blob(data=content)

            self.logger.debug(
                f"[COMPLETED] upload_blob, container_name: {container_name}, blob_name: {blob_name}"  # noqa E501
            )

    async def download_blob(self, container_name: str, blob_name: str) -> bytes:
        """Return a blob from the storage account.

        :param container_name: Name of the container.
        :param blob_name: Name of the blob.
        :return: Blob contents.
        """
        self.logger.debug(
            f"[BEGIN] download_blob, container_name: {container_name}, blob_name: {blob_name}"  # noqa E501
        )

        async with self.get_storage_client() as blob_storage_client:
            blob_client = blob_storage_client.get_blob_client(
                container=container_name, blob=blob_name
            )

            # Download blob content as text directly and ensure complete consumption
            blob_data = await blob_client.download_blob()
            content = await blob_data.readall()

            self.logger.debug(
                f"[COMPLETED] download_blob, container_name: {container_name}, blob_name: {blob_name}"  # noqa E501
            )
            return content

    async def download_blob_as_str(self, container_name: str, blob_name: str) -> str:
        """Return a blob from the storage account.

        :param container_name: Name of the container.
        :param blob_name: Name of the blob.
        :return: Blob contents.
        """
        self.logger.debug(
            f"[BEGIN] download_blob_as_str, container_name: {container_name}, blob_name: {blob_name}"  # noqa E501
        )

        async with self.get_storage_client() as blob_storage_client:
            blob_client = blob_storage_client.get_blob_client(
                container=container_name, blob=blob_name
            )

            # Download blob content as text directly and ensure complete consumption
            blob_data = await blob_client.download_blob(encoding="UTF-8")
            content = await blob_data.readall()

            self.logger.debug(
                f"[COMPLETED] download_blob_as_str, container_name: {container_name}, blob_name: {blob_name}"  # noqa E501
            )
            return content
