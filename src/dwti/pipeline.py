from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone

from .config import AppConfig
from .parser import parse_html
from .scraper import allowed, fetch_url
from .storage import ensure_db, save_indicators, save_page
from .tor_client import build_session


@dataclass
class RunStats:
    visited: int = 0
    success: int = 0
    failed: int = 0
    indicators: int = 0



def run_pipeline(config: AppConfig) -> RunStats:
    session = build_session(config)
    conn = ensure_db(config.output_db)

    q: deque[tuple[str, int]] = deque((url, 0) for url in config.crawl.seed_urls)
    seen: set[str] = set()
    stats = RunStats()

    while q and stats.visited < config.crawl.max_pages:
        url, depth = q.popleft()
        if url in seen:
            continue
        seen.add(url)

        timestamp = datetime.now(timezone.utc).isoformat()
        result = fetch_url(
            session=session,
            url=url,
            timeout_seconds=config.crawl.timeout_seconds,
            allowed_domains=config.crawl.allowed_domains,
            enforce_allowlist=config.crawl.respect_allowed_domains,
        )

        stats.visited += 1

        if result.error:
            stats.failed += 1
            save_page(
                conn,
                url=result.url,
                fetched_at=timestamp,
                status_code=result.status_code,
                title="",
                excerpt="",
                error=result.error,
            )
            continue

        parsed = parse_html(result.url, result.html)
        save_page(
            conn,
            url=result.url,
            fetched_at=timestamp,
            status_code=result.status_code,
            title=parsed.title,
            excerpt=parsed.text_excerpt,
            error=None,
        )
        save_indicators(conn, result.url, parsed.indicators, timestamp)

        stats.success += 1
        stats.indicators += len(parsed.indicators)

        if depth < config.crawl.max_depth:
            for link in parsed.links:
                if allowed(link, config.crawl.allowed_domains, config.crawl.respect_allowed_domains):
                    q.append((link, depth + 1))

    conn.close()
    return stats
