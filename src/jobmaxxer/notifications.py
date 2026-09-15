"""Notification helpers that keep delivery optional and side-effect free."""

from __future__ import annotations

from collections.abc import Iterable

from .models import MatchResult


def format_match(result: MatchResult) -> str:
    """Format one match for terminal, log, or notification delivery."""
    job = result.job
    reason = "; ".join(result.reasons) if result.reasons else "matched profile"
    return (
        f"{job.company} — {job.title}\n"
        f"Location: {job.location}\n"
        f"Match score: {result.score}\n"
        f"Why: {reason}\n"
        f"Apply: {job.url}"
    )


def format_digest(results: Iterable[MatchResult], limit: int = 10) -> str:
    """Format a bounded, actionable digest without sending messages or requiring credentials."""
    items = list(results)[: max(0, limit)]
    if not items:
        return "No new matching jobs."
    header = f"Jobmaxxer: {len(items)} new matching job(s)"
    return header + "\n\n" + "\n\n".join(format_match(item) for item in items)
