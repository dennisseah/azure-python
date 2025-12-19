import asyncio

from azure_python.hosting import container
from azure_python.protocols.i_embedding_service import IEmbeddingService

svc = container[IEmbeddingService]


async def main() -> None:
    embeddings = await svc.get_embeddings(["Hello, world!"])

    print("Embeddings:")
    print(embeddings["data"][0]["embedding"])


if __name__ == "__main__":
    asyncio.run(main())
