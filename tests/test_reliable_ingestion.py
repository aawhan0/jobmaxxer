from src.jobmaxxer.providers import deduplicate
from src.jobmaxxer.models import Job


def make_job(url: str) -> Job:
    return Job(
        company="Example",
        title="Backend Engineer",
        location="Remote",
        url=url,
        source="test",
        description="",
        external_id=url,
    )


def test_deduplicate_removes_repeated_jobs():
    first = make_job("https://example.com/jobs/1")
    duplicate = make_job("https://example.com/jobs/1")
    second = make_job("https://example.com/jobs/2")

    result = deduplicate([first, duplicate, second])

    assert result == [first, second]


def test_deduplicate_preserves_first_seen_order():
    jobs = [make_job(f"https://example.com/jobs/{index}") for index in range(3)]

    assert deduplicate(jobs) == jobs
