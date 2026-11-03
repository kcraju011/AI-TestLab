from openai import (
    OpenAI,
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    InternalServerError,
    APIStatusError
)

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from app.core.config import settings
from app.services.base_llm import BaseLLMProvider


class LLMProviderError(Exception):
    pass


class OpenAILLMService(BaseLLMProvider):

    def __init__(self):

        if not settings.OPENAI_API_KEY:
            raise LLMProviderError(
                "OpenAI API key is not configured"
            )

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=settings.LLM_TIMEOUT_SECONDS,
            max_retries=0
        )

        self.model = settings.OPENAI_MODEL

    @retry(
        retry=retry_if_exception_type((
            APIConnectionError,
            APITimeoutError,
            RateLimitError,
            InternalServerError
        )),
        stop=stop_after_attempt(
            settings.LLM_MAX_RETRIES + 1
        ),
        wait=wait_exponential(
            multiplier=1,
            min=1,
            max=5
        ),
        reraise=True
    )
    def _call_api(self, question: str):

        return self.client.responses.create(
            model=self.model,
            instructions=(
                "You are a helpful product support assistant. "
                "Answer clearly. Never invent product specifications. "
                "If you do not know the answer, say so."
            ),
            input=question
        )

    def generate_response(self, question: str) -> dict:

        try:

            response = self._call_api(question)

            usage = response.usage

            return {
                "text": response.output_text,
                "provider": "openai",
                "model": self.model,
                "input_tokens": (
                    usage.input_tokens if usage else 0
                ),
                "output_tokens": (
                    usage.output_tokens if usage else 0
                )
            }

        except (
            APIConnectionError,
            APITimeoutError
        ) as error:

            raise LLMProviderError(
                "LLM connection or timeout failure"
            ) from error

        except RateLimitError as error:

            raise LLMProviderError(
                "LLM rate limit exceeded"
            ) from error

        except InternalServerError as error:

            raise LLMProviderError(
                "LLM provider server error"
            ) from error

        except APIStatusError as error:

            raise LLMProviderError(
                f"LLM provider returned HTTP {error.status_code}"
            ) from error