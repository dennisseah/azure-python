from contextlib import asynccontextmanager
from typing import AsyncIterator, Callable
from unittest.mock import AsyncMock, MagicMock

import pytest
from azure.ai.inference import EmbeddingsClient
from azure.ai.inference.models import EmbeddingsResult
from pytest_mock import MockerFixture

from azure_python.services.embedding_service import (
    EmbeddingService,
    EmbeddingServiceEnv,
)


@pytest.fixture
def mock_env() -> Callable:
    def wrapper(with_key: bool) -> EmbeddingServiceEnv:
        return EmbeddingServiceEnv(
            embedding_endpoint="mock_endpoint",
            embedding_model="mock_model",
            embedding_credential="mock_credential" if with_key else None,
        )

    return wrapper


@pytest.mark.asyncio
@pytest.mark.parametrize("with_key", [True, False])
async def test_get_client(with_key, mocker: MockerFixture, mock_env: Callable):
    service = EmbeddingService(env=mock_env(with_key), logger=MagicMock())

    mocker.patch(
        "azure_python.services.embedding_service.EmbeddingsClient",
        return_value=AsyncMock(),
    )

    async with service.get_client() as client:  # type: ignore
        assert client is not None


@pytest.fixture
@asynccontextmanager
async def mock_embedding_client() -> AsyncIterator[MockerFixture]:
    mock_emb_client = MagicMock(spec=EmbeddingsClient)
    result = MagicMock(spec=EmbeddingsResult)
    result.data = [
        MagicMock(embedding=[0.1, 0.2, 0.3]),
        MagicMock(embedding=[0.4, 0.5, 0.6]),
    ]
    mock_emb_client.embed = AsyncMock(return_value=result)
    yield mock_emb_client


@pytest.fixture
def embedding_service(
    mock_embedding_client: MagicMock, mocker: MockerFixture
) -> EmbeddingService:
    service = EmbeddingService(env=MagicMock(), logger=MagicMock())
    mocker.patch.object(
        EmbeddingService, "get_client", return_value=mock_embedding_client
    )
    return service


@pytest.mark.asyncio
async def test_get_embeddings(embedding_service: EmbeddingService) -> None:
    texts = ["Hello, world!", "Testing embeddings."]

    embeddings_result = await embedding_service.get_embeddings(texts)

    assert embeddings_result is not None
    assert len(embeddings_result.data) == 2
