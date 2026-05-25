# AHN Subjects — Training Range Library

Reusable test-bed codebases for lab experiments. These are the probes.

## What belongs here

Multi-cycle subjects — small but realistic codebases that evolve across feature cycles and expose specific agent bias classes. Not single functions (those are experiment-specific and live in `lab/experiments/EN/subjects/`).

Each subject is chosen to probe a named bias, not just to be "something agents might get wrong."

## Structure per subject

```
subjects/<name>/
  meta.md          ← what bias this probes, cycle count, validated capability notes
  cycles/
    c1/intent.md   ← feature request the agent sees at cycle 1
    c2/intent.md
    ...
  seeds/
    c1_seed.py     ← empty or minimal stub (starting point for cycle 1)
    c2_seed.py     ← correct cycle 1 impl (starting point for cycle 2 in snapshot mode)
    ...
  hidden/
    hidden_c1.py   ← tests for cycle 1 behaviors only
    hidden_c2.py   ← cumulative: c1+c2
    ...
```

Arm-specific contracts live in `lab/experiments/EN/` — not here. Subjects are neutral. Experiments define what the agent sees.

## Catalog

| Subject | Cycles | Bias probed | Status |
|---|---|---|---|
| todo_list | 4 | Compounding regression without contract accumulation | Planned (E3) |
