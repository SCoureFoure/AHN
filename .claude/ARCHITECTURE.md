# .claude Architecture — AHN Repo

Design doc for how Claude Code is configured in this repo. Treat as intent + requirements layer; the actual config files in this directory are the contracts.

**Status: implemented v1 on 2026-05-24.** See "Status" section at the bottom for the current state and any drift from this design.

---

## Goals (intent)

1. **Cost control.** Cheap sessions wherever cheap suffices. Opus only for genuine design/architecture work.
2. **Context fidelity.** Right instructions load at right time. Framework vocabulary present where AHN docs are touched; lab conventions present where lab code is touched; no global pollution.
3. **Measurable.** Hooks emit signals the lab can consume. .claude config decisions are themselves candidates for AHN lab experiments.
4. **Handoff-safe.** When Opus context fills, drop to Sonnet/Haiku without losing thread. Configuration encodes the thread so the new model doesn't need to re-derive it.
5. **Recursive coherence.** The .claude setup is itself an example of contract-first agentic work — exists to demonstrate AHN principles applied to agent tooling, not just to product code.

---

## Pre-implementation state (audit, retained for record)

This is what the repo looked like before v1 was applied. Kept here as the baseline against which any later config experiment (E9) compares.

| Path | State | Notes |
|---|---|---|
| `.claude/settings.local.json` | Existed | Had cruft: hyper-specific PowerShell allow with escaped chars; one-off `Bash(ls ...)` allow; broad `Read(//c/Users/...)` |
| `.claude/settings.json` | Missing | No team-shared config |
| `.claude/CLAUDE.md` | Missing | No project instructions |
| `.claude/rules/` | Missing | All instructions would have lived in CLAUDE.md without this |
| `.claude/skills/` | Missing | No project skills |
| `.claude/agents/` | Missing | No subagents |
| `.mcp.json` | Missing | No project MCP servers; still missing — none required for v1 |
| `lab/.claude/` | Missing | No nested scope for lab work |
| `~/.claude/projects/c--Users-SCora-...-AHN/memory/` | Auto-created | Auto memory was active from prior sessions before v1 |

---

## Scoping model (the three contexts)

The repo has three distinct work modes. Each gets its own context profile.

### Mode A — Framework writing (Opus or Sonnet, root-launched)

**Work:** Editing `documents/*.md`. Theoretical framework development.

**Context needed:**
- AHN vocabulary (intent/requirements/contracts/membrane/etc.)
- Writing conventions (concise prose, no emojis, specific formatting)
- The four framework docs themselves are subject matter — Claude reads them, doesn't need full content preloaded.

**Where instructions live:**
- Root `.claude/CLAUDE.md` — repo-wide framing, what this project IS, link to AHN docs
- `.claude/rules/framework-vocab.md` — `paths: documents/**` — loads only when touching docs

### Mode B — Lab implementation (Sonnet, lab-launched OR root w/ lab subagent)

**Work:** Implementing experiments E1..E8, harness components, subject codebases.

**Context needed:**
- Python conventions, stack (anthropic SDK, pytest, duckdb, pydantic, rich)
- AHN lab structure (where things go)
- Bootstrap exceptions discipline (BUILDLOG.md)
- Specific experiment requirements

**Where instructions live:**
- `lab/.claude/CLAUDE.md` — nested, loads when lab/ files read
- `lab/.claude/rules/python-style.md` — `paths: lab/**/*.py`
- `lab/.claude/rules/experiments.md` — `paths: lab/experiments/**`

### Mode C — Experiment running + analysis (Haiku acceptable, subagent-friendly)

**Work:** `ahnlab run`, `ahnlab report`, querying DuckDB, summarizing results.

**Context needed:**
- CLI commands
- DuckDB schema knowledge
- Metric interpretation rules

**Where instructions live:**
- `.claude/skills/lab-run/SKILL.md` — `/lab-run` wrapper, on-demand
- `.claude/skills/lab-report/SKILL.md` — `/lab-report` wrapper, on-demand
- `.claude/agents/experiment-analyst.md` — Sonnet subagent, restricted to Read/Grep/Bash for DB queries

---

## File inventory (implemented)

### Committed (team-shared)

