import argparse
import logging

from src.jobmaxxer.adapters import scan_html_company
from src.jobmaxxer.config import load_json
from src.jobmaxxer.filtering import rank_matches
from src.jobmaxxer.storage import Store

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("jobmaxxer")


def run(companies_path: str, profile_path: str, db_path: str) -> int:
    companies = [item for item in load_json(companies_path).get("companies", []) if item.get("enabled", True)]
    profile = load_json(profile_path)
    store = Store(db_path)
    failures = 0
    discovered = 0
    new_matches = 0

    try:
        for company in companies:
            name = company["name"]
            url = company["career_url"]
            try:
                logger.info("Scanning %s", name)
                jobs = scan_html_company(name, url)
                discovered += len(jobs)
                matches = rank_matches(jobs, profile)
                unseen = store.add_jobs(result.job for result in matches)
                ranked_unseen = rank_matches(unseen, profile)
                new_matches += len(ranked_unseen)
                store.record_scan(name, True, len(jobs))
                for result in ranked_unseen:
                    print("\nNEW MATCH")
                    print(f"Company: {result.job.company}")
                    print(f"Role: {result.job.title}")
                    print(f"Location: {result.job.location or 'Not listed'}")
                    print(f"Match: {result.match_reason}")
                    print(f"Source: {result.job.source}")
                    print(f"Apply: {result.job.url}")
            except Exception as exc:
                failures += 1
                store.record_scan(name, False, 0, str(exc))
                logger.exception("Failed to scan %s", name)
    finally:
        store.close()

    print("\nSCAN SUMMARY")
    print(f"Companies configured: {len(companies)}")
    print(f"Jobs discovered: {discovered}")
    print(f"New relevant jobs: {new_matches}")
    print(f"Failed companies: {failures}")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Personal job scanner")
    parser.add_argument("--companies", default="config/companies.json")
    parser.add_argument("--profile", default="config/profile.json")
    parser.add_argument("--db", default="jobmaxxer.db")
    args = parser.parse_args()
    return run(args.companies, args.profile, args.db)


if __name__ == "__main__":
    raise SystemExit(main())
