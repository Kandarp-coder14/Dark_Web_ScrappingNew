from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,
    fetched_at TEXT NOT NULL,
    status_code INTEGER,
    title TEXT,
    excerpt TEXT,
    error TEXT
);

CREATE TABLE IF NOT EXISTS indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_url TEXT NOT NULL,
    indicator TEXT NOT NULL,
    type TEXT NOT NULL,
    found_at TEXT NOT NULL
);
"""



def ensure_db(db_path: str) -> sqlite3.Connection:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    return conn



def save_page(
    conn: sqlite3.Connection,
    url: str,
    fetched_at: str,
    status_code: int | None,
    title: str,
    excerpt: str,
    error: str | None,
) -> None:
    conn.execute(
        """
        INSERT INTO pages(url, fetched_at, status_code, title, excerpt, error)
        VALUES(?, ?, ?, ?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET
          fetched_at=excluded.fetched_at,
          status_code=excluded.status_code,
          title=excluded.title,
          excerpt=excluded.excerpt,
          error=excluded.error
        """,
        (url, fetched_at, status_code, title, excerpt, error),
    )
    conn.commit()



def classify_indicator(value: str) -> str:
    if value.endswith(".onion"):
        return "onion_address"
    if "@" in value:
        return "email"
    if value.startswith("bc1") or value[:1] in {"1", "3"}:
        return "crypto_wallet"
    return "unknown"



def save_indicators(conn: sqlite3.Connection, page_url: str, values: list[str], found_at: str) -> None:
    rows = [(page_url, value, classify_indicator(value), found_at) for value in values]
    if rows:
        conn.executemany(
            "INSERT INTO indicators(page_url, indicator, type, found_at) VALUES(?, ?, ?, ?)",
            rows,
        )
        conn.commit()
