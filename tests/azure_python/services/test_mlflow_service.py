from unittest.mock import MagicMock

import pytest
from mlflow import MlflowException

from azure_python.services.mlflow_service import MLFlowService


def test_start_run(mocker: MagicMock):
    mocker.patch("mlflow.set_experiment", return_value=MagicMock(experiment_id="123"))
    mocker.patch("mlflow.start_run", return_value=MagicMock())
    mocker.patch(
        "mlflow.active_run",
        return_value=MagicMock(info=MagicMock(run_id="456", status="RUNNING")),
    )

    service = MLFlowService(logger=MagicMock())
    service.start_run(experiment_name="test_experiment", run_name="test_run")

    assert service.experiment_id == "123"


def test_start_run_failed(mocker: MagicMock):
    mocker.patch("mlflow.set_experiment", return_value=MagicMock(experiment_id="123"))
    mocker.patch("mlflow.start_run", return_value=MagicMock())
    mocker.patch("mlflow.active_run", return_value=None)

    service = MLFlowService(logger=MagicMock())

    with pytest.raises(
        Exception, match="Run was not created for experiment, test_experiment."
    ):
        service.start_run(experiment_name="test_experiment", run_name="test_run")


def test_end_run(mocker: MagicMock):
    mocker.patch(
        "mlflow.active_run",
        side_effect=[MagicMock(info=MagicMock(run_id="456", status="RUNNING")), None],
    )
    mocker.patch("mlflow.end_run")

    service = MLFlowService(logger=MagicMock())
    service.end_run()


def test_end_run_does_not_end(mocker: MagicMock):
    mocker.patch(
        "mlflow.active_run",
        return_value=MagicMock(info=MagicMock(run_id="456", status="RUNNING")),
    )
    mocker.patch("mlflow.end_run")

    service = MLFlowService(logger=MagicMock())

    with pytest.raises(MlflowException):
        service.end_run()


def test_query_runs_by_experiment_id(mocker: MagicMock):
    mocker.patch(
        "mlflow.search_runs",
        return_value=[{"run_id": "123", "experiment_id": "456", "status": "FINISHED"}],
    )

    service = MLFlowService(logger=MagicMock())
    runs = service.query_runs_by_experiment_id(experiment_id="456")

    assert len(runs) == 1


def test_get_run_artifact(mocker: MagicMock):
    mocker.patch(
        "mlflow.artifacts.load_dict",
        return_value={"artifact": "data"},
    )

    service = MLFlowService(logger=MagicMock())
    artifact = service.get_run_artifact(run_id="123", name="test_artifact")

    assert artifact == {"artifact": "data"}


def test_get_run_artifact_not_found(mocker: MagicMock):
    mocker.patch(
        "mlflow.artifacts.load_dict",
        side_effect=Exception("Artifact not found"),
    )

    service = MLFlowService(logger=MagicMock())
    artifact = service.get_run_artifact(run_id="123", name="test_artifact")

    assert artifact is None
