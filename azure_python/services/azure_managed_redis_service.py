from dataclasses import dataclass
from typing import Any

from lagom.environment import Env
from redis.asyncio import Redis
from redis_entraid.cred_provider import create_from_default_azure_credential

from azure_python.protocols.i_azure_managed_redis_service import (
    IAzureManagedRedisService,
)


class AzureManagedRedisServiceEnv(Env):
    redis_host: str
    redis_port: int = 10000
    socket_timeout: int = 10
    socket_connect_timeout: int = 10


@dataclass
class AzureManagedRedisService(IAzureManagedRedisService):
    env: AzureManagedRedisServiceEnv

    def __post_init__(self) -> None:
        self.client = self.get_client()

    def get_client(self) -> Redis:
        credential_provider = create_from_default_azure_credential(
            scopes=("https://redis.azure.com/.default",),
        )

        return Redis(
            host=self.env.redis_host,
            port=self.env.redis_port,
            ssl=True,
            decode_responses=True,
            credential_provider=credential_provider,
            socket_timeout=self.env.socket_timeout,
            socket_connect_timeout=self.env.socket_connect_timeout,
        )

    async def ping(self) -> bool:
        return await self.client.ping()  # type: ignore

    async def set(self, key: str, value: Any) -> None:
        await self.client.set(name=key, value=value)

    async def get(self, key: str) -> Any:
        return await self.client.get(name=key)
