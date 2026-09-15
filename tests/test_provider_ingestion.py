from unittest.mock import patch

import pytest

from src.jobmaxxer.providers import scan_company
from src.jobmaxxer.scan_errors import ScanError


def test_greenhouse_scan_uses_structured_endpoint():
    payload = {"jobs": [{"id": 7, "title": "AI Engineer", "location": {"name": "Remote"}, "absolute_url": "https://example.com/jobs/7"}]}
    with patch("src.jobmaxxer.providers._fetch_json", return_value=payload) as fetch:
        jobs = scan_company("Example", "https://boards.greenhouse.io/example")
    fetch.assert_called_once()
    assert jobs[0].title == "AI Engineer"
    assert jobs[0].source == "greenhouse"


def test_unsupported_provider_fails_clearly():
    with pytest.raises(ScanError, match="workday"):
        scan_company("Example", "https://jobs.example.com/careers", "workday")
