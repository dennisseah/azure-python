import asyncio
from dataclasses import dataclass

from azure_python.hosting import container
from samples.utils import set_log_level


@dataclass
class Endpoint:
    def __post_init__(self):
        from azure_python.protocols.i_azure_openai_service import (
            IAzureOpenAIService,
        )

        self.openai_service = container[IAzureOpenAIService]

    async def call_endpoint(self, query: str) -> str | None:
        try:
            result = await self.openai_service.chat_completion(
                messages=[
                    {"role": "user", "content": query},
                ],
            )
            return result.content
        except Exception:
            return None


async def main() -> None:
    from azure_python.protocols.i_adversarial_simulation_service import (
        IAdversarialSimulationService,
    )

    svc = container[IAdversarialSimulationService]
    endpoint = Endpoint()
    await svc.execute(endpoint.call_endpoint)


if __name__ == "__main__":
    set_log_level("INFO")
    asyncio.run(main())
