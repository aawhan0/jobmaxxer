"""Notification helpers that keep delivery optional and side-effect free."""

from __future__ import annotations

from collections.abc import Iterable

from .models import MatchResult


def format_match(result: MatchResult) -> str:
    """Format one match for terminal, log, or future notification delivery."""
    job = result.job
    reason = "; ".join(result.reasons) if result.reasons else "matched profile"
    return f"{job.company} — {job.title} ({job.location})\n{job.url}\n{reason}"


def format_digest(results: Iterable[MatchResult], limit: int = 10) -> str:
    """Format a bounded digest without sending messages or requiring credentials."""
    items = list(results)[: max(0, limit)]
    if not items:
        return "No new matching jobs."
    return "\n\n".join(format_match(item) for item in items)
