import logging
from dataclasses import dataclass
from typing import Any

import mlflow
from mlflow.entities import Run
from mlflow.exceptions import MlflowException

from azure_python.protocols.i_mlflow_service import IMLFlowService, State


@dataclass
class MLFlowService(IMLFlowService):
    """
    MLFlowService is a class that provides functionality to interact with MLFlow.
    It includes methods to start and end runs, log parameters, metrics, and artifacts,
    and query runs by experiment name or ID.
    """

    logger: logging.Logger

    def start_run(self, experiment_name: str, run_name: str | None = None):
        """
        Start a new MLFlow run with the given experiment name.
        If the run is successfully created, log the run ID and status.

        :param experiment_name: The name of the experiment for the MLFlow run
        :type experiment_name: str
        :param run_name: The name of the run, defaults to None
        :type run_name: str, optional
        :raises MlflowException: If the run is not created.
        """
        self.experiment_name = experiment_name
        experiment = mlflow.set_experiment(experiment_name=experiment_name)
        self.experiment_id = str(experiment.experiment_id)  # type: ignore

        mlflow.start_run(run_name=run_name)
        run = mlflow.active_run()

        if run:
            self.logger.info(f"run_id: {run.info.run_id}; status: {run.info.status}")  # type: ignore
        else:
            self.logger.error("Run was not created.")
            raise MlflowException(
                f"Run was not created for experiment, {experiment_name}."
            )

    def end_run(self, state: State = State.FINISHED):
        """
        End the current MLFlow run (if there is one).
        If there is an active run, log its run_id and status, then end it.

        :param end_status: The status to end the run with
        """
        active_run = mlflow.active_run()
        if active_run:
            run_id: str = active_run.info.run_id  # type: ignore
            status: str = active_run.info.status  # type: ignore

            self.logger.info(f"Ending: run_id: {run_id}; status: {status}")
            mlflow.end_run(status=str(state))

            active_run = mlflow.active_run()
            if active_run:
                msg = f"Run {active_run.info.run_id} was not ended."  # type: ignore
                self.logger.error(msg)
                raise MlflowException(msg)

    def query_runs_by_experiment_id(
        self,
        experiment_id: str,
        tag: tuple[str, str] | None = None,
        max_results: int | None = None,
    ) -> list[Run]:
        queries = [f"tags.{tag[0]} = '{tag[1]}'"] if tag else []
        queries.append("attributes.status = 'Completed'")

        return mlflow.search_runs(  # type: ignore
            experiment_ids=[experiment_id],
            output_format="list",
            filter_string=" and ".join(queries),
            order_by=["start_time DESC"],
            max_results=max_results,  # type: ignore
        )

    def get_run_artifact(self, run_id: str, name: str) -> dict[str, Any] | None:
        """
        Get the artifact URI for the given run ID.

        :param run_id: The ID of the run to get the artifact URI for
        :param name: The name of the artifact to retrieve
        :return: The artifact as a dictionary or None if not found
        """
        try:
            return mlflow.artifacts.load_dict(f"runs:/{run_id}/{name}")  # type: ignore
        except Exception as e:
            self.logger.error(f"Error loading artifact: {e}")
            return None
