import re


class BasicEvaluator:

    def evaluate(
        self,
        expected_answer: str,
        actual_answer: str
    ) -> dict:

        expected_words = set(
            re.findall(r"\b\w+\b", expected_answer.lower())
        )

        actual_words = set(
            re.findall(r"\b\w+\b", actual_answer.lower())
        )

        if not expected_words or not actual_words:
            score = 0.0

        else:
            common_words = expected_words.intersection(
                actual_words
            )

            score = len(common_words) / len(expected_words)

        score = round(score, 2)

        status = "PASS" if score >= 0.70 else "FAIL"

        return {
            "score": score,
            "status": status
        }