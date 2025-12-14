import logging
from dataclasses import dataclass

import mlflow
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from lagom.environment import Env

from azure_python.services.mlflow_service import MLFlowService


class AzureMLFlowServiceEnv(Env):
    """
    AzureMLFlowServiceEnv is a subclass of Env that provides
    environment variables for connecting to Azure MLFlow.
    It includes the Azure subscription ID, resource group name,
    and workspace name.
    """

    azure_ml_subscription_id: str
    azure_ml_resource_group: str
    azure_ml_workspace_name: str


@dataclass
class AzureMLFlowService(MLFlowService):
    env: AzureMLFlowServiceEnv
    logger: logging.Logger

    """
    AzureMLFlowService is a subclass of MLFlowService that provides
    functionality to connect to Azure MLFlow.
    It uses the Azure MLClient to interact with the Azure ML workspace
    and sets the tracking URI for MLFlow to the Azure ML workspace's tracking URI.
    """

    def __post_init__(self) -> None:
        self.ml_client = MLClient(
            credential=DefaultAzureCredential(),
            subscription_id=self.env.azure_ml_subscription_id,
            resource_group_name=self.env.azure_ml_resource_group,
            workspace_name=self.env.azure_ml_workspace_name,
        )
        self._set_tracking_uri()

    def _set_tracking_uri(self) -> str:
        """
        Fetch the workspace using the MLClient and set the tracking URI to create the
        connection with Azure ML workspace.

        :return: The tracking URI for the MLFlowService
        :rtype: str
        """
        workspace = self.ml_client.workspaces.get(self.env.azure_ml_workspace_name)  # type: ignore

        if workspace:
            mlflow_tracking_uri = workspace.mlflow_tracking_uri
            if mlflow_tracking_uri:
                mlflow.set_tracking_uri(mlflow_tracking_uri)
                return mlflow_tracking_uri

            self.logger.error("Tracking Id not found.")
            raise ValueError("Tracking Id not found.")
        else:
            self.logger.error("Workspace not found.")
            raise ValueError("Workspace not found.")
