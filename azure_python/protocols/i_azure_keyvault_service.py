from typing import Protocol


class IAzureKeyVaultService(Protocol):
    async def get_secret(self, secret_name: str) -> str | None:
        """Get secret

        :param secret_name:  Secret name
        :return: Secret value
        """
        ...

    async def set_secret(self, secret_name: str, secret_value: str) -> bool:
        """Set secret

        :param secret_name:  Secret name
        :param secret_value: Secret value
        :return: Success status
        """
        ...
