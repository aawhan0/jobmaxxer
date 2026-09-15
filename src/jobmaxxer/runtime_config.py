"""Runtime configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RuntimeConfig:
    companies_path: Path
    profile_path: Path
    db_path: Path
    log_path: Path

    @classmethod
    def from_env(cls) -> "RuntimeConfig":
        return cls(
            Path(os.getenv("JOBMAXXER_COMPANIES_PATH", "config/companies.json")),
            Path(os.getenv("JOBMAXXER_PROFILE_PATH", "config/profile.json")),
            Path(os.getenv("JOBMAXXER_DB_PATH", "data/jobmaxxer.db")),
            Path(os.getenv("JOBMAXXER_LOG_PATH", "logs/scan.log")),
        )

    def validate(self) -> None:
        for path in (self.companies_path, self.profile_path):
            if not path.is_file():
                raise FileNotFoundError(f"Required configuration file not found: {path}")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
