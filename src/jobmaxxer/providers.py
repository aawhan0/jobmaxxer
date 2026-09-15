"""Provider-aware job ingestion helpers."""
from __future__ import annotations

import json
from typing import Any, Iterable
from urllib.parse import urlparse, urlunparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from .ats import detect_ats
from .models import Job
from .scan_errors import ScanError
from .adapters import scan_html_company


def normalize_url(url: str) -> str:
    p = urlparse(url.strip())
    return urlunparse((p.scheme.lower(), p.netloc.lower(), p.path.rstrip('/'), '', p.query, ''))


def _job(company: str, item: dict[str, Any], source: str) -> Job:
    location = item.get('location') or item.get('locations') or item.get('workplace_type') or ''
    if isinstance(location, list):
        location = ', '.join(map(str, location))
    url = normalize_url(str(item.get('url') or item.get('absolute_url') or item.get('apply_url') or ''))
    return Job(company=company, title=str(item.get('title') or item.get('name') or 'Untitled role').strip(), location=str(location), url=url, source=source, description=str(item.get('description') or item.get('content') or ''), external_id=str(item.get('id') or item.get('requisition_id') or url))


def parse_greenhouse_payload(company: str, payload: dict[str, Any]) -> list[Job]:
    return [_job(company, x, 'greenhouse') for x in payload.get('jobs', []) if isinstance(x, dict)]


def parse_lever_payload(company: str, payload: list[dict[str, Any]]) -> list[Job]:
    return [_job(company, x, 'lever') for x in payload if isinstance(x, dict)]


def parse_ashby_payload(company: str, payload: dict[str, Any]) -> list[Job]:
    return [_job(company, x, 'ashby') for x in payload.get('jobs', []) if isinstance(x, dict)]


def parse_workable_payload(company: str, payload: dict[str, Any]) -> list[Job]:
    return [_job(company, x, 'workable') for x in payload.get('jobs', []) if isinstance(x, dict)]


def parse_workday_payload(company: str, payload: dict[str, Any]) -> list[Job]:
    return [_job(company, x, 'workday') for x in (payload.get('jobPostings') or payload.get('jobs') or payload.get('data') or []) if isinstance(x, dict)]


def provider_for(url: str, adapter: str | None = None) -> str:
    return (adapter or detect_ats(url) or 'html').lower()


def deduplicate(jobs: Iterable[Job]) -> list[Job]:
    seen, result = set(), []
    for job in jobs:
        if job.fingerprint not in seen:
            seen.add(job.fingerprint)
            result.append(job)
    return result


def _fetch_json(url: str, timeout: int = 20) -> Any:
    request = Request(url, headers={'User-Agent': 'jobmaxxer/1.0', 'Accept': 'application/json'})
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as exc:
        raise ScanError(f'Provider returned HTTP {exc.code} for {url}') from exc
    except URLError as exc:
        raise ScanError(f'Provider request failed for {url}: {exc.reason}') from exc
    except (TimeoutError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ScanError(f'Provider response was invalid for {url}: {exc}') from exc


def _slug(url: str) -> str:
    parts = [part for part in urlparse(url).path.split('/') if part]
    return parts[-1] if parts else urlparse(url).netloc.split('.')[0]


def scan_company(company: str, url: str, adapter: str | None = None, timeout: int = 20) -> list[Job]:
    """Fetch jobs from a supported ATS, with recoverable provider errors."""
    provider = provider_for(url, adapter)
    slug = _slug(url)
    if provider == 'greenhouse':
        return parse_greenhouse_payload(company, _fetch_json(f'https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true', timeout))
    if provider == 'lever':
        return parse_lever_payload(company, _fetch_json(f'https://api.lever.co/v0/postings/{slug}?mode=json', timeout))
    if provider == 'html':
        return scan_html_company(company, url, timeout=timeout)
    raise ScanError(f'No structured API adapter configured for provider: {provider}')
