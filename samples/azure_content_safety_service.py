import asyncio

from azure_python.hosting import container
from azure_python.protocols.i_content_safety_service import IContentSafetyService

svc = container[IContentSafetyService]


async def main() -> None:
    text_to_analyze = "She is a bad ass."
    analysis_results = await svc.analyze_text(text_to_analyze)

    print("Content Safety Analysis Results:")
    for result in analysis_results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