| File | Purpose | Approx tokens | Loads when |
|---|---|---|---|
| `.claude/CLAUDE.md` | Repo intent, modes, how to navigate | ~600 | Every session |
| `.claude/settings.json` | Permissions, hooks, statusLine, model default | n/a | Always |
| `.claude/rules/framework-vocab.md` | AHN terminology cheat sheet | ~400 | `documents/**` or `lab/docs/**` read |
| `.claude/rules/docs-style.md` | Writing conventions for framework docs | ~200 | `documents/**/*.md` read |
| `.claude/skills/lab-run/SKILL.md` | `/lab-run` wrapper | ~150 idle, full on invoke | On `/lab-run` |
| `.claude/skills/lab-report/SKILL.md` | `/lab-report` wrapper | ~150 idle | On `/lab-report` |
| `.claude/skills/ahn-experiment-spec/SKILL.md` | Scaffold new `req-EN.md` | ~150 idle | On `/ahn-experiment-spec` |
| `.claude/agents/experiment-analyst.md` | Sonnet subagent for queries | n/a (separate context) | Delegated |
| `.claude/agents/lab-implementer.md` | Sonnet subagent for impl tasks | n/a | Delegated |
| `lab/.claude/CLAUDE.md` | Lab conventions | ~500 | `lab/**` files read |
| `lab/.claude/rules/python-style.md` | Python conventions | ~250 | `lab/**/*.py` read |
| `lab/.claude/rules/experiments.md` | Per-experiment discipline | ~300 | `lab/experiments/**` read |

**Startup cost estimate (root session):** CLAUDE.md ~600 + skill descriptions ~450 = **~1050 tokens** project-side. Rules + lab CLAUDE.md only enter context when relevant files are read.

### Gitignored (personal)

| File | Purpose |
|---|---|
| `.claude/settings.local.json` | Personal permission overrides (slimmed down from current) |
| `CLAUDE.local.md` (project root) | Personal notes (none planned for v1) |

---

## Settings.json — implemented

Final shape ended up more permissive than the original draft. The human selected the "permissive" option to reduce prompt friction during heavy iteration; the deny list still guards irreversibles.

See [.claude/settings.json](settings.json) for the live config.

**Selected permissions:**

- `Bash(gh api *)`, `Bash(ls *)`, `Bash(mkdir -p *)` — low-risk reads/idempotent
- `Bash(git status|diff|log|add|commit|branch|checkout *)` — explicit per-subcommand allowlist
- `Bash(python *)`, `Bash(pytest *)`, `Bash(ahnlab *)` — lab iteration speed
- `Read(./**)` — repo-scoped read, replaces overly broad `Read(//c/Users/...)`
- `WebFetch` domains — Claude Code docs (`code.claude.com`, `docs.anthropic.com`, `platform.claude.com`) + raw.githubusercontent

**Deny list (irreversibles):**

- `Bash(rm -rf *)`
- `Bash(git push --force *)`, `Bash(git push -f *)`
- `Bash(git reset --hard *)`
- `Bash(git clean -fd *)`
- `Bash(git branch -D *)`

**Model default:** `claude-sonnet-4-6` — pinned. Opus invoked per-session when needed for framework theory or new experiment design.

**Hooks:** PostToolUse(Edit|Write) → `lab/.claude_hooks/log_edit.py`; SessionStart → `lab/.claude_hooks/session_start.py`. Both opt-in via `AHNLAB_TELEMETRY=1`.

**StatusLine:** `python .claude/statusline.py` — shows `[model] cache:N% | tele:on|off`.

### Settings.local.json (cleanup)

Strip down to:

```json
{
  "permissions": {
    "allow": []
  }
}
```

Everything currently in there either belongs in `settings.json` (promoted to team) or is one-off cruft that should be re-prompted next time.

---

## Hooks for measurement

Two hooks proposed:

### 1. `PostToolUse(Edit|Write)` → telemetry

Writes one row per edit into a SQLite/DuckDB table tracking:
- timestamp
- file path edited
- claimed lines changed
- session id (env var)
- git branch
- whether path matched any path-scoped rule (computed by hook)

Purpose: measure whether scoped rules are loading when they should, which is the key claim of the .claude scoping strategy.

### 2. `SessionStart` → record session config

Captures: model id, env vars, CLAUDE.md hash, rules manifest hash. Lets us correlate later outcomes (cost, edit count, error rate) with config snapshot.

Both hooks write to `lab/runs/claude_telemetry.duckdb`. Lab gets a new query: `ahnlab claude-stats`.

---

## Subagent design

Two specialized agents.

### `lab-implementer.md`

```yaml
---
name: lab-implementer
description: Implements lab features in lab/src/ahnlab against existing acceptance examples. Use for Python implementation work. Refuses to edit docs/ or rewrite shared requirements.
tools: Read, Edit, Write, Glob, Grep, Bash
model: sonnet
---
```

Body: enforces AHN bootstrap discipline. Reads `lab/BUILDLOG.md` first. Refuses to implement without an acceptance example in `lab/docs/`. Logs any deviation as a new BUILDLOG entry rather than silently proceeding.

### `experiment-analyst.md`

```yaml
---
name: experiment-analyst
description: Queries lab DuckDB, produces aggregates and divergence reports. Use after running ahnlab run.
tools: Read, Grep, Bash
model: sonnet
---
```

