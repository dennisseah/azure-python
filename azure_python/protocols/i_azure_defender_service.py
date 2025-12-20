from typing import Protocol

from azure_python.models.azure_defender import ComplianceResult


class IAzureDefenderService(Protocol):
    async def get_compliance_results(self, resource_id: str) -> list[ComplianceResult]:
        """
        Get compliance results for a given resource.

        :param resource_id: The resource ID.
        :return: A list of compliance results.
        """
        ...
