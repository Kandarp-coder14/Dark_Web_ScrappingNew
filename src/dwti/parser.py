from __future__ import annotations

import re
from dataclasses import dataclass, field

from bs4 import BeautifulSoup

from .scraper import normalize_link

EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
BTC_RE = re.compile(r"\b(?:bc1|[13])[a-zA-HJ-NP-Z0-9]{25,62}\b")
ONION_RE = re.compile(r"\b[a-z2-7]{16,56}\.onion\b")


@dataclass
class ParsedPage:
    title: str
    text_excerpt: str
    links: list[str] = field(default_factory=list)
    indicators: list[str] = field(default_factory=list)



def parse_html(base_url: str, html: str) -> ParsedPage:
    soup = BeautifulSoup(html, "html.parser")
    title = (soup.title.string or "").strip() if soup.title else ""

    text = " ".join(soup.stripped_strings)
    text_excerpt = text[:5000]

    links: list[str] = []
    for a in soup.find_all("a", href=True):
        normalized = normalize_link(base_url, a.get("href", ""))
        if normalized:
            links.append(normalized)

    indicator_set = set()
    for pattern in (EMAIL_RE, BTC_RE, ONION_RE):
        indicator_set.update(pattern.findall(text_excerpt))

    return ParsedPage(
        title=title,
        text_excerpt=text_excerpt,
        links=sorted(set(links)),
        indicators=sorted(indicator_set),
    )
