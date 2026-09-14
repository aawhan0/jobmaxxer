from jobmaxxer.models import Job, MatchResult
from jobmaxxer.reporting import export_jobs, summarize


def test_summary():
    assert summarize(4, 3, 2, 1) == {"companies_scanned": 4, "new_jobs": 3, "matches": 2, "failures": 1}


def test_json_export(tmp_path):
    job = Job(company="Acme", title="AI Engineer", location="Remote", url="https://example.com/jobs/1", source="test", description="python")
    path = export_jobs([MatchResult(job=job, score=8, reasons=["role"])], tmp_path / "jobs.json")
    assert path.exists()
    assert "AI Engineer" in path.read_text()
