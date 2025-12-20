from azure_python.models.original_resource_activities import OriginalResourceActivity


def test_property_resource_group():
    activity = OriginalResourceActivity(
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
        res_id="/subscriptions/sub1/resourceGroups/testGroup/providers/namespace/type/test_resource",
        res_name="test_resource",
        action_type="Create",
        timestamp="2024-01-01T00:00:00Z",
    )
    assert activity.resource_group == "/subscriptions/sub1/resourceGroups/testGroup"
    assert activity.resource_group_name == "testGroup"
