from jobmaxxer.models import Job, MatchResult
from jobmaxxer.notifications import format_digest, format_match


def test_format_match_contains_job_details():
    job = Job(company="Acme", title="AI Engineer", location="Remote", url="https://example.com/job", source="html")
    text = format_match(MatchResult(job=job, score=8, reasons=["skill: python"]))
    assert "Acme" in text
    assert "AI Engineer" in text
    assert "skill: python" in text


def test_format_digest_empty():
    assert format_digest([]) == "No new matching jobs."
