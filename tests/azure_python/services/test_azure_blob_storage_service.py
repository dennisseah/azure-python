from contextlib import asynccontextmanager
from logging import Logger
from typing import AsyncGenerator, AsyncIterator
from unittest.mock import AsyncMock, MagicMock

import pytest
from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import (
    BlobClient,
    BlobServiceClient,
    ContainerClient,
    StorageStreamDownloader,
)
from pytest_mock import MockerFixture

from azure_python.services.azure_blob_storage_service import (
    AzureBlobStorageService,
)

azure_storage_url = "http://127.0.0.1:10000/devstoreaccount1"

mock_blob_exists = True
mock_blob_str = "hello world"
mock_files = ["file1", "file2", "file3"]


class MockBlob:
    name: str

    def __init__(self, name: str):
        self.name = name


async def async_file_generator() -> AsyncGenerator[MockBlob, None]:
    for file_name in mock_files:
        yield MockBlob(file_name)


@pytest.fixture
@asynccontextmanager
async def mock_blob_service_client(
    mocker: MockerFixture,
) -> AsyncIterator[MockerFixture]:
    mock_blob_service_client = mocker.AsyncMock(spec=BlobServiceClient)
    mock_blob_client = mocker.AsyncMock(spec=BlobClient)
    mock_container_client = mocker.AsyncMock(spec=ContainerClient)
    mock_storage_stream_downloader = mocker.AsyncMock(spec=StorageStreamDownloader)

    mock_blob_client.download_blob.return_value = mock_storage_stream_downloader
    mock_blob_client.upload_blob.return_value = None

    mock_blob_service_client.get_blob_client.return_value = mock_blob_client
    mock_blob_service_client.get_container_client.return_value = mock_container_client
    mock_blob_service_client.close = mocker.AsyncMock()

    async with mock_blob_service_client:
        mock_blob_client.exists.return_value = mock_blob_exists
        mock_container_client.list_blobs.return_value = async_file_generator()
        mock_storage_stream_downloader.readall.return_value = mock_blob_str
        yield mock_blob_service_client


def test_azure_blob_storage_service_init(mocker: MockerFixture) -> None:
    mock_logger = mocker.MagicMock()
    service = AzureBlobStorageService(logger=mock_logger, env=MagicMock())

    assert hasattr(service, "is_blob_exists") and callable(service.is_blob_exists)
    assert hasattr(service, "list_blobs") and callable(service.list_blobs)
    assert hasattr(service, "download_blob_as_str") and callable(
        service.download_blob_as_str
    )


@pytest.mark.asyncio
async def test_get_storage_client(mocker: MockerFixture):
    mocker.patch(
        "azure_python.services.azure_blob_storage_service.BlobServiceClient",
        return_value=mocker.AsyncMock(),
    )
    service = AzureBlobStorageService(logger=mocker.MagicMock(), env=MagicMock())

    async with service.get_storage_client() as blob_storage_client:  # type: ignore
        assert blob_storage_client is not None


@pytest.mark.asyncio
async def test_get_storage_client_err(mocker: MockerFixture):
    mock_client = mocker.AsyncMock()
    mock_logger = MagicMock(spec=Logger)
    mock_logger.warning = MagicMock()

    mocker.patch(
        "azure_python.services.azure_blob_storage_service.BlobServiceClient",
        return_value=mock_client,
    )
    mock_client.close.side_effect = Exception("Close error")

    service = AzureBlobStorageService(logger=mock_logger, env=MagicMock())
    async with service.get_storage_client() as blob_storage_client:  # type: ignore
        assert blob_storage_client is not None
    mock_logger.warning.assert_called_once()


@pytest.mark.asyncio
async def test_get_storage_cred_err(mocker: MockerFixture):
    mock_cred = mocker.AsyncMock(spec=DefaultAzureCredential)
    mock_cred.close.side_effect = Exception("Close error")
    mock_logger = MagicMock(spec=Logger)
    mock_logger.warning = MagicMock()

    mocker.patch(
        "azure_python.services.azure_blob_storage_service.BlobServiceClient",
        return_value=mocker.AsyncMock(),
    )
    mocker.patch(
        "azure_python.services.azure_blob_storage_service.DefaultAzureCredential",
        return_value=mock_cred,
    )

    service = AzureBlobStorageService(logger=mock_logger, env=MagicMock())

    async with service.get_storage_client() as blob_storage_client:  # type: ignore
        assert blob_storage_client is not None
    mock_logger.warning.assert_called_once()


@pytest.mark.asyncio
async def test_blob_storage_service_is_blob_exists(
    mocker: MockerFixture,
    mock_blob_service_client: AsyncMock,
) -> None:
    service = AzureBlobStorageService(logger=mocker.MagicMock(Logger), env=MagicMock())

    mocker.patch.object(
        AzureBlobStorageService,
        "get_storage_client",
        return_value=mock_blob_service_client,
    )

    blob_exists = await service.is_blob_exists("test_container", "test_blob")
    assert blob_exists == mock_blob_exists


@pytest.mark.asyncio
async def test_blob_storage_list_blobs(
    mocker: MockerFixture,
    mock_blob_service_client: AsyncMock,
) -> None:
    service = AzureBlobStorageService(logger=mocker.MagicMock(Logger), env=MagicMock())

    mocker.patch.object(
        AzureBlobStorageService,
        "get_storage_client",
        return_value=mock_blob_service_client,
    )

    blobs = await service.list_blobs("test_container", name_starts_with="foo")
    assert blobs == ["file1", "file2", "file3"]


@pytest.mark.asyncio
async def test_blob_storage_download_blob_as_str(
    mocker: MockerFixture,
    mock_blob_service_client: AsyncMock,
) -> None:
    service = AzureBlobStorageService(logger=mocker.MagicMock(Logger), env=MagicMock())

    mocker.patch.object(
        AzureBlobStorageService,
        "get_storage_client",
        return_value=mock_blob_service_client,
    )

    blob_text = await service.download_blob_as_str(
        container_name="foo", blob_name="bar"
    )
    assert blob_text == mock_blob_str


@pytest.mark.asyncio
async def test_blob_storage_download_blob(
    mocker: MockerFixture,
    mock_blob_service_client: AsyncMock,
) -> None:
    service = AzureBlobStorageService(logger=mocker.MagicMock(Logger), env=MagicMock())

    mocker.patch.object(
        AzureBlobStorageService,
        "get_storage_client",
        return_value=mock_blob_service_client,
    )

    blob_text = await service.download_blob(container_name="foo", blob_name="bar")
    assert blob_text == mock_blob_str


@pytest.mark.asyncio
async def test_blob_storage_upload_blob(
    mocker: MockerFixture,
    mock_blob_service_client: AsyncMock,
) -> None:
    service = AzureBlobStorageService(logger=mocker.MagicMock(Logger), env=MagicMock())

    mocker.patch.object(
        AzureBlobStorageService,
        "get_storage_client",
        return_value=mock_blob_service_client,
    )

    await service.upload_blob(
        container_name="foo", blob_name="bar", content=mock_blob_str
    )
