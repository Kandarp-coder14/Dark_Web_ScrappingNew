# config.yaml README

This document explains each key used in `config.yaml` for the Dark Web Threat Intelligence project.

## Top-Level Keys

### `project_name`
- Label for the run/project.
- Printed in CLI output; useful for identifying scans.

### `user_agent`
- HTTP `User-Agent` header sent with each request.
- Helps identify your crawler in server logs.

### `output_db`
- SQLite file path where results are stored.
- Creates/uses `pages` and `indicators` tables there.

## `tor` Section

### `tor.enabled`
- `true`: route traffic through Tor proxy.
- `false`: normal internet routing (not `.onion` capable).

### `tor.proxy_url`
- SOCKS proxy endpoint used when Tor is enabled.
- Typical local Tor value: `socks5h://127.0.0.1:9050`.

## `crawl` Section

### `crawl.max_pages`
- Hard limit on how many URLs can be visited in one run.
- Safety/performance control.

### `crawl.max_depth`
- Link-following depth from seed URLs.
- `0` = only seeds, `1` = seeds + their links, etc.

### `crawl.timeout_seconds`
- Per-request timeout.
- Prevents hanging on slow/unresponsive sites.

### `crawl.respect_allowed_domains`
- `true`: only crawl domains in `allowed_domains`.
- `false`: allow any discovered domain (less safe).

### `crawl.allowed_domains`
- Domain allowlist for crawl scope.
- With `true`, out-of-list URLs are skipped.

### `crawl.seed_urls`
- Starting URLs for the crawler queue.
- Crawl begins from these targets.

## Interpretation of Your Current Config
- It runs in clearnet mode (`tor.enabled: false`).
- It starts at `https://example.org`.
- It is restricted to `exampleonion.org` and `example.org`.
- It can visit up to 20 pages, one level deep, with 25s timeout.
