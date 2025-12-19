from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

from azure.ai.inference.aio import EmbeddingsClient
from azure.ai.inference.models import EmbeddingsResult
from azure.core.credentials import AzureKeyCredential
from azure.identity.aio import DefaultAzureCredential
from lagom.environment import Env


class EmbeddingServiceEnv(Env):
    embedding_endpoint: str
    embedding_model: str
    embedding_credential: str | None = None


@dataclass
class EmbeddingService:
    env: EmbeddingServiceEnv

    @asynccontextmanager
    async def get_client(self) -> AsyncIterator[EmbeddingsClient]:
        endpoint = self.env.embedding_endpoint
        if self.env.embedding_credential:
            cred = AzureKeyCredential(self.env.embedding_credential)
        else:
            cred = DefaultAzureCredential(exclude_interactive_browser_credential=False)

        client = EmbeddingsClient(
            endpoint=endpoint,
            model=self.env.embedding_model,
            credential=cred,
            credential_scopes=["https://cognitiveservices.azure.com/.default"],
        )

        try:
            yield client
        finally:
            await client.close()

            if isinstance(cred, DefaultAzureCredential):
                await cred.close()

    async def get_embeddings(self, text: list[str]) -> EmbeddingsResult:
        async with self.get_client() as client:
            return await client.embed(input=text)
