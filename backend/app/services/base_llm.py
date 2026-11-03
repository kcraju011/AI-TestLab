from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate_response(
        self,
        question: str,
        expected_answer: str = "",
        scenario: str = "correct"
    ) -> dict:
        pass