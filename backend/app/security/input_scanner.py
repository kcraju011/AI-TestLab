import re


ATTACK_PATTERNS = {
    "prompt_injection": [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"disregard\s+(all\s+)?(previous\s+)?instructions",
        r"reveal\s+(your\s+)?system\s+prompt",
        r"reveal\s+(your\s+)?developer\s+instructions",
        r"disclose\s+confidential\s+data",
        r"override\s+(the\s+)?system\s+prompt"
    ],

    "jailbreak": [
        r"unrestricted\s+ai",
        r"without\s+(any\s+)?safety\s+rules",
        r"bypass\s+(your\s+)?safety",
        r"ignore\s+(your\s+)?safety\s+policy",
        r"act\s+as\s+an?\s+unrestricted"
    ]
}


class InputSecurityScanner:

    def scan(self, prompt: str):

        findings = []

        normalized_prompt = prompt.lower()

        for category, patterns in ATTACK_PATTERNS.items():

            for pattern in patterns:

                if re.search(pattern, normalized_prompt):
                    findings.append({
                        "category": category,
                        "severity": "high",
                        "description": (
                            f"Potential {category.replace('_', ' ')} detected."
                        )
                    })

                    break

        detected = len(findings) > 0

        return {
            "detected": detected,
            "findings": findings,
            "status": "BLOCK" if detected else "ALLOW"
        }