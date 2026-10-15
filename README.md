# fantasyfootballdrafter

A fantasy football drafting assistant backed by a RAG pipeline over NFL data.

## What it does

Currently the project provides a FastAPI server that proxies ESPN's public, undocumented NFL API on demand (no persistence).
It can fetch data about:

- **Teams** - all 32 teams, rosters, schedules (current and historical seasons), records, depth charts, standings, injuries, transactions
- **Athletes** - name search to ESPN IDs, profiles, season stats, per-game gamelogs (historical), splits, career stats, awards, head-to-head
- **Games** - scoreboards by week or date (including past seasons), full game summaries with boxscore, drives, play-by-play, win probability
- **League** - stat leaderboards, draft results by year, season lists, news

The endpoint catalog is documented in `docs/espn-nfl-endpoints.md`.

## File structure

```
knowledgeBaseDataGathering/
    app.py            FastAPI entrypoint (uvicorn knowledgeBaseDataGathering.app:app)
    routes.py         APIRouter with /api/nfl/* routes
    espn_client.py    httpx wrapper: base URLs, retry, pagination, .pvt ref rewrite
docs/
    espn-nfl-endpoints.md   Verified NFL endpoint reference + curl examples
    plans/                  Agentic plans (see docs/plans/README.md)
requirements.txt    fastapi, uvicorn, httpx
.venv/              Local virtualenv (gitignored)
```

## Running the server

```bash
.venv/bin/uvicorn knowledgeBaseDataGathering.app:app --reload
```

Interactive API docs at `http://localhost:8000/docs`.

## Notes

- ESPN's API is unofficial and unauthenticated - be respectful with request volume.
- Key gotcha: standings only works on `/apis/v2/` (not `/apis/site/v2/`); per-team `injuries` is a stub, use the league-wide endpoint.
