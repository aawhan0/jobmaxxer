from datetime import datetime, timezone

from src.jobmaxxer.models import Job
from src.jobmaxxer.storage import Store


def test_store_only_reports_first_seen_job(tmp_path):
    store = Store(tmp_path / "jobs.db")
    job = Job("Example", "AI Engineer", "India", "https://example.com/job/1", "https://example.com/careers")
    assert store.upsert_job(job) is True
    assert store.upsert_job(job) is False
    store.close()


def test_jobs_not_seen_since_returns_existing_stale_jobs(tmp_path):
    store = Store(tmp_path / "jobs.db")
    job = Job("Example", "AI Engineer", "India", "https://example.com/job/2", "https://example.com/careers")
    assert store.upsert_job(job) is True
    stale = store.jobs_not_seen_since(datetime.now(timezone.utc))
    assert [item.url for item in stale] == [job.url]
    store.close()
