# Dark Web Scraping for Threat Intelligence (Defensive Project)

## 1. Project Overview
This repository implements a **defensive threat-intelligence scraping pipeline** designed for cybersecurity research use cases.

The project focuses on:
- Controlled data collection from web targets (including potential `.onion` targets when Tor is enabled)
- Basic extraction of intelligence indicators from HTML content
- Structured persistence of crawl results into SQLite for later analysis

This is an educational and research-oriented implementation of a practical monitoring workflow.

## 2. Dark Web Scraping Context
### What "dark web scraping" means here
In this project, dark web scraping means collecting data from `.onion` sites by routing requests through a Tor SOCKS proxy (`socks5h://127.0.0.1:9050`).

### Why it matters for cybersecurity
Security teams may monitor approved sources for early signs of:
- Credential leaks
- Threat actor infrastructure references
- Wallets/emails/onion mirrors linked to campaigns
- Emerging tactics discussed in adversarial communities

### Important legal and safety constraints
Use only with:
- Explicit legal authorization
- Approved targets
- Secure and isolated execution environments

Do **not** use this project for unauthorized access, harmful activity, or illegal marketplace interaction.

## 3. Key Features
- Tor-aware HTTP session (optional) via `requests` + SOCKS
- Domain allowlist enforcement
- Crawl boundaries (`max_pages`, `max_depth`, timeout)
- HTML parsing with BeautifulSoup
- Indicator extraction (email, onion-like strings, wallet-like strings)
- SQLite storage with two main tables (`pages`, `indicators`)
- CLI runner with execution statistics

## 4. High-Level Architecture
```text
CLI (run.py / dwti.cli)
  -> Load YAML config (dwti.config)
  -> Build HTTP session (dwti.tor_client)
  -> Crawl/fetch URLs (dwti.scraper)
  -> Parse HTML + extract indicators (dwti.parser)
  -> Persist pages/indicators (dwti.storage)
  -> Print run stats
```

## 5. End-to-End Control Flow
1. User executes: `python run.py --config config.yaml`
2. `run.py` loads `dwti.cli.main()` from `src/`
3. CLI parses arguments and loads YAML config
4. Pipeline initializes:
- HTTP session with User-Agent
- Tor proxies if enabled
- SQLite database and schema
5. Queue is initialized with seed URLs
6. For each URL (until limits reached):
- Validate allowlist constraints
- Fetch page with timeout
- Store failure if request errors
- If HTML is available: parse title/text/links
- Extract indicators from text
- Save page + indicators to DB
- Enqueue discovered links if depth rules allow
7. Pipeline returns stats (visited/success/failed/indicators) 
8. CLI prints final summary and exits


## 6. Directory and File Details
```text
Dark_Web_ScrappingNew/
  config.example.yaml          # Sample runtime configuration
  config.yaml                  # User runtime config (created from sample)
  requirements.txt             # Python dependencies
  run.py                       # Thin entrypoint that runs CLI
  README.md                    # Project documentation

  src/
    dwti/
      __init__.py
      __main__.py              # Allows `python -m dwti`
      cli.py                   # Argument parsing + stats output
      config.py                # Dataclasses + YAML loading
      tor_client.py            # Requests session and proxy setup
      scraper.py               # URL normalization, allow checks, fetching
      parser.py                # HTML parsing + regex indicator extraction
      storage.py               # SQLite schema + insert/update logic
      pipeline.py              # Crawl orchestration and control flow

  tests/
    test_parser.py             # Unit test for parser behavior

  data/
    intel.db                   # Generated SQLite database output

  presentation/
    make_ppt.py               # Script to generate project PPT
    Dark_Web_Scraping_Threat_Intelligence_Project.pptx
```

## 7. Module-by-Module Code Explanation
### `src/dwti/config.py`
Purpose:
- Defines typed configuration using dataclasses:
  - `TorSettings`
  - `CrawlSettings`
  - `AppConfig`
- Loads YAML config safely and applies defaults.

Key behavior:
- Missing fields are defaulted
- List fields (`allowed_domains`, `seed_urls`) are normalized to strings
- Returns one `AppConfig` object consumed by the pipeline

### `src/dwti/tor_client.py`
Purpose:
- Creates a reusable `requests.Session` with consistent headers
- Applies Tor proxy settings when `tor.enabled=true`

Key behavior:
- Always sets `User-Agent`
- Adds both `http` and `https` proxy entries when Tor is enabled

### `src/dwti/scraper.py`
Purpose:
- Encapsulates URL-level operations and fetch behavior

Main components:
- `FetchResult` dataclass: standard output model for fetch attempts
- `allowed(...)`: checks whether URL domain is inside allowlist (if enforced)
- `normalize_link(...)`: converts relative links to absolute and filters unsupported schemes
- `fetch_url(...)`: performs request with timeout, handles request exceptions, and captures HTML

