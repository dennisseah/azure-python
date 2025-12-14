from dataclasses import dataclass
from logging import Logger
from typing import Any, Awaitable, Callable, TypedDict

from azure.ai.evaluation.simulator import (
    AdversarialScenario,
    AdversarialScenarioJailbreak,
    AdversarialSimulator,
    DirectAttackSimulator,
    IndirectAttackSimulator,
)
from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from lagom.environment import Env

from azure_python.models.adversarial_simulation_service_result import (
    AdversarialSimulationServiceResult,
)
from azure_python.protocols.i_adversarial_simulation_service import (
    IAdversarialSimulationService,
)


class AdversarialSimulationServiceEnv(Env):
    azure_ai_foundry_project: str


class Simulators(TypedDict):
    name: str
    simulator: Any
    scenario: list[AdversarialScenario] | list[AdversarialScenarioJailbreak]


scenarios = [
    AdversarialScenario.ADVERSARIAL_QA,
    AdversarialScenario.ADVERSARIAL_CONTENT_PROTECTED_MATERIAL,
    AdversarialScenario.ADVERSARIAL_REWRITE,
    AdversarialScenario.ADVERSARIAL_CONVERSATION,
]


@dataclass
class AdversarialSimulationService(IAdversarialSimulationService):
    """
    Adversarial Simulation Service using Azure AI Foundry.
    """

    env: AdversarialSimulationServiceEnv
    logger: Logger

    def __post_init__(self):
        self.simulators: list[Simulators] = [
            {
                "name": "AdversarialSimulator",
                "simulator": AdversarialSimulator,
                "scenario": scenarios,
            },
            {
                "name": "DirectAttackSimulator",
                "simulator": DirectAttackSimulator,
                "scenario": scenarios,
            },
            {
                "name": "IndirectAttackSimulator",
                "simulator": IndirectAttackSimulator,
                "scenario": [
                    AdversarialScenarioJailbreak.ADVERSARIAL_INDIRECT_JAILBREAK
                ],
            },
        ]

    async def callback(
        self,
        messages: Any,
        stream: bool = False,
        session_state: Any = None,  # noqa: ANN401
        context: dict[str, Any] | None = None,
    ) -> dict:
        messages_list = messages["messages"]
        query = messages_list[-1]["content"]
        try:
            response = await self.call_endpoint(query)
            formatted_response = {
                "content": response,
                "role": "assistant",
            }
        except Exception as ex:
            formatted_response = {"content": str(ex), "role": "assistant"}

        messages["messages"].append(formatted_response)
        return {
            "messages": messages_list,
            "stream": stream,
            "session_state": session_state,
            "context": context,
        }

    async def execute(
        self, call_endpoint: Callable[[str], Awaitable[str | None]], hits: int = 3
    ) -> list[AdversarialSimulationServiceResult]:
        self.call_endpoint = call_endpoint
        outputs = []

        for simulator in self.simulators:
            sim = simulator["simulator"](
                credential=DefaultAzureCredential(),
                azure_ai_project=self.env.azure_ai_foundry_project,
            )

            for scenario in simulator["scenario"]:
                try:
                    res = await sim(
                        scenario=scenario,
                        max_conversation_turns=1,
                        max_simulation_results=hits,
                        target=self.callback,
                    )
                    outputs += [
                        AdversarialSimulationServiceResult.parse(simulator["name"], o)
                        for o in res
                    ]
                except HttpResponseError as e:
                    # not supported scenario for the region
                    self.logger.error(f"Error occurred for scenario {scenario}: {e}")

        return outputs
