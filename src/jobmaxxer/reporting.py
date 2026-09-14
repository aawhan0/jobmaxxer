"""Export and summary helpers for scan results."""
from __future__ import annotations
import csv
import json
from pathlib import Path
from typing import Iterable
from .models import MatchResult


def export_jobs(results: Iterable[MatchResult], path: str | Path, fmt: str | None = None) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    rows = [{"company": r.job.company, "title": r.job.title, "location": r.job.location, "url": r.job.url, "score": r.score, "reasons": "; ".join(r.reasons)} for r in results]
    fmt = (fmt or target.suffix.lstrip(".") or "json").lower()
    if fmt == "csv":
        with target.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=rows[0].keys() if rows else ["company", "title", "location", "url", "score", "reasons"])
            writer.writeheader(); writer.writerows(rows)
    else:
        target.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    return target


def summarize(scan_count: int, new_count: int, matched_count: int, failures: int) -> dict[str, int]:
    return {"companies_scanned": scan_count, "new_jobs": new_count, "matches": matched_count, "failures": failures}