### `src/dwti/parser.py`
Purpose:
- Converts raw HTML into structured page intelligence

Main components:
- `ParsedPage` dataclass with:
  - `title`
  - `text_excerpt`
  - `links`
  - `indicators`
- Uses BeautifulSoup to parse page title and visible text
- Extracts links from `<a href=...>` and normalizes URLs
- Applies regex signatures for:
  - emails
  - onion-like hostnames
  - crypto wallet-like strings

### `src/dwti/storage.py`
Purpose:
- Handles SQLite schema creation and write operations

Tables:
- `pages`
  - URL, timestamp, status, title, excerpt, error
- `indicators`
  - page URL, indicator value, indicator type, timestamp

Key behavior:
- Upsert-style write on `pages` by URL
- Batch insert for indicators
- Simple indicator classification helper (`email`, `onion_address`, `crypto_wallet`)

### `src/dwti/pipeline.py`
Purpose:
- Coordinates complete crawl lifecycle

Main logic:
- Builds session and DB connection
- Uses BFS-style queue (`deque`) for crawling
- Tracks visited URLs to avoid repeats
- Enforces `max_pages` and `max_depth`
- For each fetch:
  - Save failures immediately
  - Parse successful HTML and persist results
  - Enqueue eligible child links
- Returns `RunStats` summary

### `src/dwti/cli.py`
Purpose:
- Command-line interface and output layer

Behavior:
- Requires `--config`
- Loads config and runs pipeline
- Prints concise execution report

### `run.py`
Purpose:
- Local launcher that ensures `src/` is importable and then calls CLI `main()`

## 8. Configuration Guide (`config.yaml`)
Example:
```yaml
project_name: "dark-web-threat-intel"
user_agent: "DWTI-Research-Bot/1.0"
output_db: "data/intel.db"

tor:
  enabled: true
  proxy_url: "socks5h://127.0.0.1:9050"

crawl:
  max_pages: 20
  max_depth: 1
  timeout_seconds: 25
  respect_allowed_domains: true
  allowed_domains:
    - "approvedtarget.onion"
  seed_urls:
    - "http://approvedtarget.onion"
```

Field notes:
- `tor.enabled`: must be `true` for `.onion` targets
- `proxy_url`: Tor SOCKS endpoint (default local)
- `respect_allowed_domains`: if true, out-of-scope domains are skipped
- `max_pages`/`max_depth`: critical safeguards for controlled crawling

## 9. Setup and Execution
### Install
```powershell
python -m pip install -r requirements.txt
```

### Create config
```powershell
Copy-Item config.example.yaml config.yaml
```
Then edit `config.yaml` with approved targets.

### Run
```powershell
python run.py --config config.yaml
```

### Test
```powershell
$env:PYTHONPATH='src'
python -m pytest -q
```

## 10. Understanding Runtime Output
Example output:
```text
Project: dark-web-threat-intel
Visited: 1
Success: 0
Failed: 1
Indicators: 0
Database: data/intel.db
```

Interpretation:
- `Visited`: URLs attempted
- `Success`: requests completed and parsed
- `Failed`: request or policy failures
- `Indicators`: total extracted matches
- `Database`: location of stored results

## 11. SQLite Data Model
### `pages` table
Stores one row per URL with latest fetch metadata:
- `url` (unique)
- `fetched_at`
- `status_code`
- `title`
- `excerpt`
- `error`

### `indicators` table
Stores extracted indicator events:
- `page_url`
- `indicator`
- `type`
- `found_at`

## 12. Security and Operational Best Practices
- Run inside isolated VM/container when testing unknown sources
- Keep strict allowlists and page limits
- Maintain logs and audit approvals for targets
- Treat extracted data as sensitive
- Validate automated findings with analyst review before action

## 13. Limitations
- Regex-based extraction can produce false positives
- No JavaScript-rendered content support
- No deduplication hash for indicator rows yet
- No advanced reporting UI (DB-first output model)
- Performance is intentionally conservative for safety

## 14. Suggested Next Enhancements
- Add export command for CSV/JSON report generation
- Add richer IOC patterns and confidence scoring
- Add retry/backoff and request jitter controls
- Add structured logging and run-level metadata
- Add dashboard/visualization layer over SQLite

## 15. Quick Viva/Presentation Summary
If presenting this project:
- Problem: early threat detection from hidden web sources
- Method: controlled crawler + parser + indicator extractor + DB persistence
- Safety: legal-only targets, Tor option, allowlists, bounded crawling
- Result: executable pipeline with measurable stats and auditable storage
