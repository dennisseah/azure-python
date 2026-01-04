from contextlib import asynccontextmanager
from typing import AsyncIterator
from unittest.mock import AsyncMock, MagicMock

import pytest
from azure.keyvault.secrets.aio import SecretClient
from pytest_mock import MockerFixture

from azure_python.services.azure_keyvault_service import (
    AzureKeyVaultService,
    AzureKeyVaultServiceEnv,
)


@pytest.fixture
def mock_env() -> AzureKeyVaultServiceEnv:
    return AzureKeyVaultServiceEnv(
        azure_key_vault_url="https://mock-vault.vault.azure.net/"
    )


@pytest.mark.asyncio
async def test_get_cosmos_client(
    mocker: MockerFixture, mock_env: AzureKeyVaultServiceEnv
):
    service = AzureKeyVaultService(env=mock_env)
    mocker.patch(
        "azure_python.services.azure_cosmos_service.CosmosClient",
        return_value=AsyncMock(),
    )
    async with service.get_client() as client:  # type: ignore
        assert client is not None


@pytest.fixture
@asynccontextmanager
async def mock_client(mocker: MockerFixture) -> AsyncIterator[MockerFixture]:
    mock_client = mocker.MagicMock(spec=SecretClient)

    async with mock_client:
        mock_client.get_secret = AsyncMock(
            return_value=MagicMock(value="mock_secret_value")
        )
        mock_client.set_secret = AsyncMock(return_value=None)
        yield mock_client


@pytest.mark.asyncio
async def test_get_secret(
    mock_env: AzureKeyVaultServiceEnv,
    mocker: MockerFixture,
    mock_client: MagicMock,
) -> None:
    service = AzureKeyVaultService(env=mock_env)
    mocker.patch.object(AzureKeyVaultService, "get_client", return_value=mock_client)
    secret = await service.get_secret("test_secret")

    assert secret == "mock_secret_value"


@pytest.mark.asyncio
async def test_set_secret(
    mock_env: AzureKeyVaultServiceEnv,
    mocker: MockerFixture,
    mock_client: MagicMock,
) -> None:
    service = AzureKeyVaultService(env=mock_env)
    mocker.patch.object(AzureKeyVaultService, "get_client", return_value=mock_client)
    status = await service.set_secret("test_secret", "mock_secret_value")
    assert status is True
