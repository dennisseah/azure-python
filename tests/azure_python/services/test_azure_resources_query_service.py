from unittest.mock import AsyncMock, MagicMock

import pytest
from azure.mgmt.resourcegraph.models import QueryRequest, QueryResponse
from pytest_mock import MockerFixture

from azure_python.services.azure_resources_query_service import (
    AzureResourcesQueryService,
)


@pytest.fixture
def mock_default_token() -> MagicMock:
    mock_def_cred = MagicMock()
    mock_token = MagicMock()
    mock_token.token = "test"
    mock_def_cred.get_token.return_value = mock_token
    mock_def_cred.close = AsyncMock()
    return mock_def_cred


@pytest.fixture
def mock_service(mock_default_token: MagicMock, mocker: MockerFixture):
    mocker.patch(
        "azure_python.services.azure_resources_query_service.DefaultAzureCredential",
        return_value=mock_default_token,
    )
    svc = AzureResourcesQueryService(logger=MagicMock())
    return svc


@pytest.mark.asyncio
async def test_get_client(mock_default_token: MagicMock, mocker: MockerFixture):
    service = AzureResourcesQueryService(logger=MagicMock())
    mocker.patch(
        "azure_python.services.azure_resources_query_service.DefaultAzureCredential",
        return_value=mock_default_token,
    )
    mocker.patch(
        "azure_python.services.azure_resources_query_service.ResourceGraphClient",
        return_value=AsyncMock(),
    )
    async with service.get_az_graph_client() as client:  # type: ignore
        assert client is not None


@pytest.fixture
def mock_client():
    def wrapper(resourceId: bool = False, no_props: bool = False):
        if no_props:
            props = {}
        else:
            props = (
                {
                    "resourceId": "/subscriptions/123/resourceGroups/456/providers/Microsoft.Storage/storageAccounts/name"  # noqa E501
                }
                if resourceId
                else {
                    "targetResourceId": "/subscriptions/123/resourceGroups/456/providers/Microsoft.Storage/storageAccounts/name"  # noqa E501
                }
            )

        return_value = MagicMock(spec=QueryResponse)
        return_value.total_records = 2
        return_value.data = [
            {
                "id": "id",
                "name": "name",
                "type": "type",
                "tenantId": "tenantId",
                "kind": "kind",
                "location": "location",
                "resourceGroup": "resourceGroup",
                "subscriptionId": "subscriptionId",
                "managedBy": "managedBy",
                "plan": {"plan": "plan"},
                "properties": props,
            }
        ]

        class MockClient:
            def __init__(self):
                self.status = 200

            async def resources(self, query: QueryRequest):
                return return_value

            async def __aexit__(self, exc_type, exc, tb):
                pass

            async def __aenter__(self):
                return self

        client = MockClient()
        return client

    return wrapper


def test_get_az_graph_client(mock_service):
    assert mock_service.get_az_graph_client() is not None


@pytest.mark.asyncio
async def test_query(mock_service, mock_client):
    mock_service.get_az_graph_client = MagicMock(return_value=mock_client())

    resources = await mock_service.query("query")
    assert len(resources) == 2


@pytest.mark.asyncio
async def test_query_activities(mock_service, mock_client):
    mock_service.get_az_graph_client = MagicMock(return_value=mock_client())

    resources = await mock_service.query_activities("query", "Create", "resourceGroup")
    assert len(resources) == 2

    svc = AzureResourcesQueryService(logger=MagicMock())
    svc.get_az_graph_client = MagicMock(return_value=mock_client(True))

    resources = await svc.query_activities("query", "Create", "resourceGroup")
    assert len(resources) == 2

    svc = AzureResourcesQueryService(logger=MagicMock())
    svc.get_az_graph_client = MagicMock(return_value=mock_client(no_props=True))

    resources = await svc.query_activities("query", "Create", "resourceGroup")
    assert len(resources) == 0


@pytest.mark.asyncio
async def test_fetch_subscriptions():
    svc = AzureResourcesQueryService(logger=MagicMock())
    svc.query_raw = AsyncMock(return_value=[])
    svc.query = AsyncMock(return_value=[1])

    resources = await svc.fetch_subscriptions("test_tenant_id")
    assert len(resources) == 1


@pytest.mark.asyncio
async def test_list_all():
    svc = AzureResourcesQueryService(logger=MagicMock())
    svc.query_raw = AsyncMock(return_value=[])
    svc.query = AsyncMock(return_value=[1])

    resources = await svc.fetch_resource_groups("subscription_id")
    assert len(resources) == 1


@pytest.mark.asyncio
async def test_fetch_resources():
    svc = AzureResourcesQueryService(logger=MagicMock())
    svc.query_raw = AsyncMock(return_value=[])
    svc.query = AsyncMock(return_value=[1, 2])

    resources = await svc.fetch_resources("subscription_id")
    assert len(resources) == 2


@pytest.mark.asyncio
async def test_fetch_creations():
    svc = AzureResourcesQueryService(logger=MagicMock())
    svc.query_raw = AsyncMock(return_value=[])
    svc.query_activities = AsyncMock(return_value=[1, 2])

    resources = await svc.fetch_creations("subscription_id", "test")
    assert len(resources) == 2


@pytest.mark.asyncio
async def test_fetch_deletions():
    svc = AzureResourcesQueryService(logger=MagicMock())
    svc.query_raw = AsyncMock(return_value=[])
    svc.query_activities = AsyncMock(return_value=[1, 2])

    resources = await svc.fetch_deletions("subscription_id")
    assert len(resources) == 2


@pytest.mark.asyncio
async def test_fetch_changes_to_resource_group():
    svc = AzureResourcesQueryService(logger=MagicMock())
    svc.query_raw = AsyncMock(return_value=[])
    svc.query_activities = AsyncMock(return_value=[1, 2])

    resources = await svc.fetch_changes("subscription_id", "test")
    assert len(resources) == 2


@pytest.mark.asyncio
async def test_fetch_azure_policies():
    svc = AzureResourcesQueryService(logger=MagicMock())
    svc.query_raw = AsyncMock(return_value=[])
    svc.query_activities = AsyncMock(return_value=[1, 2])

    resources = await svc.fetch_azure_policies("subscription_id", "test")
    assert len(resources) == 2


def test_get_timestamp():
    svc = AzureResourcesQueryService(logger=MagicMock())
    assert svc.get_timestamp({}, "") == ""

    assert svc.get_timestamp({"timestamp": "2021-01-01"}, "timestamp") == "2021-01-01"
    assert (
        svc.get_timestamp({"test": {"timestamp": "2021-01-01"}}, "test/timestamp")
        == "2021-01-01"
    )


@pytest.mark.asyncio
async def test_fetch_azure_patch_assessments():
    svc = AzureResourcesQueryService(logger=MagicMock())

    svc.query_raw = AsyncMock(
        return_value=[
            {
                "id": "/subscriptions/123/resourceGroups/456/providers/Microsoft.Storage/storageAccounts/patchAssessmentResults",  # noqa E501
                "name": "name",
                "type": "type",
                "tenantId": "tenantId",
                "kind": "kind",
                "location": "location",
                "resourceGroup": "456",
                "subscriptionId": "123",
                "managedBy": "managedBy",
                "plan": {"plan": "plan"},
                "properties": {"lastModifiedDateTime": "now"},
            }
        ]
    )

    resources = await svc.fetch_azure_patch_assessments("subscription_id", "test")
    assert len(resources) == 1
