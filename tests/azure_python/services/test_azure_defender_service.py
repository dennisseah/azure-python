from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from azure_python.services.azure_defender_service import AzureDefenderService


class MockResponse:
    def __init__(self):
        self.status = 200

    async def json(self):
        return {"value": [{"id": "test_id", "name": "test_name", "type": "test_type"}]}

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


@pytest.mark.asyncio
async def test_get_compliance_results(mocker: MockerFixture):
    mock_def_cred = MagicMock()
    mock_token = MagicMock()
    mock_token.token = "test"
    mock_def_cred.get_token.return_value = mock_token

    mock_def_azure_cred = mocker.patch(
        "azure_python.services.azure_defender_service.DefaultAzureCredential",
        return_value=mock_def_cred,
    )

    resp = MockResponse()
    mocker.patch("aiohttp.ClientSession.get", return_value=resp)

    service = AzureDefenderService(logger=MagicMock())
    result = await service.get_compliance_results("test")

    assert service is not None
    mock_def_azure_cred.assert_called_once()
    assert len(result) == 1
