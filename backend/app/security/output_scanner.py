import re


OUTPUT_PATTERNS = {
    "synthetic_secret": (
        r"AI_TESTLAB_SECRET_[A-Z0-9]+"
    ),

    "api_key": (
        r"\bsk-[A-Za-z0-9_-]{20,}\b"
    ),

    "aws_access_key": (
        r"\bAKIA[0-9A-Z]{16}\b"
    ),

    "password": (
        r"\bpassword\s*[:=]\s*\S+"
    ),

    "email": (
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )
}


class OutputSecurityScanner:

    def scan(self, response: str):

        findings = []

        for category, pattern in OUTPUT_PATTERNS.items():

            matches = re.findall(
                pattern,
                response,
                flags=re.IGNORECASE
            )

            if matches:
                findings.append({
                    "category": category,
                    "severity": (
                        "critical"
                        if category in [
                            "synthetic_secret",
                            "api_key",
                            "aws_access_key",
                            "password"
                        ]
                        else "medium"
                    ),
                    "count": len(matches),
                    "description": (
                        f"Potential {category.replace('_', ' ')} "
                        "exposure detected."
                    )
                })

        detected = len(findings) > 0

        return {
            "detected": detected,
            "findings": findings,
            "status": "BLOCK" if detected else "ALLOW"
        }