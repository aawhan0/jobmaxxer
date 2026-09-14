# JobMaxxer

Personal, cost-free job monitoring for entry-level AI/backend/software roles.

## Current stage

The core scanner foundation is ready in the first feature PR:

- JSON-based company and candidate configuration
- Generic public HTML career-page adapter
- Normalized job model
- Entry-level relevance scoring
- Seniority and experience exclusions
- SQLite persistence and first-seen deduplication
- Per-company scan failure recording
- Command-line runner
- Tests for matching and persistence

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scanner.py
```

Replace the placeholder company in `config/companies.json` with a real public career page before scanning.

## Planned next stages

1. Configure all 46 real companies.
2. Add ATS-specific adapters where public endpoints exist.
3. Improve job parsing, location extraction, deduplication, and matching.
4. Add Telegram notifications.
5. Add Windows Task Scheduler setup.
6. Add optional LinkedIn alert-email/referral intake without automated LinkedIn messaging or login.

## Safety

JobMaxxer does not auto-apply to jobs, automate LinkedIn messaging, perform automated LinkedIn login, or use aggressive LinkedIn scraping.

## Cost

The intended deployment is local-only at INR 0/month: no paid API, VPS, hosted database, domain, or paid scraping service.
