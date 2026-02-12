**Execution Summary**

- **Repository inspected:** `run.py`, `src/dwti/*`, `tests/test_parser.py`, `config.yaml`, `config.example.yaml`.

- **Safety defaults added:** `crawl.dry_run` (default: `true`) was added to avoid accidental network requests.
- **Allowlist enforcement:** `pipeline` now raises if `respect_allowed_domains` is true but `allowed_domains` is empty.
- **CLI confirmation:** `--confirm` flag and an interactive `YES` prompt were added to require explicit user confirmation before real network activity when `dry_run` is false.
- **SSL control:** `AppConfig` gained `verify_ssl` and `ca_bundle` fields; `tor_client.build_session()` respects these settings (toggle verification or point to custom CA bundle).
- **Export tooling:** `scripts/export_db.py` added to export `pages` and `indicators` to `exports/pages.csv`, `exports/indicators.csv`, and `exports/intel.json`.
- **DB inspection helper:** `scripts/inspect_db.py` added to quickly print table names and first rows.
- **Tests:** Verified with Python 3.12; `py -3.12 -m pytest -q` passed (1 test).
- **Dry runs and real runs:** Performed dry-run and limited real crawls (small `max_pages`) and measured elapsed times. Reverted `config.yaml` to safe defaults (`dry_run: true`, `max_pages: 20`).

**Files added/modified (high level)**

- `src/dwti/config.py` — added `crawl.dry_run`, `verify_ssl`, `ca_bundle`
- `src/dwti/pipeline.py` — enforce allowlist, support dry-run behavior
- `src/dwti/cli.py` — added `--confirm` and interactive prompt
- `src/dwti/tor_client.py` — respect `verify_ssl` / `ca_bundle` and Tor proxy settings
- `scripts/inspect_db.py` — DB quick-inspect helper
- `scripts/export_db.py` — export pages/indicators to CSV + combined JSON
- `config.example.yaml` — documented `dry_run`, `verify_ssl`, `ca_bundle`
- `config.yaml` — temporarily adjusted for testing and then reverted to safe defaults

**How to reproduce key actions locally**

- Run tests (Python 3.12):

```powershell
py -3.12 -m pip install -r requirements.txt
py -3.12 -m pytest -q
```

- Dry-run the pipeline (no network calls):

```powershell
py -3.12 run.py --config config.yaml
```

- Run a real (non-dry) limited crawl (requires approvals):

1. Edit `config.yaml` and set `crawl.dry_run: false` and provide `crawl.allowed_domains` / `seed_urls` you are approved to crawl.
2. Run with explicit confirmation (or `--confirm`):

```powershell
py -3.12 run.py --config config.yaml --confirm
```

- Export DB to CSV/JSON:

```powershell
py -3.12 scripts\\export_db.py data\\intel.db exports
dir exports
```

**Inspect DB quickly (already present script):**

```powershell
py -3.12 scripts\\inspect_db.py
```

---

**Install sqlite3 on Windows (CMD instructions)**

Use one of these methods. The first is GUI/manual download + CMD PATH update. The second uses `curl`/`tar` if available in your CMD environment.

Method A — Manual download + CMD PATH update

1. Download the precompiled sqlite tools ZIP from the official site in a browser:
   - https://www.sqlite.org/download.html
   - Choose: "sqlite-tools-win32-x86-<version>.zip" (contains `sqlite3.exe`).
2. Create target folder in CMD:

```cmd
mkdir "D:\\SOFTWARES\\SQLITE"
```

3. Extract the ZIP contents into `D:\\SOFTWARES\\SQLITE` (use Explorer or a tool like 7-Zip). Place `sqlite3.exe` directly inside the folder.

4. Add the folder to your PATH using CMD (this updates user PATH permanently):

```cmd
setx PATH "%PATH%;D:\\SOFTWARES\\SQLITE"
```

5. Close and reopen any CMD windows, then verify:

```cmd
sqlite3 --version
```

Method B — Download via CMD (if `curl` and `tar` present)

1. From CMD, download the ZIP (replace the URL with the current release):

```cmd
curl -L -o sqlite-tools.zip "https://www.sqlite.org/2026/sqlite-tools-win32-x86-xxxxxx.zip"
mkdir D:\\SOFTWARES\\SQLITE
tar -xf sqlite-tools.zip -C D:\\SOFTWARES\\SQLITE
```

2. Add to PATH and verify (same `setx` + `sqlite3 --version` as above).

Notes & troubleshooting:

- After `setx`, open a new CMD — `setx` changes won't affect existing shells.
- If PATH gets very long, Windows `setx` may fail — use System → Advanced → Environment Variables to edit PATH manually.
- If you prefer PowerShell, use `Expand-Archive` to unzip:

```powershell
Expand-Archive -Path sqlite-tools.zip -DestinationPath D:\\SOFTWARES\\SQLITE
```

---

If you want, I can:

- Open and paste `exports/intel.json` here or show counts from the DB.
- Add an automatic `--export` flag to the CLI that runs the export after a crawl.
- Add optional retries/backoff or SSL troubleshooting guidance (e.g., how to point `ca_bundle` to an internal CA file).

Pick the next action and I will proceed.
