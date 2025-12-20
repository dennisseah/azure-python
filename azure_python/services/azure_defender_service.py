from dataclasses import dataclass
from typing import Any

import aiohttp
from azure.identity import DefaultAzureCredential

from azure_python.models.azure_defender import ComplianceResult
from azure_python.protocols.i_azure_defender_service import IAzureDefenderService

URL_COMPLIANCE_RESULTS = "https://management.azure.com/{0}/providers/Microsoft.Security/complianceResults?api-version=2017-08-01"


@dataclass
class AzureDefenderService(IAzureDefenderService):
    def __post_init__(self):
        tokenCredential = DefaultAzureCredential()
        self.accessToken = tokenCredential.get_token(
            "https://management.azure.com/.default"
        ).token

    async def get_compliance_results(self, resource_id: str) -> list[ComplianceResult]:
        url = URL_COMPLIANCE_RESULTS.format(resource_id)

        async with aiohttp.ClientSession() as client:
            headers = {
                "Authorization": "Bearer " + self.accessToken,
                "Content-Type": "application/json",
            }
            async with client.get(url, headers=headers) as resp:
                assert resp.status == 200
                results: Any = await resp.json()
                return (
                    [ComplianceResult(**val) for val in results["value"]]
                    if "value" in results
                    else []
                )
