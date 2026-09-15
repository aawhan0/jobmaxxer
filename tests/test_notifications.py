from jobmaxxer.models import Job, MatchResult
from jobmaxxer.notifications import format_digest, format_match


def test_format_match_contains_actionable_job_details():
    job = Job(company="Acme", title="AI Engineer", location="Remote", url="https://example.com/job", source="html")
    text = format_match(MatchResult(job=job, score=8, reasons=["skill: python"]))
    assert "Acme" in text
    assert "AI Engineer" in text
    assert "Location: Remote" in text
    assert "Match score: 8" in text
    assert "Why: skill: python" in text
    assert "Apply: https://example.com/job" in text


def test_format_digest_has_header_and_limit():
    job = Job(company="Acme", title="AI Engineer", location="Remote", url="https://example.com/job", source="html")
    result = MatchResult(job=job, score=8, reasons=["skill: python"])
    text = format_digest([result], limit=1)
    assert text.startswith("Jobmaxxer: 1 new matching job(s)")
    assert text.count("Apply:") == 1


def test_format_digest_empty():
    assert format_digest([]) == "No new matching jobs."
