from typing import Protocol

from azure.ai.inference.models import EmbeddingsResult


class IEmbeddingService(Protocol):
    async def get_embeddings(self, text: list[str]) -> EmbeddingsResult:
        """
        Get embeddings for the given text.

        :param text: The text to get embeddings for
        :return: The embeddings result
        """
        ...
