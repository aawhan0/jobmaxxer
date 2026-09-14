"""Small, dependency-light ATS URL helpers."""
from __future__ import annotations

from urllib.parse import urlparse


def detect_ats(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if "greenhouse.io" in host:
        return "greenhouse"
    if "lever.co" in host:
        return "lever"
    if "ashbyhq.com" in host:
        return "ashby"
    if "workable.com" in host:
        return "workable"
    if "myworkdayjobs.com" in host or "workday.com" in host:
        return "workday"
    return "html"


def normalize_job_url(url: str) -> str:
    return url.split("#", 1)[0].rstrip("/")
