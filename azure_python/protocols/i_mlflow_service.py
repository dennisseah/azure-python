from enum import Enum
from typing import Any, Protocol

from mlflow.entities import Run


class State(Enum):
    RUNNING = "RUNNING"
    SCHEDULED = "SCHEDULED"
    FINISHED = "FINISHED"
    FAILED = "FAILED"
    KILLED = "KILLED"

    def __str__(self):
        return self.value


class IMLFlowService(Protocol):
    def start_run(self, experiment_name: str, run_name: str | None = None) -> None:
        """Start a new run in the given experiment.

        :param experiment_name: The name of the experiment.
        :param run_name: The name of the run.
        """
        ...

    def end_run(self, state: State = State.FINISHED) -> None:
        """
        End the current run.

        :param state: The state of the run.
        """
        ...

    def query_runs_by_experiment_id(
        self,
        experiment_id: str,
        tag: tuple[str, str] | None = None,
        max_results: int | None = None,
    ) -> list[Run]:
        """
        Query runs by experiment ID and optional tag.

        :param experiment_id: The ID of the experiment.
        :param tag: An optional tag to filter runs.
        :param max_results: The maximum number of results to return.
        :return: A list of runs matching the query.
        """
        ...

    def get_run_artifact(self, run_id: str, name: str) -> dict[str, Any] | None:
        """
        Get the artifact URI for the given run ID.

        :param run_id: The ID of the run to get the artifact URI for
        :param name: The name of the artifact to retrieve
        :return: The artifact as a dictionary or None if not found
        """
        ...
