from __future__ import annotations

import argparse

from .config import load_config
from .pipeline import run_pipeline



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dwti",
        description="Defensive dark web threat intelligence scraper",
    )
    parser.add_argument("--config", required=True, help="Path to YAML config")
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Confirm that you understand this will perform real network requests when config.crawl.dry_run is false",
    )
    return parser



def main() -> int:
    args = build_parser().parse_args()
    config = load_config(args.config)
    # If dry_run is disabled, require explicit confirmation to proceed
    if not config.crawl.dry_run and not args.confirm:
        try:
            resp = input(
                "WARNING: dry_run is disabled. Type YES to proceed with real network requests: "
            )
        except EOFError:
            print("No interactive input available. Use --confirm to bypass prompt.")
            return 2
        if resp.strip() != "YES":
            print("Aborted by user. Re-enable dry_run or provide --confirm to proceed.")
            return 1

    stats = run_pipeline(config)

    print(f"Project: {config.project_name}")
    print(f"Visited: {stats.visited}")
    print(f"Success: {stats.success}")
    print(f"Failed: {stats.failed}")
    print(f"Indicators: {stats.indicators}")
    print(f"Database: {config.output_db}")
    return 0
