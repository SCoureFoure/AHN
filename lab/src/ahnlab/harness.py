"""R1 Task Harness — runs one agent task end-to-end and records the result.

Flow:
1. Stage subject intent + any provided contracts/extra files into a fresh artifacts dir.
2. Build the prompt: system + user (intent text + contract excerpts if include_contracts).
3. Call Messages API.
4. Parse output for fenced code blocks → write to artifacts dir as solution.py.
5. Capture transcript, tokens, cost, request id → RunRecord.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import uuid
from pathlib import Path

from anthropic import Anthropic, APIError, APIStatusError

from .config import ANTHROPIC_API_KEY, RUNS_DIR, compute_cost_usd, lab_git_sha
from .models import RunRecord, TaskSpec, utcnow


SYSTEM_PROMPT_DEFAULT = (
    "You are a Python implementer. You will be given a requirement. "
    "Reply with a single fenced ```python``` code block containing the requested "
    "function in a file conceptually named solution.py. Do not include explanation "
    "outside the code block. Do not include __main__ guards. Do not print anything."
)

SYSTEM_PROMPT_CYCLE = (
    "You are a Python implementer. You will be given an existing implementation and a "
    "feature request. Reply with a single fenced ```python``` code block containing the "
    "complete updated implementation in a file conceptually named solution.py. Include all "
    "prior functionality. Do not include explanation outside the code block. "
    "Do not include __main__ guards. Do not print anything."
)


_FENCE_RE = re.compile(r"```(?:python)?\s*\n(.*?)```", re.DOTALL)


def _extract_code(text: str) -> str | None:
    m = _FENCE_RE.search(text)
    if m:
        return m.group(1).rstrip() + "\n"
    return None


def _prompt_hash(parts: list[str]) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update(p.encode("utf-8"))
        h.update(b"\x00")
    return h.hexdigest()


def _build_user_content(spec: TaskSpec, include_contracts: bool) -> str:
    parts = [f"# Requirement\n\n{spec.intent_text.strip()}\n"]
    if include_contracts and spec.contract_files:
        parts.append("\n# Acceptance contracts (pytest)\n")
        parts.append(
            "Your solution must make every test below pass when placed alongside solution.py.\n\n"
        )
        for cf in spec.contract_files:
            content = Path(cf).read_text(encoding="utf-8")
            parts.append(f"## {Path(cf).name}\n\n```python\n{content}\n```\n")
    return "".join(parts)


def _build_cycle_content(intent_text: str, prior_code: str, include_contracts: bool, contract_files: list[Path]) -> str:
    parts = [
        f"# Current implementation\n\n```python\n{prior_code.strip()}\n```\n\n",
        f"# Feature request\n\n{intent_text.strip()}\n",
    ]
    if include_contracts and contract_files:
        parts.append("\n# Acceptance contracts (pytest)\n")
        parts.append(
            "Your updated implementation must make every test below pass when placed alongside solution.py.\n\n"
        )
        for cf in contract_files:
            content = Path(cf).read_text(encoding="utf-8")
            parts.append(f"## {Path(cf).name}\n\n```python\n{content}\n```\n")
    return "".join(parts)


def run_task(
    spec: TaskSpec,
    experiment_id: str,
    arm_id: str,
    seed: int,
    include_contracts: bool,
    client: Anthropic | None = None,
) -> RunRecord:
    run_id = uuid.uuid4().hex[:16]
    artifacts_dir = RUNS_DIR / experiment_id / arm_id / spec.subject / run_id
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = artifacts_dir / "transcript.jsonl"

    system = spec.system_prompt or SYSTEM_PROMPT_DEFAULT
    user_content = _build_user_content(spec, include_contracts)
    prompt_hash = _prompt_hash([system, user_content, spec.model, str(spec.temperature)])

    started_at = utcnow()
    client = client or Anthropic(api_key=ANTHROPIC_API_KEY)

    record_kwargs = dict(
        run_id=run_id,
        task_id=spec.task_id,
        subject=spec.subject,
        experiment_id=experiment_id,
        arm_id=arm_id,
        seed=seed,
        model=spec.model,
        transcript_path=transcript_path,
        artifacts_dir=artifacts_dir,
        prompt_hash=prompt_hash,
        lab_git_sha=lab_git_sha(),
    )

    try:
        response = client.messages.create(
            model=spec.model,
            max_tokens=spec.max_tokens,
            temperature=spec.temperature,
            system=system,
            messages=[{"role": "user", "content": user_content}],
        )
    except APIStatusError as e:
        ended_at = utcnow()
        _write_transcript(transcript_path, system, user_content, None, error=str(e))
        return RunRecord(
            started_at=started_at,
            ended_at=ended_at,
            terminal_status="api_error",
            error_reason=f"{type(e).__name__}: {e}",
            **record_kwargs,
        )
    except APIError as e:
        ended_at = utcnow()
        _write_transcript(transcript_path, system, user_content, None, error=str(e))
        return RunRecord(
            started_at=started_at,
            ended_at=ended_at,
            terminal_status="api_error",
            error_reason=f"{type(e).__name__}: {e}",
            **record_kwargs,
        )

    ended_at = utcnow()

    text_blocks = [b.text for b in response.content if getattr(b, "type", None) == "text"]
    full_text = "\n".join(text_blocks)
    code = _extract_code(full_text)
    if code is not None:
        (artifacts_dir / "solution.py").write_text(code, encoding="utf-8")

    request_id = getattr(response, "_request_id", None) or getattr(response, "id", None)
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    stop_reason = response.stop_reason
    terminal: str
    if stop_reason in ("end_turn", "stop_sequence"):
        terminal = "ok" if code is not None else "tool_error"
    elif stop_reason == "max_tokens":
        terminal = "max_tokens"
    else:
        terminal = "unknown"

    _write_transcript(transcript_path, system, user_content, full_text)

    return RunRecord(
        started_at=started_at,
        ended_at=ended_at,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost_usd=compute_cost_usd(spec.model, input_tokens, output_tokens),
        terminal_status=terminal,  # type: ignore[arg-type]
        api_request_id=request_id,
        error_reason=None if terminal == "ok" else f"stop_reason={stop_reason}, code_extracted={code is not None}",
        **record_kwargs,
    )


def _write_transcript(path: Path, system: str, user: str, assistant: str | None, error: str | None = None) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write(json.dumps({"role": "system", "content": system}) + "\n")
        f.write(json.dumps({"role": "user", "content": user}) + "\n")
        if assistant is not None:
            f.write(json.dumps({"role": "assistant", "content": assistant}) + "\n")
        if error is not None:
            f.write(json.dumps({"role": "error", "content": error}) + "\n")


def run_cycle(
    intent_text: str,
    prior_code: str,
    contract_files: list[Path],
    include_contracts: bool,
    experiment_id: str,
    arm_id: str,
    subject: str,
    seed: int,
    cycle_num: int,
    chain_id: str,
    model: str,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    client: Anthropic | None = None,
) -> RunRecord:
    run_id = uuid.uuid4().hex[:16]
    artifacts_dir = RUNS_DIR / experiment_id / arm_id / subject / f"chain_{chain_id}" / f"c{cycle_num}"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = artifacts_dir / "transcript.jsonl"

    system = SYSTEM_PROMPT_CYCLE
    user_content = _build_cycle_content(intent_text, prior_code, include_contracts, contract_files)
    prompt_hash = _prompt_hash([system, user_content, model, str(temperature)])

    started_at = utcnow()
    client = client or Anthropic(api_key=ANTHROPIC_API_KEY)

    record_kwargs = dict(
        run_id=run_id,
        task_id=f"{experiment_id}:{subject}:{arm_id}:{seed}:c{cycle_num}",
        subject=subject,
        experiment_id=experiment_id,
        arm_id=arm_id,
        seed=seed,
        model=model,
        transcript_path=transcript_path,
        artifacts_dir=artifacts_dir,
        prompt_hash=prompt_hash,
        lab_git_sha=lab_git_sha(),
        cycle_num=cycle_num,
        chain_id=chain_id,
    )

    try:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": user_content}],
        )
    except (APIStatusError, APIError) as e:
        ended_at = utcnow()
        _write_transcript(transcript_path, system, user_content, None, error=str(e))
        return RunRecord(
            started_at=started_at, ended_at=ended_at,
            terminal_status="api_error", error_reason=f"{type(e).__name__}: {e}",
            **record_kwargs,
        )

    ended_at = utcnow()
    text_blocks = [b.text for b in response.content if getattr(b, "type", None) == "text"]
    full_text = "\n".join(text_blocks)
    code = _extract_code(full_text)
    if code is not None:
        (artifacts_dir / "solution.py").write_text(code, encoding="utf-8")

    _write_transcript(transcript_path, system, user_content, full_text)

    stop_reason = response.stop_reason
    terminal = "ok" if (stop_reason in ("end_turn", "stop_sequence") and code is not None) else (
        "max_tokens" if stop_reason == "max_tokens" else "tool_error" if code is None else "unknown"
    )

    return RunRecord(
        started_at=started_at, ended_at=ended_at,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
        cost_usd=compute_cost_usd(model, response.usage.input_tokens, response.usage.output_tokens),
        terminal_status=terminal,
        api_request_id=getattr(response, "_request_id", None) or getattr(response, "id", None),
        error_reason=None if terminal == "ok" else f"stop_reason={stop_reason}",
        **record_kwargs,
    )


_MULTI_FENCE_RE = re.compile(r"```python:(\S+)\s*\n(.*?)```", re.DOTALL)


def _extract_multi_file_code(text: str) -> dict[str, str]:
    """Extract named fenced blocks: ```python:filename.py ... ``` → {filename: code}."""
    return {
        m.group(1): m.group(2).rstrip() + "\n"
        for m in _MULTI_FENCE_RE.finditer(text)
    }


def _build_multi_file_cycle_content(
    intent_text: str,
    prior_files: dict[str, str],
    include_contracts: bool,
    contract_files: list[Path],
) -> str:
    parts = ["# Current implementation\n\n"]
    for filename, code in sorted(prior_files.items()):
        parts.append(f"## {filename}\n\n```python\n{code.strip()}\n```\n\n")
    parts.append(f"# Feature request\n\n{intent_text.strip()}\n")
    parts.append(
        "\nReply with one fenced code block per file you modify or create, "
        "using the format ```python:<filename> ... ```. "
        "Include ALL files that changed. Do not omit unchanged files you reference.\n"
    )
    if include_contracts and contract_files:
        parts.append("\n# Acceptance contracts (pytest)\n")
        parts.append(
            "Your updated implementation must make every test below pass.\n\n"
        )
        for cf in contract_files:
            content = Path(cf).read_text(encoding="utf-8")
            parts.append(f"## {Path(cf).name}\n\n```python\n{content}\n```\n")
    return "".join(parts)


SYSTEM_PROMPT_MULTI_FILE_CYCLE = (
    "You are a Python implementer working on a multi-file project. "
    "You will be given the current implementation (multiple files) and a feature request. "
    "Reply with one fenced code block per file you need to create or modify, using the format "
    "```python:<filename> where <filename> is the exact filename (e.g. models.py). "
    "Include ALL changed files. Preserve all prior functionality. "
    "Do not include explanation outside the code blocks. "
    "Do not include __main__ guards. Do not print anything."
)


def run_multi_file_cycle(
    intent_text: str,
    prior_files: dict[str, str],
    contract_files: list[Path],
    include_contracts: bool,
    experiment_id: str,
    arm_id: str,
    subject: str,
    seed: int,
    cycle_num: int,
    chain_id: str,
    model: str,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    client: Anthropic | None = None,
) -> RunRecord:
    run_id = uuid.uuid4().hex[:16]
    artifacts_dir = RUNS_DIR / experiment_id / arm_id / subject / f"chain_{chain_id}" / f"c{cycle_num}"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = artifacts_dir / "transcript.jsonl"

    system = SYSTEM_PROMPT_MULTI_FILE_CYCLE
    user_content = _build_multi_file_cycle_content(intent_text, prior_files, include_contracts, contract_files)
    prompt_hash = _prompt_hash([system, user_content, model, str(temperature)])

    started_at = utcnow()
    client = client or Anthropic(api_key=ANTHROPIC_API_KEY)

    record_kwargs = dict(
        run_id=run_id,
        task_id=f"{experiment_id}:{subject}:{arm_id}:{seed}:c{cycle_num}",
        subject=subject,
        experiment_id=experiment_id,
        arm_id=arm_id,
        seed=seed,
        model=model,
        transcript_path=transcript_path,
        artifacts_dir=artifacts_dir,
        prompt_hash=prompt_hash,
        lab_git_sha=lab_git_sha(),
        cycle_num=cycle_num,
        chain_id=chain_id,
    )

    try:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": user_content}],
        )
    except (APIStatusError, APIError) as e:
        ended_at = utcnow()
        _write_transcript(transcript_path, system, user_content, None, error=str(e))
        return RunRecord(
            started_at=started_at, ended_at=ended_at,
            terminal_status="api_error", error_reason=f"{type(e).__name__}: {e}",
            **record_kwargs,
        )

    ended_at = utcnow()
    text_blocks = [b.text for b in response.content if getattr(b, "type", None) == "text"]
    full_text = "\n".join(text_blocks)
    extracted = _extract_multi_file_code(full_text)

    for filename, code in extracted.items():
        (artifacts_dir / filename).write_text(code, encoding="utf-8")

    _write_transcript(transcript_path, system, user_content, full_text)

    stop_reason = response.stop_reason
    terminal = "ok" if (stop_reason in ("end_turn", "stop_sequence") and extracted) else (
        "max_tokens" if stop_reason == "max_tokens" else "tool_error" if not extracted else "unknown"
    )

    return RunRecord(
        started_at=started_at, ended_at=ended_at,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
        cost_usd=compute_cost_usd(model, response.usage.input_tokens, response.usage.output_tokens),
        terminal_status=terminal,
        api_request_id=getattr(response, "_request_id", None) or getattr(response, "id", None),
        error_reason=None if terminal == "ok" else f"stop_reason={stop_reason}, files_extracted={list(extracted.keys())}",
        **record_kwargs,
    )


def stage_workspace(
    spec: TaskSpec,
    artifacts_dir: Path,
    include_contracts: bool,
) -> None:
    """Copy contract + extra files into artifacts dir. Used after run_task for membrane scoring."""
    if include_contracts:
        for cf in spec.contract_files:
            shutil.copy(cf, artifacts_dir / Path(cf).name)
    for ef in spec.extra_files:
        shutil.copy(ef, artifacts_dir / Path(ef).name)
