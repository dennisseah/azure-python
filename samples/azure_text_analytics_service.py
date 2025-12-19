import asyncio
import json
import os

from azure_python.hosting import container
from azure_python.protocols.i_azure_text_analytics_service import (
    IAzureTextAnalyticsService,
)


def fetch_content():
    results = []
    for f in os.listdir("data"):
        if f.endswith(".txt"):
            with open(f"data/{f}") as file:
                results.append(file.read())
    return results


async def main():
    svc = container[IAzureTextAnalyticsService]
    results = await svc.recognize_entities(
        [
            "Studies have shown that regular physical activity is "
            "associated with a longer lifespan, reducing the risk "
            "of premature death from all causes.",
            "Climate change refers to significant, long-term changes in "
            "the average temperature, weather patterns, and atmospheric "
            "conditions on Earth. Although climate change is a natural "
            "phenomenon, the current trend of rapid warming is largely "
            "attributed to human activities. Understanding the causes, "
            "effects, and potential solutions for climate change is "
            "critical for mitigating its impacts on the environment "
            "and human society.",
        ]
    )
    print(json.dumps([r.model_dump() for r in results], indent=2))


if __name__ == "__main__":
    asyncio.run(main())
