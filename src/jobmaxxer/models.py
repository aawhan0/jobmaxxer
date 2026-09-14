from dataclasses import dataclass, field
from hashlib import sha256


@dataclass(frozen=True)
class Job:
    company: str
    title: str
    location: str
    url: str
    source: str
    description: str = ""
    external_id: str = ""

    @property
    def fingerprint(self) -> str:
        identity = self.external_id or self.url or f"{self.company}|{self.title}|{self.location}"
        return sha256(identity.strip().lower().encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class MatchResult:
    job: Job
    score: int
    reasons: tuple[str, ...] = field(default_factory=tuple)

    @property
    def match_reason(self) -> str:
        return "; ".join(self.reasons) if self.reasons else "Matched target role/profile criteria"
