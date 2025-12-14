from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from azure_python.services.azure_mlflow_service import (
    AzureMLFlowService,
    AzureMLFlowServiceEnv,
)


def test_set_tracking_uri(mocker: MockerFixture):
    mock_workspace = MagicMock()
    mock_workspace.mlflow_tracking_uri = "https://example.com/mlflow"

    mock_client = MagicMock()
    mock_client.workspaces = MagicMock()
    mock_client.workspaces.get = MagicMock(return_value=mock_workspace)
    mocker.patch(
        "azure_python.services.azure_mlflow_service.MLClient",
        return_value=mock_client,
    )
    mocker.patch(
        "azure_python.services.azure_mlflow_service.DefaultAzureCredential",
        return_value=MagicMock(),
    )
    mocker.patch("azure_python.services.azure_mlflow_service.mlflow")
    env = AzureMLFlowServiceEnv(
        azure_ml_subscription_id="your-subscription-id",
        azure_ml_resource_group="your-resource-group",
        azure_ml_workspace_name="your-workspace-name",
    )
    mock_service = AzureMLFlowService(env=env, logger=MagicMock())

    assert mock_service.ml_client is not None


def test_set_tracking_uri_no_workspace(mocker: MockerFixture):
    mock_client = MagicMock()
    mock_client.workspaces = MagicMock()
    mock_client.workspaces.get = MagicMock(return_value=None)
    mocker.patch(
        "azure_python.services.azure_mlflow_service.MLClient",
        return_value=mock_client,
    )
    mocker.patch(
        "azure_python.services.azure_mlflow_service.DefaultAzureCredential",
        return_value=MagicMock(),
    )
    mocker.patch("azure_python.services.azure_mlflow_service.mlflow")
    env = AzureMLFlowServiceEnv(
        azure_ml_subscription_id="your-subscription-id",
        azure_ml_resource_group="your-resource-group",
        azure_ml_workspace_name="your-workspace-name",
    )

    with pytest.raises(ValueError, match="Workspace not found."):
        AzureMLFlowService(env=env, logger=MagicMock())


def test_set_tracking_uri_no_uri(mocker: MockerFixture):
    mock_workspace = MagicMock()
    mock_workspace.mlflow_tracking_uri = ""

    mock_client = MagicMock()
    mock_client.workspaces = MagicMock()
    mock_client.workspaces.get = MagicMock(return_value=mock_workspace)
    mocker.patch(
        "azure_python.services.azure_mlflow_service.MLClient",
        return_value=mock_client,
    )
    mocker.patch(
        "azure_python.services.azure_mlflow_service.DefaultAzureCredential",
        return_value=MagicMock(),
    )
    mocker.patch("azure_python.services.azure_mlflow_service.mlflow")
    env = AzureMLFlowServiceEnv(
        azure_ml_subscription_id="your-subscription-id",
        azure_ml_resource_group="your-resource-group",
        azure_ml_workspace_name="your-workspace-name",
    )

    with pytest.raises(ValueError, match="Tracking Id not found."):
        AzureMLFlowService(env=env, logger=MagicMock())
