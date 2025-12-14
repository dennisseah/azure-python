# Samples

This folder contains sample scripts demonstrating how to use the services
provided by the `azure_python` package. Each sample showcases a different Azure
service integration using dependency injection patterns.

## Available Samples

### 1. Azure OpenAI Service ([azure_openai_service.py](azure_openai_service.py))

Demonstrates how to use the Azure OpenAI service for chat completions.

```bash
task sample-azure-openai-service
```

### 2. Azure Blob Storage Service ([azure_blob_storage_service.py](azure_blob_storage_service.py))

Shows how to interact with Azure Blob Storage to list blobs in a container.

```bash
task sample-azure-blob-storage-service
```

### 3. Azure Foundry Adversarial Simulation ([azure_foundry_adv_sim.py](azure_foundry_adv_sim.py))

Demonstrates adversarial simulation testing for AI endpoints.

```bash
task sample-azure_foundry_adv_sim
```

### 4. Azure MLFlow Service ([azure_mlflow_service.py](azure_mlflow_service.py))

Shows how to use MLFlow for experiment tracking and logging.

```bash
task sample-azure-mlflow-service
```

## Common Patterns

All samples follow these consistent patterns:

### Dependency Injection

Services are resolved through the container defined in
[hosting.py](../azure_python/hosting.py):

## Prerequisites

Before running any samples, ensure you have:

1. Completed the project setup (see main [README.md](../README.md))
2. Configured environment variables in `.env` file
3. Activated the virtual environment

## Related Documentation

- [Guidelines](../Guidelines.md) - Python development best practices
- [UV Package Management](../docs/uv_package_management.md) - Dependency
  management guide
- [Main README](../README.md) - Project setup instructions
