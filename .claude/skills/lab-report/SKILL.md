---
description: Generate aggregate report for an AHN lab experiment and snapshot to disk. Usage: /lab-report <experiment-id>
argument-hint: <experiment-id>
---

# /lab-report

Generate and persist the aggregate report for an experiment.

```bash
cd lab && ahnlab report --experiment $1
```

Then write a markdown snapshot to `lab/runs/reports/$1-$(date +%Y%m%d-%H%M%S).md` containing:

1. The report table verbatim
2. A one-paragraph interpretation that ONLY says what the numbers literally show. Do not extrapolate.
3. Whether the experiment's predicted result (from `lab/docs/req-$1.md`) was observed.

If the predicted result was observed, say so. If it was not, say so plainly and list the candidate explanations from the experiment's own falsifier section. Do not editorialize beyond that.
