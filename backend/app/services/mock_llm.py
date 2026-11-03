from app.services.base_llm import BaseLLMProvider


class MockLLMService(BaseLLMProvider):

    def generate_response(
        self,
        question: str,
        expected_answer: str = "",
        scenario: str = "correct"
    ) -> dict:

        if scenario == "correct":
            answer = expected_answer

        elif scenario == "incorrect":
            answer = (
                "I cannot provide accurate information "
                "about this topic."
            )

        elif scenario == "empty":
            answer = ""

        else:
            answer = "Unknown response"

        return {
            "text": answer,
            "provider": "mock",
            "model": "mock-model",
            "input_tokens": 0,
            "output_tokens": 0
        }