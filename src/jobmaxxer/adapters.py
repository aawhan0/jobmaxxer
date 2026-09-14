import logging
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from .models import Job

logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
    )
}


def fetch_html(url: str, timeout: int = 20) -> str:
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text


def _looks_like_job_link(url: str, text: str) -> bool:
    haystack = f"{url} {text}".lower()
    tokens = ("job", "jobs", "career", "careers", "opening", "position", "vacancy", "apply")
    return any(token in haystack for token in tokens)


def parse_generic_html(company: str, career_url: str, html: str) -> list[Job]:
    soup = BeautifulSoup(html, "html.parser")
    jobs: list[Job] = []
    seen_urls: set[str] = set()

    for anchor in soup.find_all("a", href=True):
        title = anchor.get_text(" ", strip=True)
        href = urljoin(career_url, anchor["href"])
        if not title or href in seen_urls or not _looks_like_job_link(href, title):
            continue
        if urlparse(href).scheme not in {"http", "https"}:
            continue

        parent_text = anchor.parent.get_text(" ", strip=True) if anchor.parent else title
        location = parent_text.replace(title, " ").strip()
        jobs.append(
            Job(
                company=company,
                title=title,
                location=location,
                url=href,
                source=career_url,
                description=parent_text,
            )
        )
        seen_urls.add(href)

    return jobs


def scan_html_company(company: str, career_url: str, timeout: int = 20) -> list[Job]:
    html = fetch_html(career_url, timeout=timeout)
    return parse_generic_html(company, career_url, html)
