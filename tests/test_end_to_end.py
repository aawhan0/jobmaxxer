from pathlib import Path

from jobmaxxer.models import Job
from jobmaxxer.storage import Store


def test_store_round_trip_and_deduplication(tmp_path: Path):
    db = tmp_path / "jobs.db"
    job = Job(
        company="Example",
        title="AI Engineer",
        location="Remote",
        url="https://example.com/jobs/1",
        source="greenhouse",
    )
    store = Store(str(db))
    try:
        first = store.add_jobs([job])
        second = store.add_jobs([job])
    finally:
        store.close()

    assert first == [job]
    assert second == []
