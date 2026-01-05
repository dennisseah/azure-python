from contextlib import asynccontextmanager
from logging import Logger
from typing import AsyncIterator
from unittest.mock import AsyncMock, MagicMock

import pytest
from azure.data.tables.aio import TableServiceClient
from azure.identity.aio import DefaultAzureCredential
from pytest_mock import MockerFixture

from azure_python.services.azure_table_storage_service import (
    AzureTableStorageService,
    AzureTableStorageServiceEnv,
)


@pytest.fixture
def mock_env() -> AzureTableStorageServiceEnv:
    return AzureTableStorageServiceEnv(
        azure_table_storage_url="https://mock-table.table.core.windows.net/"
    )


@pytest.mark.asyncio
async def test_get_client(mocker: MockerFixture, mock_env: AzureTableStorageServiceEnv):
    service = AzureTableStorageService(env=mock_env, logger=MagicMock())
    mocker.patch(
        "azure_python.services.azure_table_storage_service.TableServiceClient",
        return_value=AsyncMock(),
    )
    async with service.get_client() as client:  # type: ignore
        assert client is not None


@pytest.mark.asyncio
async def test_get_client_err(mocker: MockerFixture):
    mock_client = mocker.AsyncMock()
    mock_logger = MagicMock(spec=Logger)
    mock_logger.warning = MagicMock()

    mocker.patch(
        "azure_python.services.azure_table_storage_service.TableServiceClient",
        return_value=mock_client,
    )
    mock_client.close.side_effect = Exception("Close error")

    service = AzureTableStorageService(logger=mock_logger, env=MagicMock())
    async with service.get_client() as blob_storage_client:  # type: ignore
        assert blob_storage_client is not None
    mock_logger.warning.assert_called_once()


@pytest.mark.asyncio
async def test_get_cred_err(mocker: MockerFixture):
    mock_cred = mocker.AsyncMock(spec=DefaultAzureCredential)
    mock_cred.close.side_effect = Exception("Close error")
    mock_logger = MagicMock(spec=Logger)
    mock_logger.warning = MagicMock()

    mocker.patch(
        "azure_python.services.azure_table_storage_service.TableServiceClient",
        return_value=mocker.AsyncMock(),
    )
    mocker.patch(
        "azure_python.services.azure_table_storage_service.DefaultAzureCredential",
        return_value=mock_cred,
    )

    service = AzureTableStorageService(logger=mock_logger, env=MagicMock())

    async with service.get_client() as blob_storage_client:  # type: ignore
        assert blob_storage_client is not None
    mock_logger.warning.assert_called_once()


@pytest.fixture
@asynccontextmanager
async def mock_client(mocker: MockerFixture) -> AsyncIterator[MockerFixture]:
    mock_client = mocker.MagicMock(spec=TableServiceClient)
    mock_table_client = mocker.MagicMock(spec=TableServiceClient)
    mock_table_client.get_table_access_policy = AsyncMock()

    async with mock_client:
        mock_client.get_table_client = MagicMock(return_value=mock_table_client)
        yield mock_client


@pytest.fixture
@asynccontextmanager
async def mock_client_err(mocker: MockerFixture) -> AsyncIterator[MockerFixture]:
    mock_client = mocker.MagicMock(spec=TableServiceClient)
    mock_table_client = mocker.MagicMock(spec=TableServiceClient)
    mock_table_client.get_table_access_policy = AsyncMock(
        side_effect=Exception("Table not found")
    )

    async with mock_client:
        mock_client.get_table_client = MagicMock(return_value=mock_table_client)
        yield mock_client


@pytest.fixture
def service(
    mock_env: AzureTableStorageServiceEnv,
    mocker: MockerFixture,
    mock_client: MagicMock,
) -> AzureTableStorageService:
    service = AzureTableStorageService(env=mock_env, logger=MagicMock())
    mocker.patch.object(
        AzureTableStorageService, "get_client", return_value=mock_client
    )
    return service


@pytest.mark.asyncio
async def test_is_table_exist(
    service: AzureTableStorageService,
) -> None:
    exist = await service.is_table_exist("TestTable")
    assert exist is True


@pytest.mark.asyncio
async def test_is_table_exist_not(
    mock_env: AzureTableStorageServiceEnv,
    mocker: MockerFixture,
    mock_client_err: MagicMock,
) -> None:
    service = AzureTableStorageService(env=mock_env, logger=MagicMock())
    mocker.patch.object(
        AzureTableStorageService, "get_client", return_value=mock_client_err
    )
    exist = await service.is_table_exist("TestTable")
    assert not exist


@pytest.mark.asyncio
async def test_create_table(
    service: AzureTableStorageService,
) -> None:
    created = await service.create_table("NewTable")
    assert created is True


@pytest.mark.asyncio
async def test_delete_table(
    service: AzureTableStorageService,
) -> None:
    deleted = await service.delete_table("OldTable")
    assert deleted is True


@pytest.mark.asyncio
async def test_list_tables(
    service: AzureTableStorageService,
    mocker: MockerFixture,
) -> None:
    mock_table_names = ["Table1", "Table2", "Table3"]

    mock_tables = []
    for t in mock_table_names:
        mock_table = MagicMock()
        mock_table.name = t
        mock_tables.append(mock_table)

    async def async_table_generator():
        for table in mock_tables:
            yield table

    mock_client = MagicMock()
    mock_client.list_tables = lambda: async_table_generator()

    @asynccontextmanager
    async def mock_get_client():
        yield mock_client

    mocker.patch.object(service, "get_client", side_effect=mock_get_client)

    tables = await service.list_tables()
    assert tables == mock_table_names


