import re
from urllib.parse import urlparse

import requests

from .models import Job
from .ats import detect_ats
from .adapters import DEFAULT_HEADERS, parse_generic_html


def _board_slug(url: str) -> str | None:
    path = urlparse(url).path.strip('/').split('/')
    for marker in ('boards', 'companies'):
        if marker in path:
            index = path.index(marker)
            if index + 1 < len(path):
                return path[index + 1]
    return None


def _json(url: str, timeout: int) -> object:
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.json()


def scan_greenhouse(company: str, url: str, timeout: int = 20) -> list[Job]:
    slug = _board_slug(url)
    if not slug:
        raise ValueError('Greenhouse board slug not found')
    data = _json(f'https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true', timeout)
    return [_job(company, url, item, 'greenhouse') for item in data.get('jobs', [])]


def scan_lever(company: str, url: str, timeout: int = 20) -> list[Job]:
    slug = _board_slug(url)
    if not slug:
        raise ValueError('Lever board slug not found')
    data = _json(f'https://api.lever.co/v0/postings/{slug}?mode=json', timeout)
    return [_job(company, url, item, 'lever') for item in data]


def _job(company: str, source: str, item: dict, provider: str) -> Job:
    location = item.get('location') or item.get('location', {}).get('name', '') if isinstance(item.get('location'), dict) else item.get('location', '')
    description = item.get('content') or item.get('descriptionPlain') or item.get('description') or ''
    link = item.get('absolute_url') or item.get('hostedUrl') or item.get('applyUrl') or item.get('url') or source
    return Job(company=company, title=item.get('title', '').strip(), location=str(location), url=link, source=source, description=description, external_id=str(item.get('id', '')))


def scan_company(company: str, url: str, adapter: str | None = None, timeout: int = 20) -> list[Job]:
    provider = adapter or detect_ats(url)
    if provider == 'greenhouse':
        return scan_greenhouse(company, url, timeout)
    if provider == 'lever':
        return scan_lever(company, url, timeout)
    return parse_generic_html(company, url, __import__('src.jobmaxxer.adapters', fromlist=['fetch_html']).fetch_html(url, timeout))
