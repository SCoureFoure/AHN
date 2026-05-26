# Agentic Hierarchy of Needs (AHN)

A theoretical framework and empirical test harness for scalable human-agent software development.

**Core claim:** Agentic development produces drift when agent execution is not grounded by human-authored, executable contracts. The AHN framework defines a rigidity hierarchy — intent → requirements → contracts → implementation — where contracts (tests) form an inviolable membrane. Agents are free above the membrane; locked out below.

---

## What's in this repo

### `documents/` — The Framework

Four markdown documents arguing the theory from first principles. Read in order.

| File | Contents |
| --- | --- |
| `00-overview.md` | Core argument, pyramid diagram, entry point |
| `01-the-problem.md` | Structural ceiling in current agentic practice |
| `02-the-framework.md` | The hierarchy, the two laws, the membrane |
| `03-the-hypothesis.md` | Formal hypothesis, predictions, falsification conditions |
| `04-implications.md` | For designers, agent systems, and the field |

**The central argument** (`00-overview.md`) is that the dominant agentic pattern —

```text
Human states intent → Agent produces code
```

— has no mechanism to verify the output satisfies the intent. It produces drift, slowly in human teams and rapidly in agent-assisted ones, because there is no executable ground truth for the agent to check against. The fix is a rigidity hierarchy where tests form an inviolable membrane between the human domain and the agent domain:

```text
        / INFRA \          ← most agent-autonomous
       /─────────\
      /   STATE   \
     /─────────────\
    / IMPLEMENTATION \
   /─────────────────\
  /     CONTRACTS     \
 /═══════════════════════\  ← The Membrane
/      REQUIREMENTS       \
/─────────────────────────\
/          INTENT           \  ← must originate from human
```

Agents work above the membrane. Humans own below it. The membrane is inviolable.

**The hypothesis** (`03-the-hypothesis.md`) is formal and falsifiable — the document names specific findings that would constitute evidence against the framework, and commits to them. One of the more counterintuitive predictions: partial contracts are worse than no contracts on uncovered behaviors, because they compress the agent's solution space toward visible cases only while leaving invisible cases more variable than they would be under unconstrained generation. That claim is testable and the lab is designed to test it.

These docs are the theory. The lab tests whether the theory holds.

### `lab/` — The Experiment Harness

Python CLI (`ahnlab`) that runs controlled experiments measuring the effect of contract presence on agent output quality. Each experiment pits two or more arms against each other — e.g., agents given contracts vs. agents given only intent — and scores results against a hidden judge suite the agent never sees.

Results land in a DuckDB store at `lab/runs/`. See `lab/README.md` for setup and `lab/docs/` for per-experiment requirements.

### `subjects/` — The Test-Bed Codebases

Reusable small codebases used as tasks inside experiments. A subject is a mini-project with cycles of evolving feature requests — each cycle has an `intent.md`, `contracts.py` (what an arm can show the agent), and `hidden/` tests (what the experiment scores against, invisible to the agent).

Subjects are neutral: they carry no experiment-specific logic. Experiments pull from subjects and decide what context each arm provides.

---

## How the three parts connect

```text
documents/          lab/                    subjects/
──────────          ───────────────────     ─────────────────────────
Framework theory  → Experiments test it  ← Subjects are the tasks
                    (arms vary what         (multi-cycle codebases
                    context agents see)      with hidden judge suites)
```

The framework predicts: agents with contracts outperform agents without. The lab runs that comparison. Subjects provide the comparable, repeatable coding tasks the comparison runs on.

---

## Concrete example: E2 (Contract Completeness)

**What it tests.** E1 found that giving agents contracts reduced behavioral divergence. E2 asks the follow-up: does *completeness* matter, or do any contracts help equally? The framework predicts divergence decreases monotonically with coverage. That's a falsifiable, quantitative claim.

**The arms.** Four groups of agent sessions, all given the same task, each seeing a different amount of specification:

| Arm | What the agent sees |
| --- | --- |
| A | Intent text only — no contracts |
| B | Intent + 2 acceptance examples (happy path only) |
| C | Intent + same 2 examples + explicit warning that more edge cases exist |
| D | Intent + all 9 acceptance examples (full coverage) |

All four arms are scored against the same hidden judge suite the agent never sees. That hidden suite is the membrane — it can't be edited after the run starts.

**The subject: `normalize_tags`.** Experiments need tasks where model behavior is genuinely ambiguous, not tasks the model has memorized from training. `normalize_tags` was selected specifically because at temperature=0 with only the intent, the model still produces divergent outputs across sessions — agents disagree on whether to strip whitespace, drop `None`, preserve insertion order during dedup, or sort. Those disagreements are exactly the edge cases the four arms resolve by degrees.

The subject lives in `subjects/normalize_tags/` as a reusable probe. E2 pulls from it and defines what each arm shows the agent. If a future experiment wants to test a different variable on the same task, it can point at the same subject without touching E2.

**The prediction.** Pass rate on the hidden suite increases A → B → C → D. If A passes as often as D, either the subject is memorized (invalid experiment) or contracts don't help (framework falsified). The requirement doc commits to both outcomes.

---

## Quick start (lab)

```bash
cd lab
python -m venv .venv
.venv\Scripts\Activate.ps1      # PowerShell; use source .venv/bin/activate on Unix
pip install -e .
cp .env.example .env            # add ANTHROPIC_API_KEY
ahnlab init

ahnlab run --experiment E1 --trials 3
ahnlab report --experiment E1
```
