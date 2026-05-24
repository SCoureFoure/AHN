---
paths:
  - "documents/**"
  - "lab/docs/**"
  - ".claude/ARCHITECTURE.md"
---

# AHN Framework Vocabulary

When editing or referring to AHN documents, use these terms precisely.

## The hierarchy (bottom to top)

1. **Intent** — what the human wants. Originates from a human, full stop.
2. **Requirements** — intent made precise and structured. Human authors with optional agent assistance.
3. **Contracts** — requirements made executable. Tests. **The membrane.** Inviolable from above.
4. **Implementation** — code that satisfies contracts. Agent territory.
5. **State** — data that satisfies implementation. Agent territory.
6. **Infrastructure** — environment supporting everything above. Most agent-autonomous.

## The two laws

- **Law I — Autonomy increases with altitude.** Agents are free at the top, constrained at the membrane, locked out below.
- **Law II — You cannot enforce downward without grounding upward.** Specifying implementation without contracts above is the failure mode that produces silent drift.

## Critical distinctions

- **Contract vs transcript.** A test written from a requirement is a contract. A test written from existing code is a transcript. Transcripts drift with the code; contracts hold the code accountable.
- **Legitimate vs illegitimate contract revision.** Legitimate: intent changed upstream, requirement re-derived, contract updated to encode the new requirement. Illegitimate: test deleted or modified to make a feature ship. The first is honest; the second silently breaches the membrane.
- **Frozen artifact = contract in costume.** Freezing a schema/API/UI is only legitimate if traceable to a requirement above it. Otherwise it's the top-down spec failure mode in disguise.
- **Fuzzy band of the membrane.** Properties like UX quality or LLM eval scores get rubric-graded continuous values, gated against human-set thresholds. Still contracts. Still derived from above. Just not boolean.
- **Layers as roles, not files.** Same artifact can be implementation to one concern, contract to another. Rigidity attaches to the role, not the artifact.

## Falsification conditions (do not soften these)

1. Systems without a formal contract layer that maintain correctness at scale over long horizons by some other mechanism.
2. Evidence that agents can reliably self-evaluate translation correctness without external executable check.
3. Evidence that contract cost consistently exceeds benefit within stated scope conditions.

## Scope (the framework is NOT for)

- Exploratory spikes / prototypes
- Evaluation of agentic feature sets (use eval harnesses instead)
- Security / adversarial robustness (parallel discipline)
- One-off scripts / single-maintainer systems
