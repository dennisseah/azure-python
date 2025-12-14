from contextlib import asynccontextmanager
from logging import Logger
from typing import Any, AsyncGenerator, AsyncIterator, Dict
from unittest.mock import AsyncMock, MagicMock

import pytest
from azure.cosmos.aio import ContainerProxy, CosmosClient, DatabaseProxy
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from pytest_mock import MockerFixture

from azure_python.services.azure_cosmos_service import (
    AzureCosmosService,
    AzureCosmosServiceEnv,
)


async def async_database_generator() -> AsyncGenerator[Dict[str, Any], None]:
    strings = ["mock_db1", "mock_db2", "mock_db3"]
    for string in strings:
        yield {"id": string}


async def async_container_generator() -> AsyncGenerator[Dict[str, Any], None]:
    strings = ["mock_container1", "mock_container2", "mock_container3"]
    for string in strings:
        yield {"id": string}


async def async_item_generator() -> AsyncGenerator[Dict[str, Any], None]:
    strings = ["foo", "bar"]
    for string in strings:
        yield {"id": string}


@pytest.fixture
def mock_env() -> AzureCosmosServiceEnv:
    return AzureCosmosServiceEnv(
        azure_cosmos_host="mock_host", azure_cosmos_key="mock_key"
    )


@pytest.mark.asyncio
async def testget_cosmos_client(mocker: MockerFixture, mock_env: AzureCosmosServiceEnv):
    service = AzureCosmosService(env=mock_env, logger=MagicMock(Logger))
    mocker.patch(
        "azure_python.services.azure_cosmos_service.CosmosClient",
        return_value=AsyncMock(),
    )
    async with service.get_cosmos_client() as client:  # type: ignore
        assert client is not None


@pytest.fixture
@asynccontextmanager
async def mock_cosmos_client(mocker: MockerFixture) -> AsyncIterator[MockerFixture]:
    mock_cosmos_client = mocker.MagicMock(spec=CosmosClient)
    mock_database_client = mocker.MagicMock(spec=DatabaseProxy)
    mock_container_client = mocker.MagicMock(spec=ContainerProxy)

    mock_cosmos_client.get_database_client.return_value = mock_database_client
    mock_database_client.get_container_client.return_value = mock_container_client

    async with mock_cosmos_client:
        mock_cosmos_client.list_databases.return_value = async_database_generator()
        mock_database_client.list_containers.return_value = async_container_generator()
        mock_database_client.create_container.return_value = None
        mock_database_client.delete_container.return_value = None
        mock_container_client.query_items.return_value = async_item_generator()
        mock_container_client.create_item.return_value = {"id": "mock_item"}
        mock_container_client.upsert_item.return_value = {"id": "mock_item"}
        yield mock_cosmos_client


@pytest.fixture
@asynccontextmanager
async def mock_cosmos_client_del_not_found(
    mocker: MockerFixture,
) -> AsyncIterator[MockerFixture]:
    mock_cosmos_client = mocker.MagicMock(spec=CosmosClient)
    mock_database_client = mocker.MagicMock(spec=DatabaseProxy)

    mock_cosmos_client.get_database_client.return_value = mock_database_client

    async with mock_cosmos_client:
        mock_cosmos_client.list_databases.return_value = async_database_generator()
        mock_database_client.delete_container.side_effect = CosmosResourceNotFoundError
        yield mock_cosmos_client


def test_cosmos_service_init(
    mock_env: AzureCosmosServiceEnv, mocker: MockerFixture
) -> None:
    service = AzureCosmosService(env=mock_env, logger=mocker.MagicMock(Logger))

    assert service.env == mock_env
    assert hasattr(service, "list_databases") and callable(service.list_databases)
    assert hasattr(service, "list_containers") and callable(service.list_containers)
    assert hasattr(service, "list_items") and callable(service.list_items)
    assert hasattr(service, "query") and callable(service.query)


@pytest.mark.asyncio
async def test_cosmos_service_list_databases(
    mock_env: AzureCosmosServiceEnv,
    mocker: MockerFixture,
    mock_cosmos_client: MagicMock,
) -> None:
    service = AzureCosmosService(env=mock_env, logger=mocker.MagicMock(Logger))
    mocker.patch.object(
        AzureCosmosService, "get_cosmos_client", return_value=mock_cosmos_client
    )
    databases = await service.list_databases()

    assert databases == ["mock_db1", "mock_db2", "mock_db3"]


@pytest.mark.asyncio
async def test_cosmos_service_list_containers(
    mock_env: AzureCosmosServiceEnv,
    mocker: MockerFixture,
    mock_cosmos_client: MagicMock,
) -> None:
    service = AzureCosmosService(env=mock_env, logger=mocker.MagicMock(Logger))
    mocker.patch.object(
        AzureCosmosService, "get_cosmos_client", return_value=mock_cosmos_client
    )
    containers = await service.list_containers("mock_db1")

    assert containers == ["mock_container1", "mock_container2", "mock_container3"]


