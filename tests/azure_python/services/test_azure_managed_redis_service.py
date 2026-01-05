from unittest.mock import AsyncMock, MagicMock

import pytest
from pytest_mock import MockerFixture

from azure_python.services.azure_managed_redis_service import (
    AzureManagedRedisService,
    AzureManagedRedisServiceEnv,
)


@pytest.fixture
def azure_managed_redis_service(mocker: MockerFixture) -> AzureManagedRedisService:
    mocker.patch("azure_python.services.azure_managed_redis_service.Redis")
    mocker.patch(
        "azure_python.services.azure_managed_redis_service.create_from_default_azure_credential"
    )
    svc = AzureManagedRedisService(
        env=AzureManagedRedisServiceEnv(
            redis_host="test.redis.cache.windows.net",
        ),
        logger=MagicMock(),
    )
    svc.client = MagicMock(
        ping=AsyncMock(return_value=True),
        set=AsyncMock(),
        get=AsyncMock(return_value="test_value"),
    )
    return svc


def test_azure_managed_redis_service_get_client(
    mocker: MockerFixture,
) -> None:
    mock_redis = mocker.patch("azure_python.services.azure_managed_redis_service.Redis")
    mock_fn_auth = mocker.patch(
        "azure_python.services.azure_managed_redis_service.create_from_default_azure_credential"
    )
    svc = AzureManagedRedisService(env=MagicMock(), logger=MagicMock())

    mock_redis.assert_called_once()
    mock_fn_auth.assert_called_once()
    assert svc.client is not None


@pytest.mark.asyncio
async def test_azure_managed_redis_service_set(
    azure_managed_redis_service: AzureManagedRedisService,
) -> None:
    svc = azure_managed_redis_service

    await svc.set("test_key", "test_value")
    svc.client.set.assert_called_once_with(name="test_key", value="test_value")  # type: ignore


@pytest.mark.asyncio
async def test_azure_managed_redis_service_get(
    azure_managed_redis_service: AzureManagedRedisService,
) -> None:
    svc = azure_managed_redis_service

    value = await svc.get("test_key")
    svc.client.get.assert_called_once_with(name="test_key")  # type: ignore
    assert value == "test_value"


@pytest.mark.asyncio
async def test_azure_managed_redis_service_ping(
    azure_managed_redis_service: AzureManagedRedisService,
) -> None:
    svc = azure_managed_redis_service

    result = await svc.ping()
    svc.client.ping.assert_called_once()  # type: ignore
    assert result is True
