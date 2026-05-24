"""Smoke test for membrane runner — runs a tiny suite against an inline solution."""
from pathlib import Path

from ahnlab.membrane import run_suite


def _write_solution(tmp: Path, body: str) -> Path:
    art = tmp / "art"
    art.mkdir()
    (art / "solution.py").write_text(body, encoding="utf-8")
    return art


def _write_suite(tmp: Path, body: str) -> Path:
    sf = tmp / "test_check.py"
    sf.write_text(body, encoding="utf-8")
    return sf


def test_all_pass(tmp_path: Path):
    art = _write_solution(tmp_path, "def f():\n    return 1\n")
    sf = _write_suite(tmp_path, "from solution import f\n\ndef test_one():\n    assert f() == 1\n")
    report = run_suite("rid", art, [sf], "contracts")
    assert report.passed == 1
    assert report.failed == 0


def test_failure_reported(tmp_path: Path):
    art = _write_solution(tmp_path, "def f():\n    return 2\n")
    sf = _write_suite(tmp_path, "from solution import f\n\ndef test_one():\n    assert f() == 1\n")
    report = run_suite("rid", art, [sf], "contracts")
    assert report.passed == 0
    assert report.failed == 1


def test_missing_solution_errors(tmp_path: Path):
    art = tmp_path / "art"
    art.mkdir()
    sf = _write_suite(tmp_path, "def test_x():\n    assert True\n")
    report = run_suite("rid", art, [sf], "contracts")
    assert report.errors >= 1
