import re
from typing import Any

from .models import Job, MatchResult


def _contains_any(text: str, keywords: list[str]) -> list[str]:
    lowered = text.lower()
    return [keyword for keyword in keywords if keyword.lower() in lowered]


def _experience_years(text: str) -> list[int]:
    values: list[int] = []
    for match in re.findall(r"(?<!\d)(\d+)\s*\+?\s*years?", text.lower()):
        values.append(int(match))
    return values


def match_job(job: Job, profile: dict[str, Any]) -> MatchResult | None:
    combined = " ".join((job.title, job.location, job.description)).strip()
    exclude_hits = _contains_any(combined, profile.get("exclude_keywords", []))
    if exclude_hits:
        return None

    experience = _experience_years(combined)
    max_years = int(profile.get("max_years_experience", 2))
    if any(years > max_years for years in experience):
        return None

    role_hits = _contains_any(job.title, profile.get("target_roles", []))
    skill_hits = _contains_any(combined, profile.get("skills", []))
    entry_hits = _contains_any(combined, profile.get("entry_keywords", []))
    location_hits = _contains_any(job.location, profile.get("preferred_locations", []))

    score = len(role_hits) * 5 + len(skill_hits) * 2 + len(entry_hits) * 3 + len(location_hits) * 2

    if not role_hits and not skill_hits:
        return None

    reasons: list[str] = []
    if role_hits:
        reasons.append(f"target role: {role_hits[0]}")
    if skill_hits:
        reasons.append(f"skills: {', '.join(skill_hits[:4])}")
    if entry_hits:
        reasons.append(f"entry-level signal: {entry_hits[0]}")
    if location_hits:
        reasons.append(f"preferred location: {location_hits[0]}")

    return MatchResult(job=job, score=score, reasons=tuple(reasons))


def rank_matches(jobs: list[Job], profile: dict[str, Any]) -> list[MatchResult]:
    matches = [result for job in jobs if (result := match_job(job, profile)) is not None]
    return sorted(matches, key=lambda item: (-item.score, item.job.company.lower(), item.job.title.lower()))
