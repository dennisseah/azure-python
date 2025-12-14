from unittest.mock import AsyncMock, MagicMock

import pytest
from azure.core.exceptions import HttpResponseError
from pytest_mock import MockerFixture

from azure_python.services.adversarial_simulation_service import (
    AdversarialSimulationService,
    AdversarialSimulationServiceEnv,
)


@pytest.fixture
def service(mocker: MockerFixture) -> AdversarialSimulationService:
    proj = "https://thefoundry.services.ai.azure.com/api/projects/theproject"
    env = AdversarialSimulationServiceEnv(
        azure_ai_foundry_project=proj,
    )

    return_value = AsyncMock(
        return_value=[
            {
                "template_parameters": {"category": "test"},
                "messages": [
                    {"content": "System prompt", "role": "system"},
                    {"content": "Test query", "role": "user"},
                ],
            }
        ]
    )

    mocker.patch(
        "azure_python.services.adversarial_simulation_service.DefaultAzureCredential",
        return_value=MagicMock(),
    )

    for svc in ["AdversarialSimulator", "DirectAttackSimulator"]:
        mocker.patch(
            f"azure_python.services.adversarial_simulation_service.{svc}",
            return_value=return_value,
        )
    mocker.patch(
        "azure_python.services.adversarial_simulation_service.IndirectAttackSimulator",
        return_value=AsyncMock(side_effect=HttpResponseError("Test error")),
    )

    return AdversarialSimulationService(env=env, logger=MagicMock())


@pytest.mark.asyncio
async def test_callback(service: AdversarialSimulationService):
    call_endpoint = AsyncMock(return_value=None)
    service.call_endpoint = call_endpoint

    result = await service.callback(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Test query",
                }
            ],
        }
    )

    assert len(result["messages"]) == 2
    assert result["messages"][1]["role"] == "assistant"
    assert result["messages"][1]["content"] is None


@pytest.mark.asyncio
async def test_callback_err(service: AdversarialSimulationService):
    call_endpoint = AsyncMock(side_effect=Exception("Test exception"))
    service.call_endpoint = call_endpoint

    result = await service.callback(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Test query",
                }
            ],
        }
    )

    assert len(result["messages"]) == 2
    assert result["messages"][1]["role"] == "assistant"
    assert result["messages"][1]["content"] == "Test exception"


@pytest.mark.asyncio
async def test_execute(service: AdversarialSimulationService, mocker: MockerFixture):
    call_endpoint = AsyncMock(
        return_value=MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(content="Test response"), finish_reason="stop"
                )
            ],
            usage=None,
        )
    )

    service.callback = AsyncMock()
    result = await service.execute(call_endpoint=call_endpoint, hits=1)

    # (2 x 5 scenarios) and 1 (error
    # AdversarialScenarioJailbreak.ADVERSARIAL_INDIRECT_JAILBREAK)
    assert len(result) == 8
    assert result[0].category == "test"
    assert result[0].query == "System prompt"
    assert result[0].response == "Test query"
