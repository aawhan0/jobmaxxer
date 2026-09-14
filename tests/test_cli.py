from src.jobmaxxer.cli import format_match
from src.jobmaxxer.models import Job, MatchResult


def test_format_match_contains_application_details():
    result = MatchResult(Job("Acme", "AI Engineer", "Remote", "https://example.com/job", "https://example.com/careers"), 10, ("target role",))
    output = format_match(result)
    assert "Acme" in output
    assert "AI Engineer" in output
    assert "https://example.com/job" in output
