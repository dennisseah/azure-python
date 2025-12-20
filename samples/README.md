# Azure Python Samples

This folder contains sample scripts demonstrating how to use the services
provided by the `azure_python` package. Each sample showcases a different Azure
service integration using dependency injection patterns and async/await for
efficient I/O operations.

## Prerequisites

Before running any samples, ensure you have:

1. Completed the project setup (see main [README.md](../README.md))
2. Configured environment variables in `.env` file
3. Activated the virtual environment
4. Provisioned the required Azure services

## Available Samples

### 1. Azure OpenAI Service ([azure_openai_service.py](azure_openai_service.py))

Demonstrates chat completion using Azure OpenAI service.

**What it does:**

- Sends messages to Azure OpenAI's chat completion endpoint
- Generates multiple responses using the `num_generations` parameter
- Returns structured response objects in JSON format

**Key Features:**

- Chat completion with system and user messages
- Temperature control for response variability
- Multiple response generation
- Configurable logging

**Run:**

```bash
task sample-azure-openai-service
# or
python -m samples.azure_openai_service
```

---

### 2. Azure Blob Storage Service ([azure_blob_storage_service.py](azure_blob_storage_service.py))

Shows how to interact with Azure Blob Storage to list blobs in a container.

**What it does:**

- Lists all blobs in a container named "datasets"
- Uses dependency injection via the container to get the service instance

**Key Features:**

- Async blob listing functionality
- Clean dependency injection pattern
- Simple blob enumeration

**Run:**

```bash
task sample-azure-blob-storage-service
# or
python -m samples.azure_blob_storage_service
```

---

### 3. Azure Content Safety Service ([azure_content_safety_service.py](azure_content_safety_service.py))

Analyzes text content for safety issues using Azure Content Safety.

**What it does:**

- Analyzes text for potential safety concerns
- Returns analysis results including severity levels for different categories
- Example text: "She is a bad ass."

**Key Features:**

- Content moderation capabilities
- Text safety analysis
- Returns structured safety scores

**Run:**

```bash
task sample-azure-content-safety-service
# or
python -m samples.azure_content_safety_service
```

**Use Cases:**

- Content moderation
- User-generated content filtering
- Compliance checking

---

### 4. Azure Cosmos DB Service ([azure_cosmos_service.py](azure_cosmos_service.py))

Demonstrates basic Azure Cosmos DB operations, specifically listing containers.

**What it does:**

- Connects to a Cosmos DB account
- Lists all containers within the "sample-db" database

**Key Features:**

- Cosmos DB container enumeration
- Dependency injection pattern
- Async operations

**Run:**

```bash
task sample-azure-cosmos-service
# or
python -m samples.azure_cosmos_service
```

---

### 5. Azure Foundry Adversarial Simulation ([azure_foundry_adv_sim.py](azure_foundry_adv_sim.py))

Advanced sample showing how to perform adversarial simulation testing on AI
endpoints.

**What it does:**

- Creates a test endpoint using Azure OpenAI
- Executes adversarial simulation to test the endpoint's robustness
- Tests the AI model against various adversarial scenarios

**Key Features:**

- Adversarial testing for AI models
- Integration with Azure OpenAI
- Custom endpoint wrapping pattern
- Configurable logging

**Architecture:**

- `Endpoint` class wraps the OpenAI service
- Implements `call_endpoint` method that handles queries
- Adversarial simulation service tests the endpoint with challenging inputs

**Run:**

```bash
task sample-azure_foundry_adv_sim
# or
python -m samples.azure_foundry_adv_sim
```

**Use Cases:**

- Testing AI model robustness
- Red teaming for AI applications
- Safety and security validation

---

### 6. Azure Managed Redis Service ([azure_managed_redis_service.py](azure_managed_redis_service.py))

Demonstrates basic Redis operations using Azure Managed Redis.

**What it does:**

- Pings the Redis server to verify connectivity
- Sets a key-value pair (`my_key`: `my_value`)
- Retrieves and verifies the stored value with assertions

**Key Features:**

- Basic Redis operations (ping, set, get)
- Async Redis client
- Simple validation pattern

**Run:**

```bash
task sample-azure-managed-redis-service
# or
python -m samples.azure_managed_redis_service
```

**Use Cases:**

- Caching
- Session management
- Real-time analytics

---

### 7. Azure MLflow Service ([azure_mlflow_service.py](azure_mlflow_service.py))

Shows how to use MLflow for experiment tracking and logging.

**What it does:**

- Starts an MLflow run with a specific experiment ("sample_experiment") and run
  name ("sample_run")
- Logs metrics (accuracy: 0.95, loss: 0.05)
- Ends the run properly

**Key Features:**

