from typing import Awaitable, Callable, Protocol

from azure_python.models.adversarial_simulation_service_result import (
    AdversarialSimulationServiceResult,
)


class IAdversarialSimulationService(Protocol):
    """Using Azure AI Foundry to run adversarial simulations.

    This is a form of security testing where inputs are crafted to
    intentionally provoke incorrect or unexpected behavior from AI models.
    The service simulates various adversarial scenarios to evaluate the
    robustness and security of AI systems.
    """

    async def execute(
        self, call_endpoint: Callable[[str], Awaitable[str | None]], hits: int = 3
    ) -> list[AdversarialSimulationServiceResult]:
        """
        Execute the adversarial simulation for a given scenario.

        :param call_endpoint: A callable that takes a query string and returns a
        response string asynchronously.
        :param hits: The number of hits/attempts to perform.
        :return: A list of Result objects containing the query and response.
        """
        ...
