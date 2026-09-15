import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .models import Job

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    fingerprint TEXT PRIMARY KEY,
    company TEXT NOT NULL,
    title TEXT NOT NULL,
    location TEXT NOT NULL,
    url TEXT NOT NULL,
    source TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    external_id TEXT NOT NULL DEFAULT '',
    first_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scan_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    success INTEGER NOT NULL,
    job_count INTEGER NOT NULL DEFAULT 0,
    error TEXT,
    scanned_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


class Store:
    def __init__(self, db_path: str | Path = "jobmaxxer.db") -> None:
        self.db_path = str(db_path)
        self._connection = sqlite3.connect(self.db_path)
        self._connection.row_factory = sqlite3.Row
        self._connection.executescript(SCHEMA)
        self._connection.commit()

    def close(self) -> None:
        self._connection.close()

    def seen(self, job: Job) -> bool:
        row = self._connection.execute(
            "SELECT 1 FROM jobs WHERE fingerprint = ?", (job.fingerprint,)
        ).fetchone()
        return row is not None

    def count_seen(self, jobs: Iterable[Job]) -> int:
        return sum(1 for job in jobs if self.seen(job))

    def upsert_job(self, job: Job) -> bool:
        is_new = not self.seen(job)
        self._connection.execute(
            """
            INSERT INTO jobs (
                fingerprint, company, title, location, url, source,
                description, external_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(fingerprint) DO UPDATE SET
                title = excluded.title,
                location = excluded.location,
                url = excluded.url,
                source = excluded.source,
                description = excluded.description,
                external_id = excluded.external_id,
                last_seen_at = CURRENT_TIMESTAMP
            """,
            (job.fingerprint, job.company, job.title, job.location, job.url,
             job.source, job.description, job.external_id),
        )
        self._connection.commit()
        return is_new

    def record_scan(self, company: str, success: bool, job_count: int, error: str | None = None) -> None:
        self._connection.execute(
            "INSERT INTO scan_runs (company, success, job_count, error) VALUES (?, ?, ?, ?)",
            (company, int(success), job_count, error),
        )
        self._connection.commit()

    def add_jobs(self, jobs: Iterable[Job]) -> list[Job]:
        new_jobs: list[Job] = []
        for job in jobs:
            if self.upsert_job(job):
                new_jobs.append(job)
        return new_jobs

    def jobs_not_seen_since(self, since: datetime, company: str | None = None) -> list[Job]:
        """Return stored jobs not observed since the supplied UTC timestamp."""
        timestamp = since.astimezone(timezone.utc).replace(tzinfo=None).isoformat(sep=" ")
        query = "SELECT * FROM jobs WHERE last_seen_at < ?"
        params: list[str] = [timestamp]
        if company is not None:
            query += " AND company = ?"
            params.append(company)
        rows = self._connection.execute(query, params).fetchall()
        return [Job(row["company"], row["title"], row["location"], row["url"], row["source"], row["description"], row["external_id"]) for row in rows]
