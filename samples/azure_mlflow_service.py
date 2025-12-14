import mlflow

from azure_python.hosting import container


def main() -> None:
    from azure_python.protocols.i_mlflow_service import IMLFlowService

    svc = container[IMLFlowService]
    svc.start_run(experiment_name="sample_experiment", run_name="sample_run")

    # Simulate some MLFlow logging activity here
    # we also use mflow.log_text and other logging methods as needed
    mlflow.log_metrics({"accuracy": 0.95, "loss": 0.05})

    svc.end_run()
    # check the mlflow UI or backend to verify the run has been logged


if __name__ == "__main__":
    main()
