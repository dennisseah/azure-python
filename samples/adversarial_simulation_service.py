import asyncio

from azure_python.hosting import container
from azure_python.protocols.i_adversarial_simulation_service import (
    IAdversarialSimulationService,
)
from azure_python.protocols.i_azure_openai_service import IAzureOpenAIService


async def call_openai_endpoint(
    query: str,
) -> str | None:
    openai_service = container[IAzureOpenAIService]
    responses = await openai_service.chat_completion(
        messages=[{"role": "user", "content": query}],
    )

    if not responses or len(responses) == 0:
        return None

    return responses[0].content


async def main() -> None:
    attack = container[IAdversarialSimulationService]
    result = await attack.execute(call_openai_endpoint, hits=5)
    for res in result:
        print(f"Simulator: {res.simulator_name}")
        print(f"Category: {res.category}")
        print(f"Query: {res.query}")
        print(f"Response: {res.response}")
        print("-----")


if __name__ == "__main__":
    asyncio.run(main())
