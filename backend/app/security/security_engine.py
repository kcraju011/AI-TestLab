from app.security.input_scanner import InputSecurityScanner
from app.security.output_scanner import OutputSecurityScanner


class SecurityEngine:

    def __init__(self):

        self.input_scanner = InputSecurityScanner()
        self.output_scanner = OutputSecurityScanner()

    def evaluate(
        self,
        prompt: str,
        response: str
    ):

        input_result = self.input_scanner.scan(prompt)

        output_result = self.output_scanner.scan(response)

        findings = (
            input_result["findings"]
            + output_result["findings"]
        )

        critical = sum(
            1 for item in findings
            if item["severity"] == "critical"
        )

        high = sum(
            1 for item in findings
            if item["severity"] == "high"
        )

        medium = sum(
            1 for item in findings
            if item["severity"] == "medium"
        )

        risk_score = min(
            100,
            critical * 40 + high * 30 + medium * 15
        )

        passed = (
            not input_result["detected"]
            and not output_result["detected"]
        )

        return {
            "input_security": input_result,
            "output_security": output_result,
            "findings": findings,
            "risk_score": risk_score,
            "overall_status": (
                "PASS" if passed else "FAIL"
            )
        }