from contextlib import asynccontextmanager
from dataclasses import dataclass
from logging import Logger
from typing import AsyncIterator

from azure.ai.contentsafety.aio import ContentSafetyClient
from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    AnalyzeTextResult,
    TextCategory,
)
from azure.core.credentials import AzureKeyCredential
from azure.identity.aio import DefaultAzureCredential
from lagom.environment import Env

from azure_python.protocols.i_content_safety_service import IContentSafetyService


class ContentSafetyServiceEnv(Env):
    content_safety_endpoint: str
    content_safety_key: str | None = None


@dataclass
class ContentSafetyService(IContentSafetyService):
    env: ContentSafetyServiceEnv
    logger: Logger

    @asynccontextmanager
    async def get_client(self) -> AsyncIterator[ContentSafetyClient]:
        client = None
        credential = (
            DefaultAzureCredential()
            if not self.env.content_safety_key
            else AzureKeyCredential(self.env.content_safety_key)
        )

        try:
            client = ContentSafetyClient(
                self.env.content_safety_endpoint,
                credential=credential,
            )
            yield client
        finally:
            if client:
                try:
                    await client.close()
                except Exception as e:
                    self.logger.warning(f"Error closing blob client: {e}")

            if credential and not self.env.content_safety_key:
                try:
                    await credential.close()  # type: ignore
                except Exception as e:
                    self.logger.warning(f"Error closing credential: {e}")

    def collect_results(self, analysis_response: AnalyzeTextResult) -> list[dict]:
        results = []
        for cat in [
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ]:
            result = next(
                (
                    item
                    for item in analysis_response.categories_analysis
                    if item.category == cat
                ),
                None,
            )
            if result:
                results.append(result.as_dict())
        return results

    async def analyze_text(self, text: str) -> list[dict]:
        self.logger.debug("[BEGIN] analyze_text")
        request = AnalyzeTextOptions(text=text)

        async with self.get_client() as client:
            response = await client.analyze_text(request)
            self.logger.debug("[COMPLETED] analyze_text")

        return self.collect_results(response)
