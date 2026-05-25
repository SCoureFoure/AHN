---
description: Audit the prompt ecosystem — crawl all CLAUDE.md, skills, hooks, rules, and settings files, then map interactions and score against six failure modes.
argument-hint: [path] (optional — defaults to repo root)
---

# /desk-check

Audit the active prompt configuration of this repository. Do NOT ask the user to paste anything. Crawl the filesystem yourself.

## Step 1 — Discover artifacts

Search for all prompt-relevant files. Run these globs from the root (or `$1` if provided):

- `**/.claude/CLAUDE.md` — project and nested project instructions
- `**/.claude/settings.json` — model defaults, permission rules, hook registrations
- `**/.claude/rules/**/*.md` — always-loaded rule files
- `**/.claude/skills/**/*.md` — user-invocable skill definitions
- `**/.claude/agents/**/*.md` — sub-agent definitions
- `**/.claude_hooks/**/*.py` — hook scripts referenced in settings

Also read any hook script paths listed in `settings.json` under `hooks`.

For each file found: read it in full.

## Step 2 — Inventory table

Produce a markdown table with one row per artifact:

| Name | Type | Scope | Grants | Restricts | Assumes |
|---|---|---|---|---|---|

- **Type**: CLAUDE.md / settings / rule / skill / hook / agent
- **Scope**: when does this activate? (always-on, per-command `/cmd`, per-tool-call, nested project only, etc.)
- **Grants**: behaviors/permissions/capabilities this artifact enables
- **Restricts**: behaviors this artifact explicitly forbids or constrains
- **Assumes**: what this artifact takes for granted about the environment or other artifacts

## Step 3 — Dependency map

For each pair of artifacts that share a topic, behavior, or assumption, write one edge:

```
[A] → [B] : [shared topic]  — [relationship: overrides / depends on / conflicts with / leaves gap with]
```

Flag conflicts (`!`) and gaps (`?`) explicitly. A conflict is two artifacts saying different things about the same case. A gap is a case where both are silent but a reasonable agent might need guidance.

## Step 4 — Interaction audit

For each edge from Step 3, score these six failure modes. Return **pass**, **warn**, or **fail** with a one-sentence reason.

### Failure modes (from AHN research)

**Intent drift** *(E1)*
Ambiguous intent at the interaction point. Two agents reading both artifacts could make meaningfully different choices on the same input.
Check: is there a wrong-but-plausible interpretation that produces significantly different behavior?

**Partial suppression** *(E2 B_partial)*
One artifact partially specifies a behavior with examples or constraints. Incomplete specification can suppress the model's correct defaults, producing worse behavior on uncovered cases than if no specification existed.
Check: for each set of examples or constraints, is there a plausible uncovered case where the specification steers the agent away from the correct default?

**False completeness** *(E2 no-warning)*
An artifact specifies some cases without signaling incompleteness. The agent infers it has complete instructions and confidently fills gaps incorrectly.
Check: does any artifact read as exhaustive when it is not? Is a caveat like "these examples are not exhaustive" missing where it should appear?

**Cascade regression** *(E3)*
A later or more specific artifact touches behavior established by an earlier or more general one, potentially breaking it silently.
Check: for each newer/more-specific artifact, what behaviors did earlier/more-general artifacts establish that this one could override or contradict?

**Scope leak**
An artifact grants capability or uses permissive phrasing ("use your judgment," "be helpful") without explicit bounds. The agent interprets the surface as authorizing more than intended.
Check: for each capability granted, is there an explicit bound on when/how to use it? Could a reasonable agent do something unintended but not explicitly forbidden?

**Falsifiability gap** *(framework membrane)*
No artifact makes failure detectable. The agent can produce wrong output with no mechanism to surface it.
Check: if this agent produced consistently wrong output, what in the configuration would catch it?

## Step 5 — Output

### Summary table

| Surface | Artifacts | Drift | Suppression | False completeness | Cascade | Scope | Falsifiability |
|---|---|---|---|---|---|---|---|

### Findings

For each **warn** or **fail**:

```
Finding [N]: [short title]
Surface: [Artifact A] × [Artifact B] on [topic]
Failure mode: [name]
Risk: [what could go wrong, concretely — one sentence]
Evidence: [exact quote or paraphrase of the text creating the risk]
Fix: [specific change to resolve it]
```

### Verdict

- **Clean** — no fails, at most minor warns
- **Caution** — warns present; review before relying on this configuration in production
- **Unsafe** — one or more fails; agent should not run as-is without changes

---

After the verdict, list any artifacts you could not read (permissions, missing files) so the user knows what was excluded from the audit.
