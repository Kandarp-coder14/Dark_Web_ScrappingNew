from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse

import requests


@dataclass
class FetchResult:
    url: str
    status_code: int | None
    content_type: str
    html: str
    error: str | None = None
    discovered_links: list[str] = field(default_factory=list)



def _domain(url: str) -> str:
    return (urlparse(url).hostname or "").lower()



def allowed(url: str, allowed_domains: list[str], enforce: bool) -> bool:
    if not enforce or not allowed_domains:
        return True
    d = _domain(url)
    return any(d == item or d.endswith(f".{item}") for item in allowed_domains)



def normalize_link(base_url: str, href: str) -> str | None:
    if not href:
        return None
    href = href.strip()
    if href.startswith("#") or href.startswith("javascript:"):
        return None

    candidate = urljoin(base_url, href)
    parsed = urlparse(candidate)
    if parsed.scheme not in {"http", "https"}:
        return None
    return candidate



def fetch_url(
    session: requests.Session,
    url: str,
    timeout_seconds: int,
    allowed_domains: list[str],
    enforce_allowlist: bool,
) -> FetchResult:
    if not allowed(url, allowed_domains, enforce_allowlist):
        return FetchResult(
            url=url,
            status_code=None,
            content_type="",
            html="",
            error="URL outside allowed domains",
        )

    try:
        response = session.get(url, timeout=timeout_seconds)
        content_type = response.headers.get("Content-Type", "").lower()
        html = response.text if "text/html" in content_type else ""
        return FetchResult(
            url=response.url,
            status_code=response.status_code,
            content_type=content_type,
            html=html,
        )
    except requests.RequestException as exc:
        return FetchResult(
            url=url,
            status_code=None,
            content_type="",
            html="",
            error=str(exc),
        )
