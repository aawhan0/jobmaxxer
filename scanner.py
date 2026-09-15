import argparse
import logging
from pathlib import Path

from src.jobmaxxer.providers import scan_company
from src.jobmaxxer.config import load_json
from src.jobmaxxer.filtering import rank_matches
from src.jobmaxxer.reporting import export_jobs
from src.jobmaxxer.cli import format_match, output_path
from src.jobmaxxer.notifications import format_digest
from src.jobmaxxer.telegram import TelegramConfig, send_message
from src.jobmaxxer.runtime_config import RuntimeConfig
from src.jobmaxxer.storage import Store

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("jobmaxxer")


def run(companies_path: str, profile_path: str, db_path: str, export: str | None = None) -> int:
    companies = [item for item in load_json(companies_path).get("companies", []) if item.get("enabled", True)]
    profile = load_json(profile_path)
    store = Store(db_path)
    failures = discovered = new_matches = 0
    all_matches = []
    try:
        for company in companies:
            name, url = company["name"], company["career_url"]
            try:
                logger.info("Scanning %s", name)
                jobs = scan_company(name, url, company.get("adapter"))
                discovered += len(jobs)
                ranked = rank_matches(jobs, profile)
                unseen_jobs = store.add_jobs(result.job for result in ranked)
                ranked_unseen = rank_matches(unseen_jobs, profile)
                all_matches.extend(ranked_unseen)
                new_matches += len(ranked_unseen)
                store.record_scan(name, True, len(jobs))
                for result in ranked_unseen:
                    print(f"\n{format_match(result)}")
            except Exception as exc:
                failures += 1
                store.record_scan(name, False, 0, str(exc))
                logger.exception("Failed to scan %s", name)
    finally:
        store.close()
    if export:
        export_jobs(all_matches, output_path(export))
    telegram = TelegramConfig.from_env()
    if telegram and all_matches:
        try:
            send_message(format_digest(all_matches), telegram)
            logger.info("Sent %s new matches to Telegram", len(all_matches))
        except Exception:
            logger.exception("Telegram delivery failed")
            failures += 1
    print(f"\nSCAN SUMMARY\nCompanies configured: {len(companies)}\nJobs discovered: {discovered}\nNew relevant jobs: {new_matches}\nFailed companies: {failures}")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Personal job scanner")
    defaults = RuntimeConfig.from_env()
    parser.add_argument("--companies", default=str(defaults.companies_path))
    parser.add_argument("--profile", default=str(defaults.profile_path))
    parser.add_argument("--db", default=str(defaults.db_path))
    parser.add_argument("--export", help="Write new matches to a .json or .csv file")
    args = parser.parse_args()
    config = RuntimeConfig(Path(args.companies), Path(args.profile), Path(args.db), defaults.log_path)
    config.validate()
    return run(args.companies, args.profile, args.db, args.export)


if __name__ == "__main__":
    raise SystemExit(main())
