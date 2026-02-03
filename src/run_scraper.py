import argparse
from core_scraper import scrape_state


def main():
    parser = argparse.ArgumentParser(
        description="NamUs Missing Persons Scraper (Educational OSINT Automation Tool)"
    )

    parser.add_argument("--state", required=True, help="State name (example: Texas)")
    parser.add_argument("--min-age", type=int, default=6, help="Minimum age (default: 6)")
    parser.add_argument("--max-age", type=int, default=16, help="Maximum age (default: 16)")
    parser.add_argument("--output", default="output", help="Output folder (default: output)")

    args = parser.parse_args()

    scrape_state(
        state_name=args.state,
        save_folder=args.output,
        age_min=args.min_age,
        age_max=args.max_age
    )


if __name__ == "__main__":
    main()
