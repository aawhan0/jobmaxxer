"""Provider-aware job ingestion helpers."""
from __future__ import annotations
from typing import Any, Iterable
from urllib.parse import urlparse, urlunparse
from .ats import detect_ats
from .models import Job

def normalize_url(url: str) -> str:
    p = urlparse(url.strip())
    return urlunparse((p.scheme.lower(), p.netloc.lower(), p.path.rstrip('/'), '', p.query, ''))

def _job(company: str, item: dict[str, Any], source: str) -> Job:
    location = item.get('location') or item.get('locations') or item.get('workplace_type') or ''
    if isinstance(location, list): location = ', '.join(map(str, location))
    url = normalize_url(str(item.get('url') or item.get('absolute_url') or item.get('apply_url') or ''))
    return Job(company=company, title=str(item.get('title') or item.get('name') or 'Untitled role').strip(), location=str(location), url=url, source=source, description=str(item.get('description') or item.get('content') or ''), external_id=str(item.get('id') or item.get('requisition_id') or url))

def parse_greenhouse_payload(company: str, payload: dict[str, Any]) -> list[Job]: return [_job(company, x, 'greenhouse') for x in payload.get('jobs', []) if isinstance(x, dict)]
def parse_lever_payload(company: str, payload: list[dict[str, Any]]) -> list[Job]: return [_job(company, x, 'lever') for x in payload if isinstance(x, dict)]
def parse_ashby_payload(company: str, payload: dict[str, Any]) -> list[Job]: return [_job(company, x, 'ashby') for x in payload.get('jobs', []) if isinstance(x, dict)]
def parse_workable_payload(company: str, payload: dict[str, Any]) -> list[Job]: return [_job(company, x, 'workable') for x in payload.get('jobs', []) if isinstance(x, dict)]
def parse_workday_payload(company: str, payload: dict[str, Any]) -> list[Job]: return [_job(company, x, 'workday') for x in (payload.get('jobPostings') or payload.get('jobs') or payload.get('data') or []) if isinstance(x, dict)]
def provider_for(url: str, adapter: str | None = None) -> str: return (adapter or detect_ats(url) or 'html').lower()
def deduplicate(jobs: Iterable[Job]) -> list[Job]:
    seen, result = set(), []
    for job in jobs:
        if job.fingerprint not in seen: seen.add(job.fingerprint); result.append(job)
    return result