@pytest.mark.asyncio
async def test_cosmos_service_create_container(
    mock_env: AzureCosmosServiceEnv,
    mocker: MockerFixture,
    mock_cosmos_client: MagicMock,
) -> None:
    service = AzureCosmosService(env=mock_env, logger=mocker.MagicMock(Logger))
    mocker.patch.object(
        AzureCosmosService, "get_cosmos_client", return_value=mock_cosmos_client
    )
    await service.create_container("mock_db1", "mock_container1")


@pytest.mark.asyncio
async def test_cosmos_service_delete_container(
    mock_env: AzureCosmosServiceEnv,
    mocker: MockerFixture,
    mock_cosmos_client: MagicMock,
) -> None:
    service = AzureCosmosService(env=mock_env, logger=mocker.MagicMock(Logger))
    mocker.patch.object(
        AzureCosmosService, "get_cosmos_client", return_value=mock_cosmos_client
    )
    await service.delete_container("mock_db1", "mock_container1")


@pytest.mark.asyncio
async def test_cosmos_service_delete_container_not_found(
    mock_env: AzureCosmosServiceEnv,
    mocker: MockerFixture,
    mock_cosmos_client_del_not_found: MagicMock,
) -> None:
    service = AzureCosmosService(env=mock_env, logger=mocker.MagicMock(Logger))
    mocker.patch.object(
        AzureCosmosService,
        "get_cosmos_client",
        return_value=mock_cosmos_client_del_not_found,
    )
    # not found error should be caught and logged
    await service.delete_container("mock_db1", "mock_container1")


@pytest.mark.asyncio
async def test_cosmos_service_list_items(
    mock_env: AzureCosmosServiceEnv,
    mocker: MockerFixture,
    mock_cosmos_client: MagicMock,
) -> None:
    service = AzureCosmosService(env=mock_env, logger=mocker.MagicMock(Logger))
    mocker.patch.object(
        AzureCosmosService, "get_cosmos_client", return_value=mock_cosmos_client
    )
    items = await service.list_items("mock_db1", "mock_container1")

    assert items == [{"id": "foo"}, {"id": "bar"}]


@pytest.mark.asyncio
async def test_cosmos_service_query(
    mock_env: AzureCosmosServiceEnv,
    mocker: MockerFixture,
    mock_cosmos_client: MagicMock,
) -> None:
    service = AzureCosmosService(env=mock_env, logger=mocker.MagicMock(Logger))
    mocker.patch.object(
        AzureCosmosService, "get_cosmos_client", return_value=mock_cosmos_client
    )
    items = await service.query("mock_db1", "mock_container1", "SELECT * FROM c")

    assert items == [{"id": "foo"}, {"id": "bar"}]


@pytest.mark.asyncio
async def test_cosmos_service_create_item(
    mock_env: AzureCosmosServiceEnv,
    mocker: MockerFixture,
    mock_cosmos_client: MagicMock,
) -> None:
    service = AzureCosmosService(env=mock_env, logger=mocker.MagicMock(Logger))
    mocker.patch.object(
        AzureCosmosService, "get_cosmos_client", return_value=mock_cosmos_client
    )
    results = await service.create_item(
        "mock_db1", "mock_container1", {"id": "mock_item"}
    )

    assert results == {"id": "mock_item"}


@pytest.mark.asyncio
async def test_cosmos_service_create_items(
    mock_env: AzureCosmosServiceEnv,
    mocker: MockerFixture,
    mock_cosmos_client: MagicMock,
) -> None:
    service = AzureCosmosService(env=mock_env, logger=mocker.MagicMock(Logger))
    fn = mocker.patch.object(
        AzureCosmosService, "get_cosmos_client", return_value=mock_cosmos_client
    )
    await service.create_items(
        "mock_db1", "mock_container1", [{"id0": "mock_item0"}, {"id1": "mock_item1"}]
    )

    assert fn.call_count == 1


@pytest.mark.asyncio
async def test_cosmos_service_update_item(
    mock_env: AzureCosmosServiceEnv,
    mocker: MockerFixture,
    mock_cosmos_client: MagicMock,
):
    service = AzureCosmosService(env=mock_env, logger=mocker.MagicMock(Logger))
    mocker.patch.object(
        AzureCosmosService, "get_cosmos_client", return_value=mock_cosmos_client
    )
    results = await service.update_item(
        "mock_db1", "mock_container1", {"id": "mock_item"}
    )

    assert results == {"id": "mock_item"}
