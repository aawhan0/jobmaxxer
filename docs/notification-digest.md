# Notification digest

When Telegram credentials are configured, jobmaxxer sends a digest only when new relevant jobs are discovered.

Each entry includes:

- Company and role
- Location
- Match score
- Matching reasons
- Direct application link

The digest is capped at 10 jobs per scan. Use the terminal output or `--export` for the complete set of new matches.
