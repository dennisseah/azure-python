from typing import Protocol

from azure_python.models.original_resource import OriginalResource
from azure_python.models.original_resource_activities import OriginalResourceActivity


class IAzureResourcesQueryService(Protocol):
    async def fetch_subscriptions(self, tenant_id) -> list[OriginalResource]:
        """
        Fetch all subscriptions in a tenant.

        :param tenant_id: The tenant ID.
        :return: A list of subscriptions in a tenant.
        """
        ...

    async def fetch_resource_groups(
        self, subscription_id: str
    ) -> list[OriginalResource]:
        """
        List all resource groups in the subscription.

        :param subscription_id: The subscription ID.
        :return: A list of resource groups.
        """
        ...

    async def fetch_resources(
        self, subscription_id: str, resource_group_name: str | None = None
    ) -> list[OriginalResource]:
        """
        Fetch all resources in a resource group.

        :param subscription_id: The subscription ID.
        :param resource_group_name: The name of the resource group.
        :return: A list of resources in the resource group.
        """
        ...

    async def fetch_creations(
        self, subscription_id: str, resource_group_name: str | None = None
    ) -> list[OriginalResourceActivity]:
        """
        Fetch all resources that have been created in a resource group.

        :param subscription_id: The subscription ID.
        :param resource_group_name: The name of the resource group.
        :return: A list of resources that have created.
        """
        ...

    async def fetch_deletions(
        self, subscription_id: str
    ) -> list[OriginalResourceActivity]:
        """
        Fetch all resources that have been deleted in a subscription.

        :param subscription_id: The subscription ID.
        :return: A list of resources that have deleted.
        """
        ...

    async def fetch_changes(
        self, subscription_id: str, resource_group_name: str | None = None
    ) -> list[OriginalResourceActivity]:
        """
        Fetch all resources that have changed in a resource group.

        :param subscription_id: The subscription ID.
        :param resource_group_name: The name of the resource group.
        :return: A list of resources that have changed.
        """
        ...
        ...

    async def fetch_azure_policies(
        self, subscription_id: str, resource_group_name: str | None = None
    ) -> list[OriginalResourceActivity]:
        """
        Fetch all policies applied to a resource group.

        :param subscription_id: The subscription ID.
        :param resource_group_name: The name of the resource group.
        :return: A list of policies applied to the resource group.
        """
        ...

    async def fetch_azure_patch_assessments(
        self, subscription_id: str, resource_group_name: str | None = None
    ) -> list[OriginalResourceActivity]:
        """
        Fetch all patch assessments applied to a resource group.

        :param subscription_id: The subscription ID.
        :param resource_group_name: The name of the resource group.
        :return: A list of patch assessments applied to the resource group.
        """
        ...
