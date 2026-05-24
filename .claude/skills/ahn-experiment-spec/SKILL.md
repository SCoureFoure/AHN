---
description: Scaffold a new AHN lab experiment requirements doc with acceptance examples. Usage: /ahn-experiment-spec <N> <short-name>
argument-hint: <N> <short-name>
---

# /ahn-experiment-spec

Scaffold `lab/docs/req-E$1.md` for experiment $1 with short name $2.

Read `lab/docs/req-E1.md` as the template. Mirror its structure exactly: Design, Subjects, Acceptance examples, Metrics, Falsifiers for this experiment specifically, Acceptance examples for the runner code itself.

The new file MUST include `TODO(human)` markers in every section the human needs to fill — specifically:

- The hypothesis target (which hypothesis or corollary from `documents/03-the-hypothesis.md` this experiment tests)
- The acceptance examples (concrete inputs and outputs)
- The predicted result
- The falsifier specific to this experiment

Do not invent acceptance examples. Do not predict results. Those originate from the human. Your job is the scaffolding; the human fills the substantive intent.

After writing, print a list of every `TODO(human)` location and STOP. Do not continue to encode contracts or write code until the human has filled the TODOs and explicitly continues.
