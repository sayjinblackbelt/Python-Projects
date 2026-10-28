"""Detecção e mascaramento básico de dados potencialmente sensíveis."""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    """Representa um dado potencialmente sensível encontrado."""

    category: str
    value: str
    start: int
    end: int


def is_valid_cpf(value: str) -> bool:
    """Valida os dígitos verificadores de um CPF."""
    digits = re.sub(r"\D", "", value)

    if len(digits) != 11 or len(set(digits)) == 1:
        return False

    first_sum = sum(
        int(digit) * weight
        for digit, weight in zip(digits[:9], range(10, 1, -1))
    )
    first_digit = (first_sum * 10 % 11) % 10

    second_sum = sum(
        int(digit) * weight
        for digit, weight in zip(digits[:10], range(11, 1, -1))
    )
    second_digit = (second_sum * 10 % 11) % 10

    return digits[-2:] == f"{first_digit}{second_digit}"


PATTERNS = {
    "EMAIL": re.compile(
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        re.IGNORECASE,
    ),
    "CPF": re.compile(
        r"(?<!\d)(?:\d{3}\.?\d{3}\.?\d{3}-?\d{2})(?!\d)"
    ),
    "TELEFONE": re.compile(
        r"(?<!\d)(?:\+?55\s?)?"
        r"\(?\d{2}\)?[\s.-]?"
        r"\d{4,5}[\s.-]?\d{4}(?!\d)"
    ),
    "TOKEN": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|secret)"
        r"\s*[:=]\s*['\"]?([A-Za-z0-9._-]{12,})"
    ),
}


def scan_text(text: str) -> list[Finding]:
    """Localiza padrões potencialmente sensíveis no texto."""
    if not isinstance(text, str):
        raise TypeError("O texto precisa ser uma string.")

    findings: list[Finding] = []

    for category, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            finding_category = category

            if category == "TOKEN" and match.lastindex:
                start, end = match.span(1)
                value = match.group(1)
            else:
                start, end = match.span()
                value = match.group()

                if category == "CPF" and not is_valid_cpf(value):
                    finding_category = "CPF_SUSPEITO"

            findings.append(
                Finding(
                    category=finding_category,
                    value=value,
                    start=start,
                    end=end,
                )
            )

    findings.sort(key=lambda item: (item.start, item.end))
    filtered: list[Finding] = []

    for finding in findings:
        if filtered and finding.start < filtered[-1].end:
            continue
        filtered.append(finding)

    return filtered


def mask_text(text: str) -> str:
    """Substitui dados detectados por marcadores de categoria."""
    findings = scan_text(text)

    for finding in reversed(findings):
        text = (
            text[:finding.start]
            + f"[{finding.category}]"
            + text[finding.end:]
        )

    return text
