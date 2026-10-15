# FootBallRag agent instructions

Project-specific rules for agents working in this repository.
Global guidelines live in `~/.config/devin/AGENTS.md` and apply here as well.

## Agentic Plans

- Every agentic plan produced while working on this project MUST be saved as a Markdown file in `/docs/plans/`.
- Plans must be written to `/docs/plans/` before implementation begins, so the user can review them.
- Name plan files `YYYY-MM-DD-<short-slug>.md` (e.g., `2026-10-14-rag-pipeline-redesign.md`).
- Append a suffix like `-v2` when iterating on a plan rather than overwriting the original, so planning history is preserved.
- Keep the plan file updated as work progresses: mark steps done and reflect any scope changes, so the file remains an accurate record.
- See `/docs/plans/README.md` for the expected contents of a plan file.

## README Maintenance

- After executing each plan, update the project-level `README.md`.
- The README should give a high-level overview of what the project is able to do and the general file structure, so future sessions are aware of how things are structured.

## Pull Requests

- After executing each plan, create a pull request containing all of the relevant changes.
