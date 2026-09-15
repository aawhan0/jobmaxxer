"""Conservative adapter for publicly accessible HTML career pages."""
from __future__ import annotations

from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from .models import Job


class _Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href = ""
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self._href = dict(attrs).get("href") or ""
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._href:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href:
            text = " ".join("".join(self._text).split())
            if text:
                self.links.append((text, self._href))
            self._href, self._text = "", []


def _is_job_link(title: str, href: str) -> bool:
    lowered = f"{title} {href}".lower()
    if any(token in lowered for token in ("about", "contact", "privacy", "terms", "cookie")):
        return False
    return any(token in lowered for token in ("/job", "/careers", "career", "engineer", "developer", "intern", "analyst", "vacancy", "opening"))


def scan_html(company: str, url: str, timeout: int = 20) -> list[Job]:
    request = Request(url, headers={"User-Agent": "jobmaxxer/1.0"})
    with urlopen(request, timeout=timeout) as response:
        html = response.read().decode("utf-8", errors="replace")

    parser = _Links()
    parser.feed(html)
    jobs: list[Job] = []
    seen: set[str] = set()
    for title, href in parser.links:
        if not _is_job_link(title, href):
            continue
        absolute = urljoin(url, href)
        parsed = urlparse(absolute)
        if parsed.scheme not in {"http", "https"} or absolute in seen:
            continue
        seen.add(absolute)
        jobs.append(Job(company=company, title=title, location="", url=absolute, source="html"))
    return jobs
