# Operations

## Local scan

```powershell
.venv\Scripts\python.exe scanner.py
```

## Windows shortcut

```powershell
scripts\run_scan.bat
```

Create a Windows Task Scheduler task that runs `scripts\run_scan.bat` from the repository directory. Keep credentials out of the repository and use environment variables for optional notification integrations.

## Recovery

- Re-run the scan after transient network failures.
- Inspect SQLite `scan_runs` for failed companies.
- Keep `config/companies.json` limited to verified career or ATS URLs.
- Use dry-run mode before enabling scheduled execution.
