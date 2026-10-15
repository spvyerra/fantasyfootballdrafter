---
agent: devin-local
session: lavish-bellflower
created: 2026-10-15T01:04:59Z
---
# NFL ESPN API endpoint map + basic FastAPI data-gathering server

Document the NFL-relevant ESPN public API endpoints (verified live) in docs/, then build a basic FastAPI server in `knowledgeBaseDataGathering/` that proxies those endpoints on demand for athlete, team, and historical performance data.

## Summary

Filter the pseudo-r/Public-ESPN-API docs to NFL-only endpoints (sport slug `football`, league slug `nfl`), verify them live (all returned 200 on 2026-10-14), write a lasting reference doc at `docs/espn-nfl-endpoints.md`, and implement a small FastAPI server that fetches ESPN data on demand (no persistence).

Decisions (from user): **FastAPI**, **fetch-on-demand** (thin proxy, store nothing), **endpoint list goes in `docs/`**.

## NFL-Relevant Endpoint List (verified 200 on 2026-10-14)

### Base URLs

| Domain | Purpose |
|---|---|
| `site.api.espn.com/apis/site/v2/sports/football/nfl` | Scores, teams, rosters, schedules, game summaries |
| `site.api.espn.com/apis/v2/sports/football/nfl` | Standings ONLY (`/apis/site/v2/` returns a stub here) |
| `sports.core.api.espn.com/v2/sports/football/leagues/nfl` | Athletes, seasons, events, stats, odds (deep data, paginated) |
| `sports.core.api.espn.com/v3/sports/football/nfl` | Athletes/leaders, enriched schema |
| `site.web.api.espn.com/apis/common/v3/sports/football/nfl` | Athlete overview/stats/gamelog/splits/bio |
| `site.web.api.espn.com/apis/search/v2` | Global search - resolve player names to ESPN IDs |
| `cdn.espn.com/core/nfl` | Full game packages (drives, PBP, win prob) - requires `?xhr=1` |

### Teams

| Endpoint | Returns |
|---|---|
| `GET site.api.espn.com/apis/site/v2/sports/football/nfl/teams` | All 32 teams |
| `GET .../teams/{id}` | Single team detail |
| `GET .../teams/{id}/roster` | Current roster |
| `GET .../teams/{id}/schedule?season={year}` | Season schedule/results |
| `GET .../teams/{id}/record` | Team record |
| `GET .../teams/{id}/leaders` | Team stat leaders |
| `GET .../teams/{id}/history` | Franchise historical record |
| `GET .../teams/{id}/depthcharts` | Depth chart |
| `GET site.api.espn.com/apis/v2/sports/football/nfl/standings` | Standings (must use `/apis/v2/`) |
| `GET .../injuries` | League-wide injury report |
| `GET .../transactions` | Signings/trades/waivers |
| `GET .../groups` | Conferences/divisions |
| `GET sports.core.../v2/.../teams?limit=50`, `.../seasons/{yr}/teams`, `.../franchises`, `.../venues` | Core-schema variants |

### Athletes

| Endpoint | Returns |
|---|---|
| `GET site.web.api.espn.com/apis/search/v2?query={name}` | Name -> ESPN athlete ID |
| `GET sports.core.../v2/.../athletes?limit=100&active=true` | Paginated athlete list |
| `GET sports.core.../v2/.../athletes/{id}` | Profile (position, team refs) |
| `GET .../athletes/{id}/statistics` | Career stats |
| `GET .../athletes/{id}/statisticslog` | Game-by-game log |
| `GET .../athletes/{id}/seasons`, `/awards`, `/injuries`, `/eventlog` | History sub-resources |
| `GET .../athletes/{id}/vsathlete/{oppId}` | Head-to-head |
| `GET site.web.api.espn.com/apis/common/v3/.../athletes/{id}/overview` | Profile + stats snapshot + notes |
| `GET .../athletes/{id}/stats?season={year}` | Season stats |
| `GET .../athletes/{id}/gamelog?season={year}` | Per-game logs (best for historical performance) |
| `GET .../athletes/{id}/splits`, `/bio` | Splits / awards & team history |
| `GET .../statistics/byathlete?category={cat}` | League leaderboards |
| `GET sports.core.../v2/.../leaders`, `.../seasons/{yr}/athletes` | Leaders / per-season athletes |

### Games / Historical Performance

| Endpoint | Returns |
|---|---|
| `GET site.api.espn.com/.../nfl/scoreboard?week={n}&seasontype={1,2,3}` | Scores by week |
| `GET .../scoreboard?dates={YYYYMMDD}` | Scores by date (works historically, e.g. 20201101) |
| `GET .../summary?event={id}` | Full game summary + boxscore |
| `GET sports.core.../v2/.../events/{id}`, `.../competitions/{id}/plays`, `/odds`, `/competitors/{id}/statistics` | Event detail, PBP, odds, team game stats |
| `GET cdn.espn.com/core/nfl/game?xhr=1&gameId={id}` | Full game package (also `/boxscore`, `/playbyplay`) |

