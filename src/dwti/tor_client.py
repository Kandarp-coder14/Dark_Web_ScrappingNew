from __future__ import annotations

import requests

from .config import AppConfig



def build_session(config: AppConfig) -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": config.user_agent})

    if config.tor.enabled:
        proxy = config.tor.proxy_url
        session.proxies.update({"http": proxy, "https": proxy})

    return session
