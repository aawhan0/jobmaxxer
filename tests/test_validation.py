import pytest

from jobmaxxer.validation import validate_companies, validate_or_raise


def test_valid_company_config():
    assert validate_companies({"companies": [{"name": "Acme", "career_url": "https://acme.test/careers"}]}) == []


def test_invalid_company_config():
    errors = validate_companies({"companies": [{"name": "Acme"}]})
    assert "companies[0] missing career_url" in errors


def test_validate_or_raise():
    with pytest.raises(ValueError):
        validate_or_raise({"companies": "bad"})
