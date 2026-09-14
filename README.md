# JobMaxxer

Personal, cost-free job monitoring for entry-level AI/backend/software roles.

## Goals

- Scan public company career pages and ATS endpoints.
- Normalize jobs into a common schema.
- Filter for entry-level AI/backend/platform opportunities.
- Persist seen jobs locally with SQLite.
- Report scan failures instead of hiding them.
- Send new matches to Telegram later.
- Run locally on Windows with Task Scheduler.

## Current status

Core scanner foundation is implemented in the first feature PR.

## Cost

Designed for personal use at INR 0/month. No paid API, hosting, VPS, domain, or database is required.

## Safety

This project does not auto-apply to jobs, automate LinkedIn messaging, or perform automated LinkedIn login/scraping.