### Seasons / Misc

`seasons`, `season` (current), `calendar`, `seasons/{yr}/draft`, `seasons/{yr}/types/2/weeks/{w}/qbr/{split}`, site `draft`, `news`, `positions`.

### Key parameters / gotchas

- `seasontype`: 1=preseason, 2=regular, 3=postseason
- `page` + `limit` on all Core list endpoints (response includes `pageCount`)
- Site scoreboard `dates` ranges are unreliable - iterate single dates or use week+seasontype
- Core `$ref` URLs may point at `sports.core.api.espn.pvt` - rewrite `.pvt` -> `.com`
- Per-team `injuries` (site v2) returns `{}` - use league `injuries` and filter

## Implementation Steps

1. Save this plan to `docs/plans/2026-10-14-espn-nfl-api-server.md` (per AGENTS.md).
2. Write `docs/espn-nfl-endpoints.md` - the endpoint reference above with curl examples and gotchas.
3. Create `requirements.txt` (fastapi, uvicorn, httpx) - check for an existing venv/package setup first.
4. `knowledgeBaseDataGathering/espn_client.py` - httpx `Client` wrapper: base URL constants, `get(path, params)`, timeout + one retry, `User-Agent` header, `.pvt` -> `.com` ref rewriting helper, `paginate()` helper following `pageCount`.
5. `knowledgeBaseDataGathering/routes.py` - FastAPI `APIRouter` (replaces the empty stub) exposing on-demand routes:

| Route | Backing ESPN call |
|---|---|
| `GET /api/nfl/teams` | site v2 `teams` |
| `GET /api/nfl/teams/{id}` | site v2 `teams/{id}` |
| `GET /api/nfl/teams/{id}/roster` | site v2 `teams/{id}/roster` |
| `GET /api/nfl/teams/{id}/schedule?season=` | site v2 `teams/{id}/schedule` |
| `GET /api/nfl/standings` | site `/apis/v2/standings` |
| `GET /api/nfl/athletes/search?q=` | search v2 |
| `GET /api/nfl/athletes/{id}` | common v3 `overview` |
| `GET /api/nfl/athletes/{id}/stats?season=` | common v3 `stats` |
| `GET /api/nfl/athletes/{id}/gamelog?season=` | common v3 `gamelog` |
| `GET /api/nfl/scoreboard?week=&seasontype=&dates=` | site v2 `scoreboard` |
| `GET /api/nfl/games/{id}` | site v2 `summary` |
| `GET /api/nfl/leaders?category=` | common v3 `statistics/byathlete` |

6. `knowledgeBaseDataGathering/app.py` - `FastAPI()` app, `include_router`, uvicorn entrypoint (`uvicorn app:app --reload`).

## Files to Modify / Create

- `docs/plans/2026-10-14-espn-nfl-api-server.md` - plan copy (required by AGENTS.md)
- `docs/espn-nfl-endpoints.md` - NEW, endpoint reference
- `knowledgeBaseDataGathering/espn_client.py` - NEW
- `knowledgeBaseDataGathering/routes.py` - replace stub
- `knowledgeBaseDataGathering/app.py` - NEW
- `requirements.txt` - NEW (if no env tooling found)

## Verification

- `python -m compileall knowledgeBaseDataGathering/` then `uvicorn` boot + `GET /docs`
- `curl` each new route; compare against direct ESPN calls (all already verified 200)
- Historical spot-checks: 2020 scoreboard date, prior-season gamelog, past-season team schedule

## Risks / Notes

- Unofficial API: no auth, undocumented rate limits, can change without notice - client includes timeout/retry and honest 5xx passthrough.
- Fetch-on-demand means every server route costs an ESPN round-trip; if later needed for RAG bulk ingestion, add snapshot persistence as a follow-up.

## Status

**completed** (2026-10-14)

- [x] Plan saved to `docs/plans/`
- [x] `docs/espn-nfl-endpoints.md` endpoint reference written
- [x] `requirements.txt` + `.venv` created (fastapi 0.143.1, httpx 0.28.1, uvicorn 0.54.0)
- [x] `espn_client.py`, `routes.py`, `app.py`, `__init__.py` implemented
- [x] Verified: all routes return 200 with real data (teams=32, search resolves Mahomes->3139477, 2023 gamelog=20 events, 2020 scoreboard=12 games, summary=full boxscore+drives+winprob)