Body: knows the schema (runs, membrane_reports, experiments, arms). Refuses to write to artifacts. Returns markdown tables.

Cost benefit: every analyst call is a fresh subagent context — root session doesn't accumulate query noise.

---

## Skills

### `/lab-run`

Thin wrapper: `ahnlab run --experiment $1 --trials ${2:-30}`. Adds confirmation step for `--trials > 50` (cost guard). Tells Claude to read latest BUILDLOG before running so it understands current bootstrap exception state.

### `/lab-report`

Runs `ahnlab report` and additionally writes a markdown snapshot to `lab/runs/reports/E$1-$(date).md`.

### `/ahn-experiment-spec N`

Scaffolds `lab/docs/req-E$1.md` from the E1 template. Forces user to fill acceptance examples before the skill exits (skill emits a `TODO(human)` marker, Claude refuses to proceed past it).

---

## Handoff procedure (Opus → cheaper model)

The expensive Opus session has been used for:
1. Reading framework docs end to end
2. Designing experiment catalog
3. Drafting requirements
4. Scaffolding lab impl

Most future work doesn't need Opus:
- E1 trial execution → automated by `ahnlab run`, no model needed for orchestration
- Result analysis → Sonnet via `experiment-analyst` subagent
- Drafting req-E2..E8 → Sonnet with framework-vocab rule loaded
- Lab component impl backfill → Sonnet via `lab-implementer` subagent

**Procedure:**

1. Apply the .claude config in this doc.
2. Commit framework + lab + .claude state.
3. `/clear` to drop conversation history (system prompt + CLAUDE.md + memory reload fresh).
4. Switch model to Sonnet (`/model claude-sonnet-4-6` or restart with flag).
5. Resume work. Lab CLAUDE.md + rules will load as needed.

Opus should be re-invoked only for:
- New framework theory work (Mode A, deep edits to `documents/`)
- Designing new experiments (E9+)
- Reviewing whether lab results refute the hypothesis (synthesis work)

---

## How this is itself an AHN experiment

Add to req catalog:

**E9 — Config impact on agent productivity.**

Hypothesis: `.claude` configs that follow AHN principles (explicit intent in CLAUDE.md, path-scoped rules acting as contracts, restricted subagent tools acting as enforcement) produce measurably better outcomes than ad-hoc configs.

Design: two `.claude` configs, two arms, same set of tasks (e.g., "add feature X to lab"). Measure: edit count, cost, contract-violation rate, time to green.

This makes the meta-claim falsifiable. If E9 shows no difference, the config theatre is overhead.

---

## Decisions taken on the open questions

| Question | Decision | Rationale |
| --- | --- | --- |
| Allow `ls` and `mkdir -p` team-wide? | Yes, plus `git`, `python`, `pytest`, `ahnlab` subcommands | Permissive option chosen for iteration speed; deny list catches irreversibles |
| Telemetry on by default? | Opt-in via `AHNLAB_TELEMETRY=1` | No surprise DB writes; flip on when running config experiment E9 |
| Subagents project or personal? | Project (committed) | Team-shared so the same restricted-tool agents are available to anyone working in the repo |
| Default model? | Pin to `claude-sonnet-4-6` | Cheaper baseline; Opus invoked explicitly when needed |

---

## Status

**v1 implemented 2026-05-24.** Files in this directory and `lab/.claude/`, `lab/.claude_hooks/` are live. Settings.json validated, hooks smoke-tested off-mode (exit 0 silent), statusline produces output.

**Drift from this doc:** none yet. Update this section if reality diverges.

**Known limitations:**

- The PostToolUse hook does not compute the "did a path-scoped rule load for this file" signal mentioned in the original design. v1 captures timestamp + path + tool name only. Path-scoped-rule attribution requires reading `.claude/rules/*.md` frontmatter and matching globs in the hook, which is straightforward but deferred to v2.
- E9 ("Config impact on agent productivity") is specified but not implementable until E1 produces baseline data and one of E2/E3 is also live. See [lab/docs/req-E9.md](../lab/docs/req-E9.md) for the runbook.
- Subagents are not exercised in this session. First real use happens in the next Sonnet session per HANDOFF.md.
- No `.mcp.json` yet. No MCP servers are required for v1; add one if/when the lab needs external services (e.g., GitHub for issue tracking the experiment results).

**Next config work (if any):**

- Backfill path-scoped-rule attribution in the PostToolUse hook (turns telemetry into a measurement of whether the scoping strategy actually fires).
- Decide whether `~/.claude/output-styles/` should carry an AHN-specific output style (e.g., one that always opens experiment results with the falsifier table). Out of scope for v1.
