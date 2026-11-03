class MockLLMService:

    def generate_response(
        self,
        question: str,
        expected_answer: str,
        scenario: str = "correct"
    ) -> str:

        if scenario == "correct":
            return expected_answer

        elif scenario == "incorrect":
            return "I cannot provide accurate information about this topic."

        elif scenario == "empty":
            return ""

        return "Unknown response"