- Experiment tracking
- Metrics logging
- Run management
- Integration with MLflow UI

**Run:**

```bash
task sample-azure-mlflow-service
# or
python samples/azure_mlflow_service.py
```

**Note:** Check the MLflow UI or backend to verify that runs have been logged
successfully.

**Use Cases:**

- Machine learning experiment tracking
- Model performance monitoring
- Experiment comparison

---

### 8. Azure Text Analytics Service ([azure_text_analytics_service.py](azure_text_analytics_service.py))

Shows how to use Azure Text Analytics for entity recognition in text.

**What it does:**

- Analyzes provided text to recognize entities (people, places, organizations,
  concepts, etc.)
- Processes multiple text documents in a batch
- Returns structured entity information in JSON format

**Key Features:**

- Named Entity Recognition (NER)
- Batch text processing
- Structured entity output with categories and confidence scores
- JSON formatted results

**Run:**

```bash
task sample-azure-text-analytics-service
# or
python -m samples.azure_text_analytics_service
```

**Example Texts Analyzed:**

- Health/lifestyle text about physical activity
- Climate change description

**Use Cases:**

- Extracting key information from documents
- Identifying entities in research papers or articles
- Content classification and tagging
- Knowledge graph construction

---

### 9. Embedding Service ([embedding_service.py](embedding_service.py))

Demonstrates how to generate text embeddings using Azure OpenAI.

**What it does:**

- Converts text ("Hello, world!") into vector embeddings
- Returns embedding vectors that can be used for similarity search

**Key Features:**

- Text-to-vector conversion
- Async embedding generation
- Support for batch embedding requests

**Run:**

```bash
task sample-embedding-service
# or
python -m samples.embedding_service
```

**Use Cases:**

- Semantic search
- Document similarity
- Text clustering
- RAG (Retrieval-Augmented Generation) applications
- Recommendation systems

---

## Utility Files

### `utils.py`

Contains helper functions used across samples.

**Functions:**

- `set_log_level(level)`: Configures logging level for better debugging
  - Accepts: "ERROR", "WARNING", "INFO", "DEBUG"
  - Sets up formatted logging output with timestamps

---

## Common Patterns

All samples follow consistent patterns:

### 1. Dependency Injection

Services are resolved through the container defined in
[hosting.py](../azure_python/hosting.py):

```python
from azure_python.hosting import container
from azure_python.protocols.i_azure_openai_service import IAzureOpenAIService

svc = container[IAzureOpenAIService]
```

### 2. Async/Await

Most operations use async patterns for better performance:

```python
async def main() -> None:
    result = await svc.some_operation()

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Type Hints

All code uses Python type hints for better IDE support and type checking.

### 4. Protocol-Based Design

Services implement well-defined protocols/interfaces defined in
`azure_python/protocols/`.

---

## Running Samples

You can run samples in two ways:

### Using Task Commands (Recommended)

```bash
task sample-azure-openai-service
task sample-azure-blob-storage-service
task sample-azure_foundry_adv_sim
task sample-azure-mlflow-service
```

### Direct Execution

```bash
# From project root
python samples/azure_openai_service.py
python -m samples.azure_openai_service
```

---

## Configuration

Ensure your Azure credentials and endpoints are properly configured in your
`.env` file or environment variables. Each service requires specific
configuration:

- **Azure OpenAI**: Endpoint URL, API key, deployment name
- **Azure Blob Storage**: Connection string or account credentials
- **Azure Cosmos DB**: Connection string, database name
- **Azure Redis**: Connection string
- **Azure Text Analytics**: Endpoint URL, API key
- **MLflow**: Tracking URI, experiment settings
- **Content Safety**: Endpoint URL, API key

Refer to the main project [README.md](../README.md) for detailed setup
instructions.

---

## Troubleshooting

### Common Issues

**Import Errors**

- Ensure you're running from the project root directory
- Verify virtual environment is activated
- Check that all dependencies are installed

**Authentication Errors**

- Verify your Azure credentials are configured correctly
- Check `.env` file has required variables
- Ensure service principals have appropriate permissions

**Service Errors**

- Check that the required Azure services are provisioned
- Verify service endpoints are accessible
- Check firewall rules and network settings

**Debugging**

- Use `set_log_level("DEBUG")` for verbose output
- Check logs for detailed error messages
- Verify environment variable names match expected format

---

## Related Documentation

- [Guidelines](../Guidelines.md) - Python development best practices
- [UV Package Management](../docs/uv_package_management.md) - Dependency
  management guide
- [Main README](../README.md) - Project setup instructions
- [Azure SDK for Python Documentation](https://learn.microsoft.com/python/azure/)
- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure Cosmos DB Documentation](https://learn.microsoft.com/azure/cosmos-db/)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
