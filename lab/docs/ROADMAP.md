# AHN Lab — Future Roadmap

## Vision

The lab becomes a portable agent diagnostic instrument: a plugin that travels to any repo, runs experiments against its codebase, maps agent biases in that context, and writes findings back to the local CLAUDE.md. The documents describe why agent systems fail. The lab finds where and how much.

## The plugin model

The lab ships as an MCP server installable into any Claude Code setup. A developer drops it into a repo, runs `lab diagnose`, and gets a bias report: which contract conditions produce failures in this codebase, what the failure modes look like, and what contract interventions compensate for them. The lab evolves in its own versioned repo; findings stay local.

## What needs to change to get there

1. **Decouple from AHN repo structure.** `LAB_ROOT`, subject paths, and store paths are currently hardcoded or relative to `lab/`. Replace with a `AHNLAB_ROOT` env var and a `AHNLAB_SUBJECTS_ROOT` env var so the lab resolves correctly wherever it's dropped.

2. **MCP server layer.** Wrap the existing CLI commands (`run`, `report`, `diagnose`) as MCP tools. The Claude Code plugin exposes these so agents can call them natively during a session.

3. **Findings writeback.** After a `lab report`, generate a structured findings block that can be appended to the consuming repo's `CLAUDE.md` — a machine-readable bias map for that codebase.

4. **Extract to standalone repo.** Once the bias map has enough shape from AHN experiments (E3–E6 at minimum), extract `lab/` to its own repo with proper packaging, versioning, and a subjects library that ships with it.

5. **Subjects library portability.** The `subjects/` directory at AHN root ships with the standalone lab. When foisted into a real repo, the real codebase's files become subjects; the bundled training ranges remain available for calibration runs.

## When to do this

Not yet. The bias map needs more shape before the plugin interface is worth designing. Run E3–E6 first. When the findings start pointing at a stable set of contract conditions that matter across task classes, that's the signal the interface is ready to define.

Current priority: experiments.
