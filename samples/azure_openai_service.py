import asyncio

from azure_python.hosting import container
from samples.utils import set_log_level


async def main() -> None:
    from azure_python.protocols.i_azure_openai_service import (
        IAzureOpenAIService,
    )

    svc = container[IAzureOpenAIService]
    responses = await svc.chat_completion(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "List 5 programming languages."},
        ],
        temperature=1,
    )

    print("Chat Completion Response:")
    print(responses.model_dump_json(indent=2))


if __name__ == "__main__":
    set_log_level("INFO")
    asyncio.run(main())
