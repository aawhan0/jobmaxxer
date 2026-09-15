import re
from typing import Any

from .models import Job, MatchResult


TECHNICAL_TITLE_KEYWORDS = (
    "software", "engineer", "developer", "backend", "frontend", "full stack",
    "full-stack", "data scientist", "data engineer", "machine learning", "ai",
    "artificial intelligence", "ml", "platform", "devops", "infrastructure",
    "research", "qa engineer", "automation engineer", "technical",
)


def _normalise(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def _contains_any(text: str, keywords: list[str]) -> list[str]:
    lowered = _normalise(text)
    return [keyword for keyword in keywords if _normalise(keyword) in lowered]


def _experience_years(text: str) -> list[int]:
    return [int(value) for value in re.findall(r"(?<!\d)(\d+)\s*\+?\s*years?", text.lower())]


def _technical_title(title: str) -> bool:
    lowered = _normalise(title)
    return any(_normalise(keyword) in lowered for keyword in TECHNICAL_TITLE_KEYWORDS)


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

    if not role_hits and not (skill_hits and _technical_title(job.title)):
        return None

    # Title evidence is stronger than a skill mention buried in a description.
    title_skill_hits = _contains_any(job.title, profile.get("skills", []))
    score = (
        len(role_hits) * 6
        + len(title_skill_hits) * 3
        + len(skill_hits) * 1
        + len(entry_hits) * 3
        + len(location_hits) * 2
    )

    reasons: list[str] = []
    if role_hits:
        reasons.append(f"target role: {role_hits[0]}")
    if title_skill_hits:
        reasons.append(f"title skills: {', '.join(title_skill_hits[:4])}")
    elif skill_hits:
        reasons.append(f"skills: {', '.join(skill_hits[:4])}")
    if entry_hits:
        reasons.append(f"entry-level signal: {entry_hits[0]}")
    if location_hits:
        reasons.append(f"preferred location: {location_hits[0]}")

    return MatchResult(job=job, score=score, reasons=tuple(reasons))


def rank_matches(jobs: list[Job], profile: dict[str, Any]) -> list[MatchResult]:
    matches = [result for job in jobs if (result := match_job(job, profile)) is not None]
    return sorted(matches, key=lambda item: (-item.score, item.job.company.lower(), item.job.title.lower()))
