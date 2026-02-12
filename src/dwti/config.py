from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class TorSettings:
    enabled: bool = False
    proxy_url: str = "socks5h://127.0.0.1:9050"


@dataclass
class CrawlSettings:
    max_pages: int = 30
    max_depth: int = 1
    timeout_seconds: int = 25
    respect_allowed_domains: bool = True
    allowed_domains: list[str] = field(default_factory=list)
    seed_urls: list[str] = field(default_factory=list)
    # When True, no network requests are made; safe default to avoid accidental crawls
    dry_run: bool = True


@dataclass
class AppConfig:
    project_name: str = "dwti"
    user_agent: str = "DWTI-Research-Bot/1.0"
    output_db: str = "data/intel.db"
    tor: TorSettings = field(default_factory=TorSettings)
    crawl: CrawlSettings = field(default_factory=CrawlSettings)
    # SSL verification controls: keep True for safety. Set a path to a CA bundle to trust.
    verify_ssl: bool = True
    ca_bundle: str | None = None



def _as_dict(data: Any) -> dict[str, Any]:
    return data if isinstance(data, dict) else {}



def load_config(path: str | Path) -> AppConfig:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    raw = _as_dict(raw)

    tor_raw = _as_dict(raw.get("tor"))
    crawl_raw = _as_dict(raw.get("crawl"))

    tor = TorSettings(
        enabled=bool(tor_raw.get("enabled", False)),
        proxy_url=str(tor_raw.get("proxy_url", "socks5h://127.0.0.1:9050")),
    )

    crawl = CrawlSettings(
        max_pages=int(crawl_raw.get("max_pages", 30)),
        max_depth=int(crawl_raw.get("max_depth", 1)),
        timeout_seconds=int(crawl_raw.get("timeout_seconds", 25)),
        respect_allowed_domains=bool(crawl_raw.get("respect_allowed_domains", True)),
        allowed_domains=[str(x) for x in crawl_raw.get("allowed_domains", [])],
        seed_urls=[str(x) for x in crawl_raw.get("seed_urls", [])],
        dry_run=bool(crawl_raw.get("dry_run", True)),
    )

    return AppConfig(
        project_name=str(raw.get("project_name", "dwti")),
        user_agent=str(raw.get("user_agent", "DWTI-Research-Bot/1.0")),
        output_db=str(raw.get("output_db", "data/intel.db")),
        tor=tor,
        crawl=crawl,
        verify_ssl=bool(raw.get("verify_ssl", True)),
        ca_bundle=(str(raw.get("ca_bundle")) if raw.get("ca_bundle") else None),
    )
