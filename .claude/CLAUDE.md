# AHN — Agentic Hierarchy of Needs

This repo is two things:

1. **A theoretical framework** in `documents/` (4 markdown files: 00 overview, 01 problem, 02 framework, 03 hypothesis, 04 implications). The thesis: agentic software development scales only when human intent, requirements, and executable contracts are established before implementation. Tests are the membrane between the human domain and the agent domain.
2. **An experimentation lab** in `lab/` (Python, pytest, DuckDB) that runs falsifiable experiments against that framework.

When you work here, you're either editing the framework, building the lab, or running experiments. Three modes, three context profiles.

## Modes

| Mode | Working dir | Model | What loads |
|---|---|---|---|
| Framework writing | repo root | Sonnet or Opus | `.claude/rules/framework-vocab.md` + `docs-style.md` on `documents/**` |
| Lab implementation | `lab/` or repo root | Sonnet | `lab/.claude/CLAUDE.md` + `lab/.claude/rules/*` on `lab/**` |
| Experiment running | repo root | Haiku or Sonnet | `/lab-run`, `/lab-report` skills on demand |

## Discipline

- **Framework precedence.** When editing `documents/*.md`, the four-doc consistency matters. Cross-reference before changing terminology.
- **Lab bootstrap exceptions.** The lab itself was built in a single agent-human co-author pass, deviating from the framework's "intent first, contracts before impl" rule. Read `lab/BUILDLOG.md` before judging whether to apply strict AHN discipline to new lab work.
- **Acceptance examples before contracts before code.** When adding a new lab experiment, write `lab/docs/req-EN.md` first, with concrete acceptance examples. Then encode contracts. Then implement.
- **Never silently delete tests.** A failing test is a signal that intent and implementation have diverged. Either change intent above and propagate down, or fix the implementation. Do not edit the test to make it pass.

## Common commands

- `cd lab && ahnlab run --experiment E1 --trials 3` — pilot run of E1 (~$0.01)
- `cd lab && ahnlab report --experiment E1` — aggregate divergence + pass rate per arm
- `cd lab && pytest tests/lab -q` — smoke tests for lab components
- `git status` — already permitted

## Cost posture

Default model is Sonnet (`.claude/settings.json`). Switch to Opus only for theoretical framework work or new experiment design. Switching models invalidates the prompt cache — minimize mid-session model switches.

## Telemetry

The PostToolUse + SessionStart hooks emit edit-level and session-level signals to `lab/runs/claude_telemetry.duckdb` **only when `AHNLAB_TELEMETRY=1` is set**. This data feeds experiment E9 (config impact on agent productivity).

## File pointers

- Framework: `@documents/00-overview.md`
- Lab intent: `@lab/docs/00-intent.md`
- Lab build log (bootstrap exceptions): `@lab/BUILDLOG.md`
- Architecture of this .claude setup: `@.claude/ARCHITECTURE.md`
