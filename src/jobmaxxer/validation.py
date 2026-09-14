from __future__ import annotations

from typing import Any

REQUIRED_COMPANY_KEYS = {"name", "career_url"}


def validate_companies(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    companies = config.get("companies")
    if not isinstance(companies, list):
        return ["companies must be a list"]
    for index, company in enumerate(companies):
        if not isinstance(company, dict):
            errors.append(f"companies[{index}] must be an object")
            continue
        missing = REQUIRED_COMPANY_KEYS - company.keys()
        errors.extend(f"companies[{index}] missing {key}" for key in sorted(missing))
        if "career_url" in company and not str(company["career_url"]).startswith(("http://", "https://")):
            errors.append(f"companies[{index}].career_url must be an HTTP(S) URL")
    return errors


def validate_or_raise(config: dict[str, Any]) -> None:
    errors = validate_companies(config)
    if errors:
        raise ValueError("Invalid company configuration: " + "; ".join(errors))
