from typing import Callable
from unittest.mock import AsyncMock, MagicMock

import pytest
from azure.ai.textanalytics._models import CategorizedEntity, RecognizeEntitiesResult
from pytest_mock import MockerFixture

from azure_python.services.azure_text_analytics_service import (
    AzureTextAnalyticsService,
    AzureTextAnalyticsServiceEnv,
)


@pytest.fixture
def mock_env() -> Callable[[bool], AzureTextAnalyticsServiceEnv]:
    def wrapper(has_key: bool) -> AzureTextAnalyticsServiceEnv:
        return AzureTextAnalyticsServiceEnv(
            azure_cog_service_endpoint="https://fake-endpoint.com",
            azure_cog_service_key="fake-key" if has_key else None,
        )

    return wrapper


@pytest.fixture
def mock_service(mock_env) -> Callable[[bool], AzureTextAnalyticsService]:
    def wrapper(has_key: bool) -> AzureTextAnalyticsService:
        return AzureTextAnalyticsService(env=mock_env(has_key), logger=MagicMock())

    return wrapper


def test_text_extraction_service_key(
    mock_service: Callable[[bool], AzureTextAnalyticsService], mocker: MockerFixture
):
    mocker.patch("azure.ai.textanalytics.TextAnalyticsClient")
    assert mock_service(True).get_client() is not None


def test_text_extraction_service_without_key(
    mock_service: Callable[[bool], AzureTextAnalyticsService], mocker: MockerFixture
):
    mocker.patch("azure.ai.textanalytics.TextAnalyticsClient")
    assert mock_service(False).get_client() is not None


@pytest.mark.asyncio
async def test_recognize_entities_no_content(
    mock_service: Callable[[bool], AzureTextAnalyticsService],
):
    service = mock_service(True)
    assert await service.recognize_entities([]) == []


@pytest.mark.asyncio
async def test_recognize_entities(
    mock_service: Callable[[bool], AzureTextAnalyticsService],
):
    service = mock_service(True)
    mock_client = MagicMock()
    mock_client.recognize_entities = AsyncMock(
        return_value=[
            RecognizeEntitiesResult(
                id="0",
                entities=[
                    CategorizedEntity(
                        text="Studies",
                        category="Event",
                        subcategory="Event",
                        offset=0,
                        length=7,
                        confidence_score=0.99,
                    )
                ],
            ),
            RecognizeEntitiesResult(
                id="1",
                entities=[
                    CategorizedEntity(
                        text="test",
                        category="Event",
                        subcategory="Event",
                        offset=10,
                        length=4,
                        confidence_score=0.9,
                    )
                ],
            ),
        ]
    )
    service.get_client = MagicMock(return_value=mock_client)

    input = [
        "Studies have shown that regular physical activity is "
        "associated with a longer lifespan, reducing the risk",
        "This is a test",
    ]
    results = await service.recognize_entities(input)

    assert len(results) == 2
    assert results[0].id == "0"
    assert results[0].entities[0].text == "Studies"
    assert results[0].entities[0].sentence == input[0]
    assert results[1].id == "1"
    assert results[1].entities[0].text == "test"
    assert results[1].entities[0].sentence == input[1]
