#!/usr/bin/env python3
"""Deterministic contract, guardrail, and scenario-coverage benchmark runner."""

from __future__ import annotations

import argparse
import importlib.util
import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURES_DIR = ROOT / "tests" / "fixtures"
GROUND_TRUTH_PATH = ROOT / "tests" / "benchmark" / "ground_truth.json"
SCENARIOS_PATH = FIXTURES_DIR / "adversarial_scenarios.json"
VALIDATOR_PATH = ROOT / "logic-auditor-local" / "scripts" / "validate_audit.py"
REPORT_PATH = ROOT / "tests" / "benchmark" / "BENCHMARK_REPORT.md"

SPEC = importlib.util.spec_from_file_location("validate_audit", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR_MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR_MOD)

FIXTURE_EXPECTATIONS: list[tuple[str, bool, set[str]]] = [
    ("valid_real_swarm_audit.json", True, set()),
    ("valid_virtual_swarm_audit.json", True, set()),
    ("invalid_virtual_consensus.json", False, {"LA-04"}),
    ("invalid_single_auditor.json", False, {"LA-03"}),
    ("invalid_voting_severity.json", False, {"VOTING-01", "EVIDENCE-01"}),
    ("invalid_budget_exhausted_pass.json", False, {"BUDGET-01", "COVERAGE-01"}),
    ("adversarial_external_injection.json", False, {"LA-05"}),
]


def execute_pass() -> dict[str, Any]:
    start = time.perf_counter()

    gt = json.loads(GROUND_TRUTH_PATH.read_text(encoding="utf-8"))
    scn = json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))
    gt_categories = {item["category"] for item in gt.get("scenarios", [])}
    scn_categories = {item["category"] for item in scn.get("scenarios", [])}

    fixture_results: list[dict[str, Any]] = []
    passed_expectations = 0
    for fname, expected_valid, expected_codes in FIXTURE_EXPECTATIONS:
        payload = json.loads((FIXTURES_DIR / fname).read_text(encoding="utf-8"))
        res = VALIDATOR_MOD.validate_record(payload)
        actual_codes = {e["code"] for e in res["errors"]}
        matched = (res["valid"] == expected_valid) and expected_codes.issubset(actual_codes)
        if matched:
            passed_expectations += 1
        fixture_results.append(
            {
                "fixture": fname,
                "expected_valid": expected_valid,
                "actual_valid": res["valid"],
                "expected_codes": sorted(expected_codes),
                "actual_codes": sorted(actual_codes),
                "matched": matched,
            }
        )

    elapsed_ms = (time.perf_counter() - start) * 1000.0
    return {
        "ground_truth_count": len(gt.get("scenarios", [])),
        "scenario_parity": gt_categories == scn_categories,
        "fixtures_total": len(FIXTURE_EXPECTATIONS),
        "fixtures_matched": passed_expectations,
        "fixture_results": fixture_results,
        "duration_ms": elapsed_ms,
    }


def run_benchmark(repeats: int = 3, write_report: bool = True) -> dict[str, Any]:
    passes = [execute_pass() for _ in range(repeats)]
    durations = [p["duration_ms"] for p in passes]
    last = passes[-1]

    all_matched = all(p["fixtures_matched"] == p["fixtures_total"] and p["scenario_parity"] for p in passes)
    summary = {
        "repeats": repeats,
        "all_checks_passed": all_matched,
        "ground_truth_scenarios": last["ground_truth_count"],
        "scenario_parity": last["scenario_parity"],
        "fixtures_matched": last["fixtures_matched"],
        "fixtures_total": last["fixtures_total"],
        "detection_rate": round(last["fixtures_matched"] / last["fixtures_total"], 4),
        "duration_ms_mean": round(statistics.mean(durations), 3),
        "duration_ms_stdev": round(statistics.stdev(durations) if len(durations) > 1 else 0.0, 3),
        "fixture_results": last["fixture_results"],
    }

    if write_report:
        lines = [
            "# Deterministic Contract & Guardrail Benchmark Report",
            "",
            "> **Scope Disclosure:** This report records actual deterministic validator and ground-truth fixture measurements across repeated runs. Live comparative LLM candidate runs (`A_baseline_plain_ai` through `E_real_swarm`) are supported by [score_benchmark.py](score_benchmark.py) and have not yet been executed against live model APIs.",
            "",
            "## Summary Metrics (3 Repeated Runs)",
            "",
            "| Metric | Measured Value |",
            "| :--- | :--- |",
            f"| Ground-truth scenarios covered | {summary['ground_truth_scenarios']} / 13 (`scenario_parity={summary['scenario_parity']}`) |",
            f"| Contract & guardrail fixture accuracy | {summary['fixtures_matched']} / {summary['fixtures_total']} ({summary['detection_rate'] * 100:.1f}%) |",
            f"| Mean pass latency | {summary['duration_ms_mean']} ms (stdev: {summary['duration_ms_stdev']} ms) |",
            "| Token / API cost | `null` (deterministic local run; not fabricated) |",
            "",
            "## Fixture-Level Results",
            "",
            "| Fixture | Expected Valid | Actual Valid | Expected Error Codes | Actual Error Codes | Match |",
            "| :--- | :---: | :---: | :--- | :--- | :---: |",
        ]
        for row in summary["fixture_results"]:
            exp_c = ", ".join(row["expected_codes"]) or "none"
            act_c = ", ".join(row["actual_codes"]) or "none"
            mark = "PASS" if row["matched"] else "FAIL"
            lines.append(f"| `{row['fixture']}` | {row['expected_valid']} | {row['actual_valid']} | `{exp_c}` | `{act_c}` | **{mark}** |")

        lines.append("")
        REPORT_PATH.write_bytes(("\n".join(lines)).encode("utf-8"))

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic contract benchmark for Logic Auditor V2.")
    parser.add_argument("--repeats", type=int, default=3, help="Number of repeated deterministic passes.")
    parser.add_argument("--check-only", action="store_true", help="Run checks without rewriting BENCHMARK_REPORT.md.")
    args = parser.parse_args()

    summary = run_benchmark(repeats=args.repeats, write_report=not args.check_only)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
