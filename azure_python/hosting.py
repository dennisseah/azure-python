"""Defines our top level DI container.
Utilizes the Lagom library for dependency injection, see more at:

- https://lagom-di.readthedocs.io/en/latest/
- https://github.com/meadsteve/lagom
"""

import logging
import os

from dotenv import load_dotenv
from lagom import Container, dependency_definition

from azure_python.protocols.i_azure_blob_storage_service import IAzureBlobStorageService
from azure_python.protocols.i_azure_openai_service import IAzureOpenAIService

load_dotenv(dotenv_path=".env")


container = Container()
"""The top level DI container for our application."""


# Register our dependencies ------------------------------------------------------------


@dependency_definition(container, singleton=True)
def logger() -> logging.Logger:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "ERROR"))
    logging.Formatter(fmt=" %(name)s :: %(levelname)-8s :: %(message)s")
    return logging.getLogger("azure_python")


@dependency_definition(container, singleton=True)
def azure_blob_storage_service() -> IAzureBlobStorageService:
    from azure_python.services.azure_blob_storage_service import (
        AzureBlobStorageService,
    )

    return container[AzureBlobStorageService]


@dependency_definition(container, singleton=True)
def azure_openai_service() -> IAzureOpenAIService:
    from azure_python.services.azure_openai_service import (
        AzureOpenAIService,
    )

    return container[AzureOpenAIService]
