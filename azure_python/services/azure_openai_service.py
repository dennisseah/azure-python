from dataclasses import dataclass
from typing import Any, Callable

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from lagom.environment import Env
from openai import AsyncAzureOpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
)

from azure_python.models.llm_response import LLMResponse
from azure_python.protocols.i_azure_openai_service import (
    IAzureOpenAIService,
)


class AzureOpenAIServiceEnv(Env):
    azure_openai_endpoint: str
    azure_openai_api_key: str | None = None
    azure_openai_api_version: str
    azure_openai_deployed_model_name: str


@dataclass
class AzureOpenAIService(IAzureOpenAIService):
    """
    Azure OpenAI Service implementation.
    """

    env: AzureOpenAIServiceEnv

    def __post_init__(self) -> None:
        self.client = self.get_client()

    def get_openai_auth_key(self) -> dict[str, str | Callable[[], str]]:
        if self.env.azure_openai_api_key:
            return {"api_key": self.env.azure_openai_api_key}

        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        )

        return {"azure_ad_token_provider": token_provider}

    def get_client(self) -> AsyncAzureOpenAI:
        return AsyncAzureOpenAI(
            azure_endpoint=self.env.azure_openai_endpoint,
            api_version=self.env.azure_openai_api_version,
            **self.get_openai_auth_key(),  # type: ignore
        )

    def get_deployed_model_name(self) -> str:
        return self.env.azure_openai_deployed_model_name

    async def chat_completion(
        self, messages: list[ChatCompletionMessageParam], temperature: float = 1.0
    ) -> LLMResponse:
        self.client = self.get_client()
        response = await self.client.chat.completions.create(
            model=self.env.azure_openai_deployed_model_name,
            messages=messages,
            temperature=temperature,
        )

        usages = response.usage.model_dump() if response.usage else {}
        usages = {k: v for k, v in usages.items() if isinstance(v, int)}

        return LLMResponse(
            content=response.choices[0].message.content if response.choices else "",
            finish_reason=response.choices[0].finish_reason if response.choices else "",
            usages=usages,
        )

    async def chat_completion_with_format(
        self,
        messages: list[ChatCompletionMessageParam],
        response_format: Any,
        temperature: float = 1.0,
    ) -> LLMResponse:
        try:
            self.client = self.get_client()
            response = await self.client.chat.completions.parse(
                model=self.env.azure_openai_deployed_model_name,
                messages=messages,
                response_format=response_format,
                temperature=temperature,
            )

            usages = response.usage.model_dump() if response.usage else {}
            usages = {k: v for k, v in usages.items() if isinstance(v, int)}

            return LLMResponse(
                content=response.choices[0].message.content if response.choices else "",
                finish_reason=response.choices[0].finish_reason
                if response.choices
                else "",
                usages=usages,
            )
        except Exception as e:
            return LLMResponse(content=str(e), finish_reason="error", usages={})
