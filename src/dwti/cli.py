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
    return parser



def main() -> int:
    args = build_parser().parse_args()
    config = load_config(args.config)
    stats = run_pipeline(config)

    print(f"Project: {config.project_name}")
    print(f"Visited: {stats.visited}")
    print(f"Success: {stats.success}")
    print(f"Failed: {stats.failed}")
    print(f"Indicators: {stats.indicators}")
    print(f"Database: {config.output_db}")
    return 0
