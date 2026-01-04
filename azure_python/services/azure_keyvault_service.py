from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

from azure.identity.aio import DefaultAzureCredential
from azure.keyvault.secrets.aio import SecretClient
from lagom.environment import Env

from azure_python.protocols.i_azure_keyvault_service import IAzureKeyVaultService


class AzureKeyVaultServiceEnv(Env):
    azure_key_vault_url: str


@dataclass
class AzureKeyVaultService(IAzureKeyVaultService):
    env: AzureKeyVaultServiceEnv

    @asynccontextmanager
    async def get_client(self) -> AsyncIterator[SecretClient]:
        cred = DefaultAzureCredential()
        client = SecretClient(vault_url=self.env.azure_key_vault_url, credential=cred)

        try:
            yield client
        finally:
            await client.close()
            await cred.close()

    async def get_secret(self, secret_name: str) -> str | None:
        async with self.get_client() as client:
            secret = await client.get_secret(secret_name)
            return secret.value

    async def set_secret(self, secret_name: str, secret_value: str) -> bool:
        async with self.get_client() as client:
            await client.set_secret(secret_name, secret_value)
            return True
