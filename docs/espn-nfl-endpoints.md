# ESPN NFL API Endpoints

Reference for the NFL-relevant endpoints documented in [pseudo-r/Public-ESPN-API](https://github.com/pseudo-r/Public-ESPN-API).
These are unofficial, undocumented public APIs - no auth required, no published rate limits, subject to change.
All endpoints below were verified returning HTTP 200 on 2026-10-14.

Sport slug: `football`. League slug: `nfl`.

## Base URLs

| Domain | Purpose |
|---|---|
| `site.api.espn.com/apis/site/v2/sports/football/nfl` | Scores, teams, rosters, schedules, game summaries |
| `site.api.espn.com/apis/v2/sports/football/nfl` | Standings only (`/apis/site/v2/` returns a stub for standings) |
| `sports.core.api.espn.com/v2/sports/football/leagues/nfl` | Athletes, seasons, events, stats, odds (deep data, paginated) |
| `sports.core.api.espn.com/v3/sports/football/nfl` | Athletes and leaders, enriched schema |
| `site.web.api.espn.com/apis/common/v3/sports/football/nfl` | Athlete overview, stats, gamelog, splits, bio |
| `site.web.api.espn.com/apis/search/v2` | Global search - resolve player names to ESPN IDs |
| `cdn.espn.com/core/nfl` | Full game packages (drives, play-by-play, win probability) - requires `?xhr=1` |

## Teams

| Endpoint | Returns |
|---|---|
| `GET site.api.espn.com/apis/site/v2/sports/football/nfl/teams` | All 32 teams |
| `GET .../teams/{id}` | Single team detail |
| `GET .../teams/{id}/roster` | Current roster |
| `GET .../teams/{id}/schedule?season={year}` | Season schedule and results |
| `GET .../teams/{id}/record` | Team record |
| `GET .../teams/{id}/leaders` | Team statistical leaders |
| `GET .../teams/{id}/history` | Franchise historical record |
| `GET .../teams/{id}/depthcharts` | Depth chart |
| `GET site.api.espn.com/apis/v2/sports/football/nfl/standings` | League standings - must use `/apis/v2/`, not `/apis/site/v2/` |
| `GET .../injuries` | League-wide injury report |
| `GET .../transactions` | Recent signings, trades, waivers |
| `GET .../groups` | Conferences and divisions |
| `GET sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams?limit=50` | Teams (core schema) |
| `GET sports.core.api.espn.com/v2/.../seasons/{year}/teams` | Teams for a given season |
| `GET sports.core.api.espn.com/v2/.../franchises` | Franchise records |
| `GET sports.core.api.espn.com/v2/.../venues` | Stadiums |

## Athletes

| Endpoint | Returns |
|---|---|
| `GET site.web.api.espn.com/apis/search/v2?query={name}&limit={n}` | Resolve player names to ESPN athlete IDs |
| `GET sports.core.api.espn.com/v2/.../athletes?limit=100&active=true` | Paginated athlete list |
| `GET sports.core.api.espn.com/v2/.../athletes/{id}` | Athlete profile (position, team refs, physicals) |
| `GET .../athletes/{id}/statistics` | Career stats |
| `GET .../athletes/{id}/statisticslog` | Game-by-game stat log |
| `GET .../athletes/{id}/eventlog` | Event history |
| `GET .../athletes/{id}/seasons` | Seasons played |
| `GET .../athletes/{id}/awards` | Awards |
| `GET .../athletes/{id}/injuries` | Injury history |
| `GET .../athletes/{id}/vsathlete/{opponentId}` | Head-to-head stats |
| `GET site.web.api.espn.com/apis/common/v3/.../athletes/{id}/overview` | Profile + stats snapshot + next game + notes |
| `GET .../athletes/{id}/stats?season={year}` | Season stats |
| `GET .../athletes/{id}/gamelog?season={year}` | Per-game logs - best source for historical performance |
| `GET .../athletes/{id}/splits` | Home/away/opponent splits |
| `GET .../athletes/{id}/bio` | Awards and team history |
| `GET .../statistics/byathlete?category={cat}&sort={field}` | League stat leaderboards |
| `GET sports.core.api.espn.com/v2/.../leaders` | Statistical leaders |
| `GET sports.core.api.espn.com/v2/.../seasons/{year}/athletes` | Athletes in a given season |

## Games / Events / Historical Performance

| Endpoint | Returns |
|---|---|
| `GET site.api.espn.com/.../nfl/scoreboard` | Current week scores |
| `GET .../scoreboard?week={n}&seasontype={1\|2\|3}` | Scores by week |
| `GET .../scoreboard?dates={YYYYMMDD}` | Scores by date - works for past dates (e.g. `20201101`) |
| `GET .../summary?event={id}` | Full game summary + boxscore |
| `GET sports.core.api.espn.com/v2/.../events/{id}` | Event metadata |
| `GET .../events/{id}/competitions/{id}/plays` | Play-by-play |
| `GET .../events/{id}/competitions/{id}/odds` | Betting odds |
| `GET .../events/{id}/competitions/{id}/competitors/{id}/statistics` | Team game stats |
| `GET cdn.espn.com/core/nfl/game?xhr=1&gameId={id}` | Full game package: drives, PBP, win prob, boxscore |
| `GET cdn.espn.com/core/nfl/boxscore?xhr=1&gameId={id}` | Boxscore only |
| `GET cdn.espn.com/core/nfl/playbyplay?xhr=1&gameId={id}` | Play-by-play only |

## Seasons / Misc

| Endpoint | Returns |
|---|---|
| `GET sports.core.api.espn.com/v2/.../seasons` | Season list (for historical iteration) |
| `GET sports.core.api.espn.com/v2/.../season` | Current season |
| `GET sports.core.api.espn.com/v2/.../calendar` | Season calendar (weeks, dates) |
| `GET .../seasons/{year}/draft` | Draft results by year |
| `GET .../seasons/{year}/types/2/weeks/{week}/qbr/{split}` | Weekly QBR (split: 0=total, 1=home, 2=away) |
| `GET .../seasons/{year}/types/2/groups/1/qbr/0` | Season QBR totals |
| `GET site.api.espn.com/.../nfl/draft` | Draft board |
| `GET site.api.espn.com/.../nfl/news` | Latest league news |
| `GET sports.core.api.espn.com/v2/.../positions` | Position reference data |

## Key Parameters and Gotchas

- `seasontype`: 1 = preseason, 2 = regular season, 3 = postseason.
- `page` + `limit`: pagination on all Core list endpoints; responses include `pageCount`.
- `dates=YYYYMMDD`: Site scoreboard date filter. Date ranges are unreliable - iterate single dates or use `week` + `seasontype`.
- `season={year}`: scopes team schedules and athlete gamelogs/stats to a year.
- `$ref` URLs in Core responses may point at `sports.core.api.espn.pvt` (ESPN internal). Rewrite `.pvt` to `.com`.
- Per-team `injuries` on Site v2 returns `{}` - use the league-wide `injuries` endpoint and filter by team.
- Not every athlete ID has a headshot on the CDN; prefer `headshot`/`logos` URLs returned inline by roster and athlete endpoints.

## Example Calls

```bash
# All NFL teams
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"

# Week 1 regular season scoreboard
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?week=1&seasontype=2"

# Historical scoreboard
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=20201101"

# Standings (note: /apis/v2/, not /apis/site/v2/)
curl "https://site.api.espn.com/apis/v2/sports/football/nfl/standings"

# Chiefs roster (team id 12)
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/12/roster"

# Patrick Mahomes overview / gamelog (athlete id 3139477)
curl "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/3139477/overview"
curl "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/3139477/gamelog?season=2024"

# Search for a player
curl "https://site.web.api.espn.com/apis/search/v2?query=mahomes&limit=5"

# Full game package via CDN
curl "https://cdn.espn.com/core/nfl/game?xhr=1&gameId={EVENT_ID}"
```
