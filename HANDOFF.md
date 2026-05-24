# Handoff Checklist — Opus → Sonnet

This file is the procedure to follow when the current Opus session has accomplished its design / architecture goals and the next work is best done by a cheaper model.

## When to hand off

Hand off when the remaining work is one of:

- Implementing existing acceptance examples (impl, not design)
- Running experiments and analyzing results
- Drafting `req-EN.md` for new experiments using the E1 template
- Backfilling tests against established requirements

Do NOT hand off when the next work is:

- New theoretical framework development (`documents/*.md`)
- Designing a fundamentally new experiment class
- Synthesizing whether observed results refute or support the hypothesis at the framework level

## Pre-handoff checklist (run from the current Opus session)

- [ ] All design / architecture decisions are written to disk, not living in conversation context
- [ ] `lab/BUILDLOG.md` is up to date with any bootstrap exceptions taken this session
- [ ] `pytest tests/lab -q` is green (from `lab/`)
- [ ] `.claude/ARCHITECTURE.md` reflects the current config decisions
- [ ] Open questions for the human are written down somewhere durable, not just asked in chat
- [ ] git working tree is clean or staged intentionally
- [ ] Commit (with the human's explicit go-ahead)

## Handoff procedure

1. **Commit** the current state with the human's go-ahead. Recommend a single commit summarizing the session's contribution; the BUILDLOG already records mid-session deviations.

2. **`/clear`** in Claude Code. This drops conversation history. CLAUDE.md, auto memory, settings, and rules will reload from disk.

3. **Switch model.** `.claude/settings.json` already pins default to `claude-sonnet-4-6`. The next session uses Sonnet automatically. To override per-session: `/model claude-sonnet-4-6` or restart with `claude --model claude-sonnet-4-6`.

4. **Resume work.** Tell the new Sonnet session what task to take next. Reference the relevant `lab/docs/req-EN.md` file. The lab CLAUDE.md and rules will load when Sonnet reads lab files.

## When Sonnet must escalate back to Opus

Sonnet should stop and ask for Opus when:

- A task implies changing framework documents (`documents/*.md`) in a way that affects the hypothesis or its falsifiers
- An observation looks like it might refute the framework — synthesis of that should be Opus-grade
- A new experiment class is being proposed (not just a new instance of an existing pattern)
- A `.claude/` config change is proposed that materially affects scoping

Sonnet can write the request as a markdown note in the working directory and stop. The human invokes Opus.

## Cost guardrails

- Default model = Sonnet (in `.claude/settings.json`)
- Lab experiments at Haiku for E1 pilot runs (~$0.01 per 18 trials)
- Opus-only work should fit in one session if possible; the cache-miss cost of resuming a long Opus session can exceed the cost of doing the work fresh
- `AHNLAB_TELEMETRY=1` is opt-in — turn on for sessions where E9 data collection matters, off otherwise

## Files that survive `/clear`

These reload automatically:

- `.claude/CLAUDE.md` (root) — loaded every session
- `.claude/rules/*.md` without `paths:` — loaded every session
- `.claude/skills/*/SKILL.md` descriptions — loaded every session
- Auto memory (`~/.claude/projects/<repo>/memory/MEMORY.md`) — first 200 lines

These reload on demand:

- `lab/.claude/CLAUDE.md` — when lab/ files are read
- `lab/.claude/rules/*.md` with `paths:` — when matching files are read
- Skill bodies — on `/skill-name` invocation

## After-handoff verification

Once the new Sonnet session is running, type `/context` to see what loaded. Expect:

- System prompt (~4-5K tokens, varies)
- Project CLAUDE.md (`.claude/CLAUDE.md`) (~600 tokens)
- Skill descriptions for lab-run, lab-report, ahn-experiment-spec (~450 tokens)
- Auto memory MEMORY.md (variable, capped at 25KB)

Total startup load should be well under 10K tokens — leaves the rest of the context window for actual work.
