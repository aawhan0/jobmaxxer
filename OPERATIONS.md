# Production operation checklist

1. Copy `.env.example` to `.env` or configure the variables in Windows Task Scheduler.
2. Set `JOBMAXXER_TELEGRAM_BOT_TOKEN` and `JOBMAXXER_TELEGRAM_CHAT_ID` only if Telegram delivery is desired.
3. Run the scan manually from the repository root before scheduling it.
4. Install the scheduled task with `scripts/install_task.ps1`.
5. Review `logs/scan.log` after the first scheduled run.
6. Keep `data/` and `logs/` out of version control; they contain local runtime state.

The scheduled task and credentials must be configured locally on the Windows machine. Never commit real Telegram tokens.
