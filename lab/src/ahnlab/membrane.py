"""R2 Membrane Runner — execute pytest contracts against an artifacts dir."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from .models import ContractResult, MembraneReport


def run_suite(
    run_id: str,
    artifacts_dir: Path,
    suite_files: list[Path],
    suite_label: str,
    per_test_timeout_s: float = 10.0,
) -> MembraneReport:
    """Copy suite files alongside solution.py and run pytest with json-report.

    suite_label is "contracts" (Arm B's contracts) or "hidden" (judge suite).
    """
    started = time.time()

    if not (artifacts_dir / "solution.py").exists():
        # No solution emitted — every test is an error.
        results = [
            ContractResult(name=str(sf), status="error", duration_s=0.0, message="missing solution.py")
            for sf in suite_files
        ]
        return MembraneReport(
            run_id=run_id, suite_label=suite_label, results=results,
            total=len(results), passed=0, failed=0, errors=len(results),
            timeouts=0, duration_s=time.time() - started,
        )

    with tempfile.TemporaryDirectory() as tmpd:
        tmp = Path(tmpd)
        shutil.copy(artifacts_dir / "solution.py", tmp / "solution.py")
        copied_suite_files = []
        for sf in suite_files:
            dest = tmp / Path(sf).name
            shutil.copy(sf, dest)
            copied_suite_files.append(str(dest))
        report_path = tmp / "_report.json"

        cmd = [
            sys.executable, "-m", "pytest",
            "--json-report", f"--json-report-file={report_path}",
            "-q", "--no-header", "--tb=short",
        ] + copied_suite_files
        try:
            subprocess.run(
                cmd, cwd=tmp, capture_output=True, text=True,
                timeout=per_test_timeout_s * max(len(suite_files), 1) * 5,
            )
        except subprocess.TimeoutExpired:
            return MembraneReport(
                run_id=run_id, suite_label=suite_label, results=[
                    ContractResult(name="<suite>", status="timeout", duration_s=time.time() - started,
                                   message="suite exceeded budget")
                ],
                total=1, passed=0, failed=0, errors=0, timeouts=1,
                duration_s=time.time() - started,
            )

        if not report_path.exists():
            return MembraneReport(
                run_id=run_id, suite_label=suite_label, results=[
                    ContractResult(name="<suite>", status="error", duration_s=0.0,
                                   message="pytest did not produce json report (collection failure)")
                ],
                total=1, passed=0, failed=0, errors=1, timeouts=0,
                duration_s=time.time() - started,
            )

        data = json.loads(report_path.read_text(encoding="utf-8"))

    results: list[ContractResult] = []
    for t in data.get("tests", []):
        outcome = t.get("outcome", "error")
        status_map = {"passed": "passed", "failed": "failed", "skipped": "skipped", "error": "error"}
        status = status_map.get(outcome, "error")
        msg = None
        if status in {"failed", "error"}:
            call = t.get("call") or {}
            msg = (call.get("longrepr") or t.get("longrepr") or "")[:500]
        results.append(ContractResult(
            name=t.get("nodeid", "<unknown>"),
            status=status,  # type: ignore[arg-type]
            duration_s=float(t.get("duration", 0.0)),
            message=msg,
        ))

    # Account for collection errors with no tests reported.
    collectors = data.get("collectors", [])
    for c in collectors:
        if c.get("outcome") == "failed":
            results.append(ContractResult(
                name=c.get("nodeid", "<collect>"), status="error",
                duration_s=0.0, message=str(c.get("longrepr", ""))[:500],
            ))

    if not results:
        results.append(ContractResult(name="<no-tests>", status="error", duration_s=0.0, message="no tests collected"))

    return MembraneReport(
        run_id=run_id, suite_label=suite_label, results=results,
        total=len(results),
        passed=sum(1 for r in results if r.status == "passed"),
        failed=sum(1 for r in results if r.status == "failed"),
        errors=sum(1 for r in results if r.status == "error"),
        timeouts=sum(1 for r in results if r.status == "timeout"),
        duration_s=time.time() - started,
    )