@pytest.mark.asyncio
async def test_insert_entity(
    service: AzureTableStorageService, mocker: MockerFixture
) -> None:
    mock_table_client = AsyncMock()
    mock_table_client.create_entity = AsyncMock()

    mock_client = MagicMock()
    mock_client.get_table_client = MagicMock(return_value=mock_table_client)

    @asynccontextmanager
    async def mock_get_client():
        yield mock_client

    mocker.patch.object(service, "get_client", side_effect=mock_get_client)

    entity = {"PartitionKey": "part1", "RowKey": "row1", "Value": "test"}
    await service.insert_entity("TestTable", entity)

    mock_table_client.create_entity.assert_awaited_once_with(entity=entity)


@pytest.mark.asyncio
async def test_delete_entity(
    service: AzureTableStorageService, mocker: MockerFixture
) -> None:
    mock_table_client = AsyncMock()
    mock_table_client.delete_entity = AsyncMock()

    mock_client = MagicMock()
    mock_client.get_table_client = MagicMock(return_value=mock_table_client)

    @asynccontextmanager
    async def mock_get_client():
        yield mock_client

    mocker.patch.object(service, "get_client", side_effect=mock_get_client)

    await service.delete_entity("TestTable", "part1", "row1")

    mock_table_client.delete_entity.assert_awaited_once_with(
        partition_key="part1",
        row_key="row1",
    )


@pytest.mark.asyncio
async def test_get_entity(
    service: AzureTableStorageService, mocker: MockerFixture
) -> None:
    mock_entity = {"PartitionKey": "part1", "RowKey": "row1", "Value": "test"}

    mock_table_client = AsyncMock()
    mock_table_client.get_entity = AsyncMock(return_value=mock_entity)

    mock_client = MagicMock()
    mock_client.get_table_client = MagicMock(return_value=mock_table_client)

    @asynccontextmanager
    async def mock_get_client():
        yield mock_client

    mocker.patch.object(service, "get_client", side_effect=mock_get_client)

    entity = await service.get_entity("TestTable", "part1", "row1")

    mock_table_client.get_entity.assert_awaited_once_with(
        partition_key="part1", row_key="row1"
    )
    assert entity == mock_entity


@pytest.mark.asyncio
async def test_list_entities(
    service: AzureTableStorageService, mocker: MockerFixture
) -> None:
    mock_entities = [
        {"PartitionKey": "part1", "RowKey": "row1", "Value": "test1"},
        {"PartitionKey": "part1", "RowKey": "row2", "Value": "test2"},
    ]

    async def async_entity_generator():
        for entity in mock_entities:
            yield entity

    mock_table_client = MagicMock()
    mock_table_client.list_entities = lambda: async_entity_generator()

    mock_client = MagicMock()
    mock_client.get_table_client = MagicMock(return_value=mock_table_client)

    @asynccontextmanager
    async def mock_get_client():
        yield mock_client

    mocker.patch.object(service, "get_client", side_effect=mock_get_client)

    entities = await service.list_entities("TestTable")

    assert entities == mock_entities


@pytest.mark.asyncio
async def test_update_entity(
    service: AzureTableStorageService, mocker: MockerFixture
) -> None:
    mock_table_client = AsyncMock()
    mock_table_client.update_entity = AsyncMock()

    mock_client = MagicMock()
    mock_client.get_table_client = MagicMock(return_value=mock_table_client)

    @asynccontextmanager
    async def mock_get_client():
        yield mock_client

    mocker.patch.object(service, "get_client", side_effect=mock_get_client)

    entity = {"PartitionKey": "part1", "RowKey": "row1", "Value": "updated"}
    await service.update_entity("TestTable", entity)

    mock_table_client.update_entity.assert_awaited_once_with(entity=entity)


@pytest.mark.asyncio
async def test_upsert_entity(
    service: AzureTableStorageService, mocker: MockerFixture
) -> None:
    mock_table_client = AsyncMock()
    mock_table_client.upsert_entity = AsyncMock()

    mock_client = MagicMock()
    mock_client.get_table_client = MagicMock(return_value=mock_table_client)

    @asynccontextmanager
    async def mock_get_client():
        yield mock_client

    mocker.patch.object(service, "get_client", side_effect=mock_get_client)

    entity = {"PartitionKey": "part1", "RowKey": "row1", "Value": "upserted"}
    await service.upsert_entity("TestTable", entity)

    mock_table_client.upsert_entity.assert_awaited_once_with(entity=entity)


@pytest.mark.asyncio
async def test_query_entities(
    service: AzureTableStorageService, mocker: MockerFixture
) -> None:
    mock_entities = [
        {"PartitionKey": "part1", "RowKey": "row1", "Value": "test1"},
        {"PartitionKey": "part1", "RowKey": "row2", "Value": "test2"},
    ]

    async def async_entity_generator():
        for entity in mock_entities:
            yield entity

    mock_table_client = MagicMock()
    mock_table_client.query_entities = lambda query_filter: async_entity_generator()

    mock_client = MagicMock()
    mock_client.get_table_client = MagicMock(return_value=mock_table_client)

    @asynccontextmanager
    async def mock_get_client():
        yield mock_client

    mocker.patch.object(service, "get_client", side_effect=mock_get_client)

    filter_query = "PartitionKey eq 'part1'"
    entities = await service.query_entities("TestTable", filter_query)

    assert entities == mock_entities
