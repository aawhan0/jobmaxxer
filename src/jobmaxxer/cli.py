from pathlib import Path

from .models import MatchResult


def format_match(result: MatchResult) -> str:
    job = result.job
    return "\n".join([
        "NEW MATCH",
        f"Company: {job.company}",
        f"Role: {job.title}",
        f"Location: {job.location or 'Not listed'}",
        f"Match: {result.match_reason}",
        f"Source: {job.source}",
        f"Apply: {job.url}",
    ])


def output_path(value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value)
    if path.suffix.lower() not in {".json", ".csv"}:
        raise ValueError("Export path must end in .json or .csv")
    return path
