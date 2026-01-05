import logging
from dataclasses import dataclass
from typing import Any, AsyncIterator, Literal

from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.resourcegraph.aio import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest, QueryRequestOptions
from fastapi.concurrency import asynccontextmanager

from azure_python.models.original_resource import OriginalResource
from azure_python.models.original_resource_activities import OriginalResourceActivity
from azure_python.protocols.i_azure_resources_query_service import (
    IAzureResourcesQueryService,
)


@dataclass
class AzureResourcesQueryService(IAzureResourcesQueryService):
    logger: logging.Logger

    @asynccontextmanager
    async def get_az_graph_client(self) -> AsyncIterator[ResourceGraphClient]:
        credential = DefaultAzureCredential()
        client = ResourceGraphClient(credential)

        try:
            yield client
        finally:
            await client.close()

            if credential:
                await credential.close()

    def get_timestamp(self, data: dict[str, Any], path) -> str:
        if not path:
            return ""
        for key in path.split("/"):
            data = data.get(key, {})
        return str(data)

    async def query_raw(self, query: str) -> list[dict[str, Any]]:
        data: list[dict[str, Any]] = []
        argQuery = QueryRequest(
            subscriptions=[],
            query=query,
            options=QueryRequestOptions(top=100, result_format="objectArray"),
        )

        async with self.get_az_graph_client() as client:
            argResults = await client.resources(argQuery)
            data = data + argResults.data  # type: ignore
            total = argResults.total_records

            while total != len(data):
                argQuery.options.skip = len(data)  # type: ignore
                argResults = await client.resources(argQuery)
                data = data + argResults.data  # type: ignore

            return data

    async def query_activities(
        self,
        query: str,
        action_type: Literal["Create", "Update", "Delete", "Compliance"],
        timestamp: str,
    ) -> list[OriginalResourceActivity]:
        self.logger.debug(f"[BEGIN] query_activities for action_type: {action_type}")

        data = await self.query_raw(query)

        def create(r: dict[str, Any]) -> OriginalResourceActivity | None:
            res_id = None

            if "targetResourceId" in r["properties"]:
                res_id = r["properties"]["targetResourceId"]
            elif "resourceId" in r["properties"]:
                res_id = r["properties"]["resourceId"]

            if res_id:
                return OriginalResourceActivity(
                    **r,
                    res_id=res_id,
                    res_name=res_id.split("/")[-1],
                    action_type=action_type,
                    timestamp=self.get_timestamp(r, timestamp),
                )
            return None

        created = [create(r) for r in data]

        self.logger.debug(
            f"[COMPLETED] query_activities for action_type: {action_type}, count: {len(created)}"  # noqa E501
        )
        return [c for c in created if c]

    async def query(self, query: str) -> list[OriginalResource]:
        data = await self.query_raw(query)
        return [OriginalResource(**r) for r in data]

    async def fetch_subscriptions(self, tenant_id: str) -> list[OriginalResource]:
        self.logger.debug(f"[BEGIN] fetch_subscriptions for tenant_id: {tenant_id}")
        result = await self.query(
            f"""resourcecontainers
            |
            where type =~ 'microsoft.resources/subscriptions' and
            tenantId == '{tenant_id}'
            | sort by name
            """
        )
        self.logger.debug(
            f"[COMPLETED] fetch_subscriptions for tenant_id: {tenant_id}, count: {
                len(result)
            }"
        )
        return result

    async def fetch_resource_groups(
        self, subscription_id: str
    ) -> list[OriginalResource]:
        self.logger.debug(
            f"[BEGIN] fetch_resource_groups for subscription_id: {subscription_id}"
        )
        result = await self.query(
            f"""resourcecontainers
            |
            where type =~ 'microsoft.resources/subscriptions/resourcegroups'
            and subscriptionId == '{subscription_id}'
            | sort by name
            """
        )
        self.logger.debug(
            f"[COMPLETED] fetch_resource_groups for subscription_id: {subscription_id}, "  # noqa E501
            f"count: {len(result)}"
        )
        return result

    async def fetch_resources(
        self, subscription_id: str, resource_group_name: str | None = None
    ) -> list[OriginalResource]:
        self.logger.debug(
            f"[BEGIN] fetch_resources for subscription_id: {subscription_id}, "
            f"resource_group_name: {resource_group_name}"
        )
        where_clause = (
            f"resourceGroup =~ '{resource_group_name}' and"
            if resource_group_name
            else "isnotempty(resourceGroup) and"
        )

        results = await self.query(
            f"""
            resources |
                where subscriptionId =~ '{subscription_id}' and
                {where_clause}
                isempty(properties.source)
                | sort by name
            """
        )

        self.logger.debug(
            f"[COMPLETED] fetch_resources for subscription_id: {subscription_id}, "
            f"resource_group_name: {resource_group_name}, count: {len(results)}"
        )
        return results

    async def fetch_creations(
        self, subscription_id: str, resource_group_name: str | None = None
    ) -> list[OriginalResourceActivity]:
        self.logger.debug(
            f"[BEGIN] fetch_creations for subscription_id: {subscription_id}, "
            f"resource_group_name: {resource_group_name}"
        )
        where_clause = (
            f"resourceGroup =~ '{resource_group_name}' and"
            if resource_group_name
            else "isnotempty(resourceGroup) and"
        )

        result = await self.query_activities(
            f"""
            resourcechanges |
                where subscriptionId =~ '{subscription_id}' and
                {where_clause}
                properties.changeType =~ 'Create'
            """,
            "Create",
            "properties/changeAttributes/timestamp",
        )
        self.logger.debug(
            f"[COMPLETED] fetch_creations for subscription_id: {subscription_id}, "
            f"resource_group_name: {resource_group_name}, count: {len(result)}"
        )
        return result

    async def fetch_deletions(
        self, subscription_id: str
    ) -> list[OriginalResourceActivity]:
        self.logger.debug(
            f"[BEGIN] fetch_deletions for subscription_id: {subscription_id}"
        )
        result = await self.query_activities(
            f"""
            resourcechanges |
                where subscriptionId =~ '{subscription_id}' and
                properties.changeType =~ 'Delete'
            """,
            "Delete",
            "properties/changeAttributes/timestamp",
        )
        self.logger.debug(
            f"[COMPLETED] fetch_deletions for subscription_id: {subscription_id}, "
            f"count: {len(result)}"
        )
        return result

    async def fetch_changes(
        self, subscription_id: str, resource_group_name: str | None = None
    ) -> list[OriginalResourceActivity]:
        self.logger.debug(
            f"[BEGIN] fetch_changes for subscription_id: {subscription_id}, "
            f"resource_group_name: {resource_group_name}"
        )
        where_clause = (
            f"resourceGroup =~ '{resource_group_name}' and"
            if resource_group_name
            else "isnotempty(resourceGroup) and"
        )

        result = await self.query_activities(
            f"""
            resourcechanges |
                where subscriptionId =~ '{subscription_id}' and
                {where_clause}
                properties.changeType =~ 'Update'
            """,
            "Update",
            "properties/changeAttributes/timestamp",
        )
        self.logger.debug(
            f"[COMPLETED] fetch_changes for subscription_id: {subscription_id}, "
            f"resource_group_name: {resource_group_name}, count: {len(result)}"
        )
        return result

    async def fetch_azure_policies(
        self, subscription_id: str, resource_group_name: str | None = None
    ) -> list[OriginalResourceActivity]:
        self.logger.debug(
            f"[BEGIN] fetch_azure_policies for subscription_id: {subscription_id}, "
            f"resource_group_name: {resource_group_name}"
        )
        where_clause = (
            f"and resourceGroup =~ '{resource_group_name}'"
            if resource_group_name
            else "and isnotempty(resourceGroup)"
        )

        result = await self.query_activities(
            f"""
            policyresources |
                where subscriptionId =~ '{subscription_id}' {where_clause}
            """,
            "Compliance",
            "properties/timestamp",
        )
        self.logger.debug(
            f"[COMPLETED] fetch_azure_policies for subscription_id: {subscription_id}, "
            f"resource_group_name: {resource_group_name}, count: {len(result)}"
        )
        return result

    async def fetch_azure_patch_assessments(
        self, subscription_id: str, resource_group_name: str | None = None
    ) -> list[OriginalResourceActivity]:
        self.logger.debug(
            f"[BEGIN] fetch_azure_patch_assessments for subscription_id: {subscription_id}, "  # noqa E501
            f"resource_group_name: {resource_group_name}"
        )
        where_clause = (
            f"and resourceGroup =~ '{resource_group_name}'"
            if resource_group_name
            else "and isnotempty(resourceGroup)"
        )

        query = f"""
            patchassessmentresources |
                where subscriptionId =~ '{subscription_id}' {where_clause}
            """

        data = await self.query_raw(query)

        def create(r: dict[str, Any]) -> OriginalResourceActivity:
            id = r["id"]
            res_id = id[0 : id.rindex("/patchAssessmentResults")]

            return OriginalResourceActivity(
                **r,
                res_id=res_id,
                res_name=res_id.split("/")[-1],
                action_type="Compliance",
                timestamp=self.get_timestamp(r, "properties/lastModifiedDateTime"),
            )

        self.logger.debug(
            f"[COMPLETED] fetch_azure_patch_assessments for subscription_id: {subscription_id}, "  # noqa E501
            f"resource_group_name: {resource_group_name}, count: {len(data)}"
        )
        return [create(r) for r in data]
