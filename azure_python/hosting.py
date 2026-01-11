"""Defines our top level DI container.
Utilizes the Lagom library for dependency injection, see more at:

- https://lagom-di.readthedocs.io/en/latest/
- https://github.com/meadsteve/lagom
"""

import logging
import os

from dotenv import load_dotenv
from lagom import Container, dependency_definition

from azure_python.common.log_utils import set_log_level
from azure_python.protocols.i_adversarial_simulation_service import (
    IAdversarialSimulationService,
)
from azure_python.protocols.i_azure_blob_storage_service import IAzureBlobStorageService
from azure_python.protocols.i_azure_cosmos_service import IAzureCosmosService
from azure_python.protocols.i_azure_defender_service import IAzureDefenderService
from azure_python.protocols.i_azure_form_recognizer import IAzureFormRecognizer
from azure_python.protocols.i_azure_keyvault_service import IAzureKeyVaultService
from azure_python.protocols.i_azure_managed_redis_service import (
    IAzureManagedRedisService,
)
from azure_python.protocols.i_azure_openai_service import IAzureOpenAIService
from azure_python.protocols.i_azure_resources_query_service import (
    IAzureResourcesQueryService,
)
from azure_python.protocols.i_azure_table_storage_service import (
    IAzureTableStorageService,
)
from azure_python.protocols.i_azure_text2speech_service import IAzureText2SpeechService
from azure_python.protocols.i_azure_text_analytics_service import (
    IAzureTextAnalyticsService,
)
from azure_python.protocols.i_content_safety_service import IContentSafetyService
from azure_python.protocols.i_embedding_service import IEmbeddingService
from azure_python.protocols.i_mlflow_service import IMLFlowService
from azure_python.protocols.i_openai_content_evaluator import IOpenAIContentEvaluator

load_dotenv(dotenv_path=".env")


container = Container()
"""The top level DI container for our application."""


# Register our dependencies ------------------------------------------------------------


@dependency_definition(container, singleton=True)
def logger() -> logging.Logger:
    log_level = os.getenv("LOG_LEVEL", "ERROR")
    if log_level not in ["ERROR", "WARNING", "INFO", "DEBUG"]:
        log_level = "ERROR"
    return set_log_level(log_level)  # type: ignore


@dependency_definition(container, singleton=True)
def azure_blob_storage_service() -> IAzureBlobStorageService:
    from azure_python.services.azure_blob_storage_service import (
        AzureBlobStorageService,
    )

    return container[AzureBlobStorageService]


@dependency_definition(container, singleton=True)
def azure_table_storage_service() -> IAzureTableStorageService:
    from azure_python.services.azure_table_storage_service import (
        AzureTableStorageService,
    )

    return container[AzureTableStorageService]


@dependency_definition(container, singleton=True)
def azure_openai_service() -> IAzureOpenAIService:
    from azure_python.services.azure_openai_service import (
        AzureOpenAIService,
    )

    return container[AzureOpenAIService]


@dependency_definition(container, singleton=True)
def mlflow_service() -> IMLFlowService:
    if os.getenv("LOCAL_MLFLOW", "false").lower() == "true":
        from azure_python.services.mlflow_service import MLFlowService

        return container[MLFlowService]

    from azure_python.services.azure_mlflow_service import AzureMLFlowService

    return container[AzureMLFlowService]


@dependency_definition(container, singleton=True)
def adversarial_simulation_service() -> IAdversarialSimulationService:
    from azure_python.services.adversarial_simulation_service import (
        AdversarialSimulationService,
    )

    return container[AdversarialSimulationService]


@dependency_definition(container, singleton=True)
def azure_cosmos_service() -> IAzureCosmosService:
    from azure_python.services.azure_cosmos_service import (
        AzureCosmosService,
    )

    return container[AzureCosmosService]


@dependency_definition(container, singleton=True)
def openai_content_evaluator() -> IOpenAIContentEvaluator:
    from azure_python.services.openai_content_evaluator import (
        OpenAIContentEvaluator,
    )

    return container[OpenAIContentEvaluator]


@dependency_definition(container, singleton=True)
def content_safety_service() -> IContentSafetyService:
    from azure_python.services.content_safety_service import (
        ContentSafetyService,
    )

    return container[ContentSafetyService]


@dependency_definition(container, singleton=True)
def embedding_service() -> IEmbeddingService:
    from azure_python.services.embedding_service import EmbeddingService

    return container[EmbeddingService]


@dependency_definition(container, singleton=True)
def azure_managed_redis_service() -> IAzureManagedRedisService:
    from azure_python.services.azure_managed_redis_service import (
        AzureManagedRedisService,
    )

    return container[AzureManagedRedisService]


@dependency_definition(container, singleton=True)
def azure_ai_textanalytics_service() -> IAzureTextAnalyticsService:
    from azure_python.services.azure_text_analytics_service import (
        AzureTextAnalyticsService,
    )

    return container[AzureTextAnalyticsService]


@dependency_definition(container, singleton=True)
def azure_defender_service() -> IAzureDefenderService:
    from azure_python.services.azure_defender_service import (
        AzureDefenderService,
    )

    return container[AzureDefenderService]


@dependency_definition(container, singleton=True)
def azure_resources_query() -> IAzureResourcesQueryService:
    from azure_python.services.azure_resources_query_service import (
        AzureResourcesQueryService,
    )

    return container[AzureResourcesQueryService]


@dependency_definition(container, singleton=True)
def azure_text2speech_service() -> IAzureText2SpeechService:
    from azure_python.services.azure_text2speech_service import (
        AzureText2SpeechService,
    )

    return container[AzureText2SpeechService]


@dependency_definition(container, singleton=True)
def azure_keyvault_service() -> IAzureKeyVaultService:
    from azure_python.services.azure_keyvault_service import (
        AzureKeyVaultService,
    )

    return container[AzureKeyVaultService]


@dependency_definition(container, singleton=True)
def azure_form_recognizer() -> IAzureFormRecognizer:
    from azure_python.services.azure_form_recognizer import (
        AzureFormRecognizer,
    )

    return container[AzureFormRecognizer]
