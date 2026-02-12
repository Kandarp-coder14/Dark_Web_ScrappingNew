from __future__ import annotations

import requests

from .config import AppConfig



def build_session(config: AppConfig) -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": config.user_agent})
    # Configure Tor proxies when requested
    if config.tor.enabled:
        proxy = config.tor.proxy_url
        session.proxies.update({"http": proxy, "https": proxy})

    # Configure SSL verification behavior. By default, verification is enabled.
    # If a CA bundle path is provided, requests will use that bundle.
    if config.ca_bundle:
        session.verify = config.ca_bundle
    else:
        session.verify = bool(config.verify_ssl)

    return session
