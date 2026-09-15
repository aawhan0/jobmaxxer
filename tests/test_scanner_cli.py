from pathlib import Path

from scanner import run


def test_run_returns_success_for_empty_company_config(tmp_path, capsys):
    companies = tmp_path / "companies.json"
    profile = tmp_path / "profile.json"
    db = tmp_path / "jobs.db"
    companies.write_text('{"companies": []}', encoding="utf-8")
    profile.write_text('{}', encoding="utf-8")

    assert run(str(companies), str(profile), str(db)) == 0
    assert "Companies configured: 0" in capsys.readouterr().out
    assert Path(db).exists()
