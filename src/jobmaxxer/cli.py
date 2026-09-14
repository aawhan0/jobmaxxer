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
