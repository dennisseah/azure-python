from typing import Protocol

from azure_python.models.recognized_entities import RecognizedEntities


class IAzureTextAnalyticsService(Protocol):
    async def recognize_entities(
        self, content: list[str]
    ) -> list[RecognizedEntities]: ...
