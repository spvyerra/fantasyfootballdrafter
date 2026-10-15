"""Thin httpx wrapper around ESPN's public NFL endpoints.

Base URLs and endpoint catalog: docs/espn-nfl-endpoints.md
"""

from typing import Any

import httpx

SITE_V2 = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
SITE_V2_STANDINGS = "https://site.api.espn.com/apis/v2/sports/football/nfl"
CORE_V2 = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl"
CORE_V3 = "https://sports.core.api.espn.com/v3/sports/football/nfl"
COMMON_V3 = "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl"
SEARCH_V2 = "https://site.web.api.espn.com/apis/search/v2"
CDN = "https://cdn.espn.com/core/nfl"

_TIMEOUT = httpx.Timeout(15.0)
_HEADERS = {"User-Agent": "FootBallRag/0.1 (+https://github.com/pseudo-r/Public-ESPN-API)"}


class ESPNError(Exception):
    def __init__(self, status_code: int, url: str, body: str):
        self.status_code = status_code
        self.url = url
        super().__init__(f"ESPN {status_code} for {url}: {body[:200]}")


def _rewrite_pvt(value: Any) -> Any:
    """Rewrite internal `.pvt` hostnames in ESPN $ref URLs to the public `.com` host."""
    if isinstance(value, str):
        return value.replace("sports.core.api.espn.pvt", "sports.core.api.espn.com")
    if isinstance(value, dict):
        return {k: _rewrite_pvt(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_rewrite_pvt(v) for v in value]
    return value


def get(base: str, path: str = "", params: dict[str, Any] | None = None) -> Any:
    """GET `{base}{path}` and return parsed JSON.

    Retries once on transport errors. Raises ESPNError on non-2xx responses.
    """
    url = f"{base}{path}"
    params = {k: v for k, v in (params or {}).items() if v is not None}
    last_exc: Exception | None = None
    for _ in range(2):
        try:
            resp = httpx.get(url, params=params, headers=_HEADERS, timeout=_TIMEOUT, follow_redirects=True)
            if resp.status_code >= 400:
                raise ESPNError(resp.status_code, str(resp.url), resp.text)
            return _rewrite_pvt(resp.json())
        except httpx.TransportError as exc:
            last_exc = exc
    raise ESPNError(0, url, str(last_exc))


def paginate(base: str, path: str = "", params: dict[str, Any] | None = None, limit: int = 100) -> list[Any]:
    """Follow `page`/`pageCount` on Core list endpoints; returns all `items` entries."""
    items: list[Any] = []
    page = 1
    while True:
        data = get(base, path, {**(params or {}), "page": page, "limit": limit})
        items.extend(data.get("items", []))
        if page >= data.get("pageCount", 1):
            return items
        page += 1
