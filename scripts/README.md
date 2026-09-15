# Operational scripts

## Run a scan

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_scan.ps1
```

The runner uses `.venv\Scripts\python.exe` when available and appends output to `logs\scan.log`.

## Install the daily task

Run PowerShell as the user who should own the task:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_task.ps1
```

The task runs daily at 9:00 AM local time. Update the trigger in `install_task.ps1` if you want another time.

Configure Telegram environment variables in the account that runs the task before installing it:

- `JOBMAXXER_TELEGRAM_BOT_TOKEN`
- `JOBMAXXER_TELEGRAM_CHAT_ID`
