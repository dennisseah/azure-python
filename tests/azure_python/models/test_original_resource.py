import pytest

from azure_python.models.original_resource import OriginalResource


@pytest.fixture
def mock_resource():
    return OriginalResource(
        id="/subscriptions/sub1/resourceGroups/testGroup/providers/namespace/type/test_resource",
        name="test_resource",
        type="namespace/type",
        tenantId="tenantId",
        kind="kind",
        location="location",
        resourceGroup="testGroup",
        subscriptionId="subscriptionId",
        managedBy="managedBy",
        plan={"plan": "plan"},
        properties={"properties": "properties"},
    )


def test_resource_group(mock_resource):
    assert (
        mock_resource.resource_group == "/subscriptions/sub1/resourceGroups/testGroup"
    )


def test_resource_group_name(mock_resource):
    assert mock_resource.resource_group_name == "testGroup"


def test_resource_provider_namespace(mock_resource):
    assert mock_resource.resource_provider_namespace == "namespace"


def test_resource_type(mock_resource):
    assert mock_resource.resource_type == "type"


def test_resource_name(mock_resource):
    assert mock_resource.resource_name == "test_resource"
