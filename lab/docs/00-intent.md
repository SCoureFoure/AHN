# AHN Lab — Intent

## Purpose

Validate the Agentic Hierarchy of Needs framework empirically. Produce repeatable experiments that test the hypothesis (3.1), corollaries (3.2), and falsifiers (3.3) of `documents/03-the-hypothesis.md`.

## Scope

The lab is itself a software system. Its job is to:

1. Run agent tasks against controlled conditions (with/without contracts, with/without frozen artifacts, across sequential cycles, across parallel sessions).
2. Capture artifacts, traces, costs, and outcomes per run.
3. Score outcomes against programmatic and rubric-graded contracts.
4. Aggregate results across arms and produce statistically interpretable comparisons.

## Out of scope (v1)

- Production agent orchestration (no Managed Agents API yet).
- Multi-language test runners (Python + pytest only at start).
- Web UI (CLI + DuckDB queries sufficient).
- Real production codebases as subjects (synthetic + curated minimal subjects).

## Meta-position

The framework requires intent originate from a human. This lab is being designed in co-authorship between a human and an agent for bootstrap velocity. That deviation is acknowledged in writing. If the lab proves the framework, the deviation becomes a recorded anomaly worth examining. If the lab fails to prove the framework, the deviation becomes one candidate explanation among several. Either way, the deviation is not hidden.

## Success criteria

The lab is successful if, six months from start, it can answer the following with evidence:

- Does interpretation variance across fresh agent sessions collapse when contracts are present? (E1)
- Do tests-as-transcript detect injected bugs at lower rates than tests-as-contract? (E2)
- Does regression rate per feature cycle diverge between hierarchy-first and free-edit arms across N cycles? (E3)
- Does the contract axis dominate the capability axis in a 2x2 design? (E4)
- Do agents attempt to breach the membrane more often as upper-layer autonomy increases, and does enforcement hold? (E5)
- How reliable are LLM-graded contracts under judge perturbation? (E6)
- Where does contract-first economics break even against impl-first? (E7)
- Does agent self-evaluation accuracy plateau below contract-evaluation accuracy? (E8)

## Non-goals

- The lab is not a benchmark suite for model capability.
- The lab does not rank vendors or models against each other for marketing purposes.
- The lab does not produce normative claims about how teams should work. It produces evidence about a specific framework.

## Stack

- Python 3.11+
- `anthropic` SDK (Messages, Batches)
- `pytest` for programmatic membrane
- `pydantic` for typed configs and rubrics
- `duckdb` for results store
- `rich` for CLI output

## Operating principle

The lab will be built hierarchy-first wherever feasible. Every component must carry at least one acceptance example before implementation. Components that cannot be built that way will be flagged in the build log as bootstrap exceptions.
