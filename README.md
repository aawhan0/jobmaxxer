# jobmaxxer

Personal, local-first job monitoring tool.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scanner.py
```

The scanner reads `config/companies.json` and `config/profile.json`, stores fingerprints in `jobmaxxer.db`, and prints only newly discovered relevant matches. Failed company scans are recorded in the SQLite `scan_runs` table.

For troubleshooting, `python scanner.py --diagnostics` prints filtering and storage counts by source, including relevant jobs that were already seen.

When Telegram credentials are configured, new matches are sent as an actionable digest containing the role, location, score, matching reasons, and application link. See `docs/notification-digest.md` for details.

No applications, messages, or LinkedIn actions are automated.
