# Project Instructions for AI Agents

This file provides instructions and context for AI coding agents working on this project.

## Project Timeline / Planning (Notion)

This project's timeline and day-by-day plan live in Notion, not in this repo:

https://app.notion.com/p/Timeline-Planner-86999c87538483bbb30a81974bf2dc50

Whenever the user asks what is planned for a given day, week, or milestone (e.g. "qué hay planeado para el día X"), consult this Notion page via the Notion MCP tools (`notion-fetch` / `notion-search`) before answering — do not guess from repo state or bd issues alone.

### bd ↔ Notion task mapping

The tasks database inside the Timeline Planner is the "Gantt Chart" data source (`collection://6d399c87-5384-8237-81a4-87812c222f13`), with properties `Task/Project Name`, `Status` (Not Started / In Progress / On Hold / Delayed / Completed), `Progress` (0–1), `Start Date`, `End Date`, `Blocked by` / `Blocking`, `Priority`, `Category`.

Each row now has a `Bead ID` (rich text) property holding the matching `bd` issue id (e.g. `tdew-cra`). This property was added on 2026-09-15 because no mapping existed before — task titles happened to match bead titles exactly, but that was never guaranteed. Always match by `Bead ID`, not by title.

**Closing a bead updates Notion.** A `PostToolUse` hook on `Bash` in `.claude/settings.json` detects when a `bd close <id...>` command runs and injects a reminder into context with the bead id(s). The hook cannot call Notion itself (a shell hook has no MCP access) — when you see that reminder, you (the agent) must:
1. Query the `Gantt Chart` data source for the row whose `Bead ID` equals the closed bead id.
2. Update that row via the Notion MCP `update-page` tool: set `Status` = `Completed` and `Progress` = `1`.

When creating a new bead for a task that also exists (or will exist) as a Notion row, set that row's `Bead ID` property so this mapping stays intact.

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:6cd5cc61 -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md for details and anti-patterns.

## Agent Context Profiles

The managed Beads block is task-tracking guidance, not permission to override repository, user, or orchestrator instructions.

- **Conservative (default)**: Use `bd` for task tracking. Do not run git commits, git pushes, or Dolt remote sync unless explicitly asked. At handoff, report changed files, validation, and suggested next commands.
- **Minimal**: Keep tool instruction files as pointers to `bd prime`; use the same conservative git policy unless active instructions say otherwise.
- **Team-maintainer**: Only when the repository explicitly opts in, agents may close beads, run quality gates, commit, and push as part of session close. A current "do not commit" or "do not push" instruction still wins.

## Session Completion

This protocol applies when ending a Beads implementation workflow. It is subordinate to explicit user, repository, and orchestrator instructions.

1. **File issues for remaining work** - Create beads for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **Handle git/sync by active profile**:
   ```bash
   # Conservative/minimal/default: report status and proposed commands; wait for approval.
   git status

   # Team-maintainer opt-in only, unless current instructions forbid it:
   git pull --rebase
   git push
   git status
   ```
5. **Hand off** - Summarize changes, validation, issue status, and any blocked sync/commit/push step

**Critical rules:**
- Explicit user or orchestrator instructions override this Beads block.
- Do not commit or push without clear authority from the active profile or the current user request.
- If a required sync or push is blocked, stop and report the exact command and error.
<!-- END BEADS INTEGRATION -->


## Build & Test

This project is managed with **uv** (`uv.lock` is the source of truth for dependencies). Always run Python/CLI tooling through `uv run ...` (e.g. `uv run zenml status`, `uv run pytest`) instead of manually activating `.venv` — this guarantees the locked dependency set is used and keeps behavior consistent across machines and agents.

```bash
# Example:
# uv sync
# uv run pytest
```

## Architecture Overview

_Add a brief overview of your project architecture_

## Conventions & Patterns

_Add your project-specific conventions here_
