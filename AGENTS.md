# Agent Instructions

This project uses **bd** (beads) for issue tracking. Run `bd prime` for full workflow context.

## Writing style

Before writing any documentation, report, Notion page, or other prose deliverable, read [`ESTILO_REDACCION.md`](ESTILO_REDACCION.md) and follow it. It requires Spanish, impersonal/passive voice ("se hizo", not "yo hice"), and bans a specific list of AI-sounding filler patterns. This does not apply to code comments or short back-and-forth chat replies.

## Python Environment / Tooling (uv)

This project is managed with **uv** (`uv.lock` is the source of truth for dependencies). Always run Python and CLI tooling through `uv run ...` (e.g. `uv run zenml status`, `uv run pytest`, `uv run python ...`) instead of manually activating `.venv` with `source .venv/bin/activate`. This guarantees the locked dependency set is used and keeps behavior consistent across machines and agents.

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

> **Architecture in one line:** Issues live in a local Dolt database
> (`.beads/dolt/`); cross-machine sync uses `bd dolt push/pull` (a
> git-compatible protocol), stored under `refs/dolt/data` on your git
> remote — separate from `refs/heads/*` where your code lives.
> `.beads/issues.jsonl` is a passive export, not the wire protocol.
>
> See [SYNC_CONCEPTS.md](https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md)
> for the one-screen overview and anti-patterns (don't treat JSONL as the
> source of truth; don't `bd import` during normal operation; don't
> reach for third-party Dolt hosting before trying the default).

## Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work atomically
bd close <id>         # Complete work
bd dolt push          # Push beads data to remote
```

## Non-Interactive Shell Commands

**ALWAYS use non-interactive flags** with file operations to avoid hanging on confirmation prompts.

Shell commands like `cp`, `mv`, and `rm` may be aliased to include `-i` (interactive) mode on some systems, causing the agent to hang indefinitely waiting for y/n input.

**Use these forms instead:**
```bash
# Force overwrite without prompting
cp -f source dest           # NOT: cp source dest
mv -f source dest           # NOT: mv source dest
rm -f file                  # NOT: rm file

# For recursive operations
rm -rf directory            # NOT: rm -r directory
cp -rf source dest          # NOT: cp -r source dest
```

**Other commands that may prompt:**
- `scp` - use `-o BatchMode=yes` for non-interactive
- `ssh` - use `-o BatchMode=yes` to fail instead of prompting
- `apt-get` - use `-y` flag
- `brew` - use `HOMEBREW_NO_AUTO_UPDATE=1` env var

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:970c3bf2 -->
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
- Codex agents: use the `beads` skill at `.agents/skills/beads/SKILL.md` (project install) or `~/.agents/skills/beads/SKILL.md` (global install) for Beads workflow guidance. Codex 0.129.0+ can load this context automatically through native hooks; use `/hooks` to inspect or toggle them.

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
   bd dolt push
   git push
   git status
   ```
5. **Hand off** - Summarize changes, validation, issue status, and any blocked sync/commit/push step

**Critical rules:**
- Explicit user or orchestrator instructions override this Beads block.
- Do not commit or push without clear authority from the active profile or the current user request.
- If a required sync or push is blocked, stop and report the exact command and error.
<!-- END BEADS INTEGRATION -->

## Architecture Overview

This repo estimates daily dewpoint temperature (`TDEW`) for Peru. The production model is a **bucket-year anomaly local-linear-regression** pipeline; several deep-learning experiments benchmark against it.

- `tdew_estimation/` — the production algorithm: climatology (`climatology.py`), anomaly regression training (`anomaly_train.py`, `anomaly_dask.py`), bucketed I/O (`bucketed_data.py`, `bucket_layout.py`, `parquet_io.py`), forecasting (`forecast.py`), metrics/provenance (`metrics.py`, `provenance.py`, `experiment_tracking.py`), and deep models under `tdew_estimation/models/` (TCN + attention pooling).
- `pipeline/` — ZenML-orchestrated ETL from raw PISCO climate rasters to model-ready tables (`bronze.py` → `silver.py` → `gold.py` → `features.py` → `normalize.py` → `sequences.py`/`qc.py`), driven by the DVC stages in `dvc.yaml`.
- `experiments/` — comparisons against the production anomaly model: `baselines/` (simple baselines), `tcn/` (`TCNAttentionModel`, predicts next-day dewpoint anomaly `Td(t+1)` across the four project sites — Lima, Cusco, Loreto, San Martín), `reconstruction/` (continuous `Td` reconstruction protocol, independent of the `Td(t+1)` protocol), `timesfm/` (zero-shot TimesFM 3.0 benchmark).
- `HPC_code/` — SLURM/GPU runners for the production pipeline at scale (multi-node CPU via `dask-jobqueue`, single-GPU via a batched-WLS CuPy kernel) and the scaling-benchmark harness referenced in `reports/pram/tdew_estimation_pram.qmd`.
- `HPC_code_tunning/` — GPU-accelerated search over the DOY half-window `h` and feature set, per SENAMHI climate zone, replacing the fixed global `h=11` used in production.
- `Local/run_pipeline.sh` — single-machine end-to-end runner (climatology → bucketed dataset → Dask training → DOY completeness check → patch).
- `Data/` (`bronze`/`silver`/`gold`/`qc`) — DVC-tracked data lake. `Wiki/` is a separate knowledge base with its own `CLAUDE.md`/`AGENTS.md`.
- `reports/`, `docs/` — benchmark write-ups and results. The PRAM pseudocode/methodology Quarto sources (`tdew_estimation_pram*.qmd`, `TDEW_Avance_Parcial_typst.qmd`, `pram_appendix.qmd`, plus `references.bib`/`apa.csl`/`typst-preamble.typ`) live under `reports/pram/`; their rendered PDF/DOCX outputs live in `docs/pram/`.
- Experiment tracking uses MLflow (`mlflow.db`, `mlruns/`), separate from the bd/Notion task mapping described above.

## Conventions & Patterns

- Run all Python/CLI tooling through `uv run ...` (see Python Environment above); never activate `.venv` manually.
- Data flows through the DVC-tracked stages in `dvc.yaml` in order: bronze → silver → gold → features/normalize/sequences/qc. Don't hand-edit a stage's output — re-run the DVC stage instead.
- Tests live in `tests/` at the repo root, plus per-module `tests/` under `HPC_code/` and `HPC_code_tunning/`. Provenance tests (`test_*_provenance.py`) check that experiment outputs record their inputs/config — follow that pattern for new experiment scripts.
- New deep-learning experiments live under `experiments/<name>/` with their own `zenml_pipeline.py`/`cli.py` and `README.md`, following the layout of `experiments/tcn/` and `experiments/reconstruction/`, rather than adding scripts directly to `tdew_estimation/`.
- Reports and papers are Quarto (`.qmd`) sources rendered to PDF/DOCX — edit the `.qmd`, not the rendered output.
