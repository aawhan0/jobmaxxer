from src.jobmaxxer.scanner import run


def test_scan_run_persists_new_matches(tmp_path, monkeypatch):
    companies = tmp_path / "companies.json"
    profile = tmp_path / "profile.json"
    db = tmp_path / "jobs.db"
    companies.write_text('{"companies": [{"name": "Example", "career_url": "https://example.com", "adapter": "workday"}]}')
    profile.write_text('{"target_roles": ["AI"], "skills": [], "entry_keywords": [], "preferred_locations": [], "exclude_keywords": [], "max_years_experience": 2}')
    assert run(str(companies), str(profile), str(db)) == 1
