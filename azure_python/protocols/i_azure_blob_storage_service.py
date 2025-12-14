from typing import Protocol


class IAzureBlobStorageService(Protocol):
    """Protocol for Azure Blob Storage Service."""

    async def is_blob_exists(self, container_name: str, blob_name: str) -> bool: ...

    async def list_blobs(
        self, container_name: str, name_starts_with: str | None = None
    ) -> list[str]:
        """
        Return a list all blob names within the given container.

        :param container_name: The name of the container.
        :param name_starts_with: The prefix to filter by.
        :return: A list of blob names.
        """
        ...

    async def upload_blob(
        self, container_name: str, blob_name: str, content: str
    ) -> None:
        """
        Upload a blob with the given content.

        :param container_name: The name of the container.
        :param blob_name: The name of the blob.
        :param content: The content of the blob.
        :return: None
        """
        ...

    async def download_blob(self, container_name: str, blob_name: str) -> bytes:
        """Return a blob from the storage account.

        :param container_name: Name of the container.
        :param blob_name: Name of the blob.
        :return: Blob contents.
        """
        ...

    async def download_blob_as_str(self, container_name: str, blob_name: str) -> str:
        """
        Return a blob content as a string.

        :param container_name: The name of the container.
        :param blob_name: The name of the blob.
        :return: The content of the blob.
        """
        ...
