import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    OPENAI_MODEL = os.getenv(
        "OPENAI_MODEL",
        "gpt-4.1-mini"
    )

    DEEPEVAL_MODEL = os.getenv(
        "DEEPEVAL_MODEL",
        "gpt-4.1-mini"
    )

    LLM_TIMEOUT_SECONDS = float(
        os.getenv("LLM_TIMEOUT_SECONDS", "20")
    )

    LLM_MAX_RETRIES = int(
        os.getenv("LLM_MAX_RETRIES", "2")
    )


settings = Settings()