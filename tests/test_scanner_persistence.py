from src.jobmaxxer.models import Job
from src.jobmaxxer.storage import Store


def make_job(title: str) -> Job:
    return Job(company="Example", title=title, location="Remote", url=f"https://example.com/{title.lower().replace(' ', '-')}", source="greenhouse", description="AI backend role")


def test_first_scan_returns_new_jobs(tmp_path):
    store = Store(tmp_path / "jobs.db")
    try:
        assert store.add_jobs([make_job("AI Engineer")]) == [make_job("AI Engineer")]
    finally:
        store.close()


def test_repeated_scan_returns_no_new_jobs(tmp_path):
    store = Store(tmp_path / "jobs.db")
    job = make_job("AI Engineer")
    try:
        store.add_jobs([job])
        assert store.add_jobs([job]) == []
    finally:
        store.close()


def test_scan_returns_only_new_jobs(tmp_path):
    store = Store(tmp_path / "jobs.db")
    existing = make_job("AI Engineer")
    fresh = make_job("Backend Engineer")
    try:
        store.add_jobs([existing])
        assert store.add_jobs([existing, fresh]) == [fresh]
    finally:
        store.close()
