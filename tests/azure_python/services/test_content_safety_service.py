from unittest.mock import AsyncMock, MagicMock

import pytest
from azure.ai.contentsafety.aio import ContentSafetyClient
from azure.ai.contentsafety.models import (
    AnalyzeTextResult,
    TextCategoriesAnalysis,
)
from azure.identity.aio import DefaultAzureCredential
from pytest_mock import MockerFixture

from azure_python.services.content_safety_service import ContentSafetyService


@pytest.fixture
def mock_content_safety_client(mocker: MockerFixture):
    mock_client = mocker.AsyncMock(spec=ContentSafetyClient)
    mock_client.analyze_text = AsyncMock(
        return_value=AnalyzeTextResult(
            categories_analysis=[
                TextCategoriesAnalysis(
                    category="Hate",
                    severity=2,
                )
            ]
        )
    )
    mock_client.close = AsyncMock()

    mocker.patch(
        "azure_python.services.content_safety_service.ContentSafetyClient",
        return_value=mock_client,
    )
    return mock_client


@pytest.mark.asyncio
@pytest.mark.parametrize("apikey", [None, "test"])
async def test_get_client(apikey: str | None, mocker: MockerFixture):
    mocker.patch(
        "azure_python.services.content_safety_service.ContentSafetyClient",
        return_value=mocker.AsyncMock(),
    )
    service = ContentSafetyService(
        env=MagicMock(content_safety_endpoint="test", content_safety_key=apikey),
        logger=mocker.MagicMock(),
    )

    async with service.get_client() as client:  # type: ignore
        assert client is not None


def test_collect_results():
    service = ContentSafetyService(
        env=MagicMock(content_safety_endpoint="test", content_safety_key="test"),
        logger=MagicMock(),
    )

    results = service.collect_results(
        MagicMock(
            categories_analysis=[
                TextCategoriesAnalysis(
                    category="Hate",
                    severity=2,
                ),
                TextCategoriesAnalysis(
                    category="Sexual",
                    severity=0,
                ),
            ]
        )
    )

    assert len(results) == 2
    assert results[0]["category"] == "Hate"
    assert results[0]["severity"] == 2
    assert results[1]["category"] == "Sexual"
    assert results[1]["severity"] == 0


@pytest.mark.asyncio
async def test_analyze_text(
    mock_content_safety_client: AsyncMock,
    mocker: MockerFixture,
) -> None:
    service = ContentSafetyService(
        env=MagicMock(content_safety_endpoint="test", content_safety_key="test"),
        logger=mocker.MagicMock(),
    )

    results = await service.analyze_text("test text")

    assert len(results) == 1
    assert results[0]["category"] == "Hate"
    assert results[0]["severity"] == 2

    # Verify the mock was called correctly
    mock_content_safety_client.analyze_text.assert_called_once()
    call_args = mock_content_safety_client.analyze_text.call_args[0][0]
    assert call_args.text == "test text"

    # Verify client was properly closed
    mock_content_safety_client.close.assert_called_once()


@pytest.mark.asyncio
async def test_analyze_text_client_close_exception(
    mock_content_safety_client: AsyncMock,
    mocker: MockerFixture,
) -> None:
    mock_content_safety_client.close.side_effect = Exception("Close error")

    mock_logger = mocker.MagicMock()

    service = ContentSafetyService(
        env=MagicMock(content_safety_endpoint="test", content_safety_key="test"),
        logger=mock_logger,
    )

    results = await service.analyze_text("test text")

    assert len(results) == 1
    assert results[0]["category"] == "Hate"
    assert results[0]["severity"] == 2

    # Verify the mock was called correctly
    mock_content_safety_client.analyze_text.assert_called_once()
    call_args = mock_content_safety_client.analyze_text.call_args[0][0]
    assert call_args.text == "test text"

    # Verify client close exception was logged
    mock_logger.warning.assert_called_once_with(
        "Error closing blob client: Close error"
    )


@pytest.mark.asyncio
async def test_analyze_text_credential_close_exception(
    mock_content_safety_client: AsyncMock,
    mocker: MockerFixture,
) -> None:
    mock_credential = mocker.AsyncMock(spec=DefaultAzureCredential)
    mock_credential.close.side_effect = Exception("Close error")

    mocker.patch(
        "azure_python.services.content_safety_service.DefaultAzureCredential",
        return_value=mock_credential,
    )

    mock_logger = mocker.MagicMock()

    service = ContentSafetyService(
        env=MagicMock(content_safety_endpoint="test", content_safety_key=None),
        logger=mock_logger,
    )

    await service.analyze_text("test text")

    mock_logger.warning.assert_called_once_with("Error closing credential: Close error")
