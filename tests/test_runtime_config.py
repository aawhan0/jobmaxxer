from pathlib import Path

import pytest

from jobmaxxer.runtime_config import RuntimeConfig


def test_validate_rejects_missing_configuration(tmp_path: Path):
    config = RuntimeConfig(
        tmp_path / "companies.json",
        tmp_path / "profile.json",
        tmp_path / "data" / "jobs.db",
        tmp_path / "logs" / "scan.log",
    )

    with pytest.raises(FileNotFoundError, match="companies.json"):
        config.validate()


def test_validate_creates_runtime_directories(tmp_path: Path):
    (tmp_path / "companies.json").write_text('{"companies": []}', encoding="utf-8")
    (tmp_path / "profile.json").write_text('{}', encoding="utf-8")
    config = RuntimeConfig(
        tmp_path / "companies.json",
        tmp_path / "profile.json",
        tmp_path / "data" / "jobs.db",
        tmp_path / "logs" / "scan.log",
    )

    config.validate()

    assert (tmp_path / "data").is_dir()
    assert (tmp_path / "logs").is_dir()
