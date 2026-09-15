from collections import Counter
from typing import Any

from .filtering import match_job
from .models import Job


def summarize_filtering(jobs: list[Job], profile: dict[str, Any]) -> dict[str, int]:
    counts = Counter()
    for job in jobs:
        combined = " ".join((job.title, job.location, job.description)).lower()
        if any(str(value).lower() in combined for value in profile.get("exclude_keywords", [])):
            counts["excluded_keyword"] += 1
        elif match_job(job, profile) is None:
            counts["not_relevant"] += 1
        else:
            counts["matched"] += 1
    counts["total"] = len(jobs)
    return dict(counts)
