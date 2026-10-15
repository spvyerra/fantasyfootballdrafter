"""NFL data routes - thin proxies to ESPN's public endpoints.

All routes fetch from ESPN on demand; nothing is persisted.
"""

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from . import espn_client as espn

router = APIRouter(prefix="/api/nfl", tags=["nfl"])


def _call(base: str, path: str = "", params: dict[str, Any] | None = None) -> Any:
    try:
        return espn.get(base, path, params)
    except espn.ESPNError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


# Teams


@router.get("/teams")
def list_teams() -> Any:
    return _call(espn.SITE_V2, "/teams")


@router.get("/teams/{team_id}")
def get_team(team_id: int) -> Any:
    return _call(espn.SITE_V2, f"/teams/{team_id}")


@router.get("/teams/{team_id}/roster")
def get_roster(team_id: int) -> Any:
    return _call(espn.SITE_V2, f"/teams/{team_id}/roster")


@router.get("/teams/{team_id}/schedule")
def get_schedule(team_id: int, season: int | None = Query(default=None)) -> Any:
    return _call(espn.SITE_V2, f"/teams/{team_id}/schedule", {"season": season})


@router.get("/standings")
def get_standings() -> Any:
    # Standings only works on /apis/v2/ - /apis/site/v2/ returns a stub.
    return _call(espn.SITE_V2_STANDINGS, "/standings")


@router.get("/injuries")
def get_injuries() -> Any:
    return _call(espn.SITE_V2, "/injuries")


# Athletes


@router.get("/athletes/search")
def search_athletes(q: str = Query(min_length=2), limit: int = Query(default=10, le=50)) -> Any:
    return _call(espn.SEARCH_V2, "", {"query": q, "limit": limit})


@router.get("/athletes")
def list_athletes(active: bool = True, page: int = 1, limit: int = Query(default=100, le=1000)) -> Any:
    return _call(espn.CORE_V2, "/athletes", {"active": str(active).lower(), "page": page, "limit": limit})


@router.get("/athletes/{athlete_id}")
def get_athlete(athlete_id: int) -> Any:
    return _call(espn.COMMON_V3, f"/athletes/{athlete_id}/overview")


@router.get("/athletes/{athlete_id}/stats")
def get_athlete_stats(athlete_id: int, season: int | None = Query(default=None)) -> Any:
    return _call(espn.COMMON_V3, f"/athletes/{athlete_id}/stats", {"season": season})


@router.get("/athletes/{athlete_id}/gamelog")
def get_athlete_gamelog(athlete_id: int, season: int | None = Query(default=None)) -> Any:
    return _call(espn.COMMON_V3, f"/athletes/{athlete_id}/gamelog", {"season": season})


@router.get("/athletes/{athlete_id}/splits")
def get_athlete_splits(athlete_id: int, season: int | None = Query(default=None)) -> Any:
    return _call(espn.COMMON_V3, f"/athletes/{athlete_id}/splits", {"season": season})


@router.get("/athletes/{athlete_id}/core")
def get_athlete_core(athlete_id: int) -> Any:
    return _call(espn.CORE_V2, f"/athletes/{athlete_id}")


# Games / historical performance


@router.get("/scoreboard")
def get_scoreboard(
    week: int | None = Query(default=None),
    seasontype: int | None = Query(default=None, ge=1, le=3),
    dates: str | None = Query(default=None, pattern=r"^\d{8}$"),
) -> Any:
    return _call(espn.SITE_V2, "/scoreboard", {"week": week, "seasontype": seasontype, "dates": dates})


@router.get("/games/{event_id}")
def get_game(event_id: int) -> Any:
    return _call(espn.SITE_V2, "/summary", {"event": event_id})


@router.get("/leaders")
def get_leaders(category: str | None = Query(default=None)) -> Any:
    return _call(espn.COMMON_V3, "/statistics/byathlete", {"category": category})


# Seasons / league


@router.get("/seasons")
def list_seasons() -> Any:
    return _call(espn.CORE_V2, "/seasons")


@router.get("/seasons/{season}/draft")
def get_draft(season: int) -> Any:
    return _call(espn.CORE_V2, f"/seasons/{season}/draft")


@router.get("/news")
def get_news() -> Any:
    return _call(espn.SITE_V2, "/news")
