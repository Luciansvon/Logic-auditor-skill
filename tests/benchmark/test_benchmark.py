#!/usr/bin/env python3
"""Unit tests for the Stage 5 benchmark ground truth, scorer, and deterministic runner."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
BENCH_DIR = ROOT / "tests" / "benchmark"
FIXTURES_DIR = ROOT / "tests" / "fixtures"

sys.path.insert(0, str(BENCH_DIR))
import score_benchmark  # noqa: E402


class BenchmarkTests(unittest.TestCase):
    def test_ground_truth_covers_13_scenarios(self) -> None:
        gt = json.loads((BENCH_DIR / "ground_truth.json").read_text(encoding="utf-8"))
        self.assertEqual(len(gt["scenarios"]), 13)
        self.assertEqual(len(gt["candidates"]), 5)

    def test_scorer_math_and_no_metric_fabrication(self) -> None:
        gt = json.loads((BENCH_DIR / "ground_truth.json").read_text(encoding="utf-8"))
        valid_rec = json.loads((FIXTURES_DIR / "valid_real_swarm_audit.json").read_text(encoding="utf-8"))
        run_1 = {
            "candidate_id": "E_real_swarm",
            "run_id": "r1",
            "duration_ms": 120.0,
            "scenario_outputs": [
                {
                    "scenario_id": "SCN-01",
                    "audit_record": valid_rec,
                    "predicted_defect_ids": ["DEF-HEEL-01"],
                    "predicted_severities": {"DEF-HEEL-01": "P0"},
                    "summary_fidelity_pass": True,
                },
                {
                    "scenario_id": "SCN-02",
                    "audit_record": valid_rec,
                    "predicted_defect_ids": ["FALSE-POS-1"],
                    "predicted_severities": {"FALSE-POS-1": "P2"},
                    "summary_fidelity_pass": True,
                },
            ],
        }
        s1 = score_benchmark.score_single_run(gt, run_1)
        self.assertEqual(s1["true_positives"], 1)
        self.assertEqual(s1["false_positives"], 1)
        self.assertEqual(s1["precision"], 0.5)
        self.assertIsNone(s1["tokens"])
        self.assertIsNone(s1["cost_usd"])

        agg = score_benchmark.aggregate_runs([s1, {**s1, "run_id": "r2", "duration_ms": 140.0}])
        self.assertEqual(agg["run_count"], 2)
        self.assertEqual(agg["metrics"]["precision"]["mean"], 0.5)
        self.assertEqual(agg["metrics"]["duration_ms"]["mean"], 130.0)
        self.assertIsNone(agg["metrics"]["tokens"])
        self.assertIsNone(agg["metrics"]["cost_usd"])

    def test_deterministic_benchmark_check_only_passes(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(BENCH_DIR / "run_deterministic_benchmark.py"), "--check-only"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=f"Benchmark failed:\n{proc.stdout}\n{proc.stderr}")
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["all_checks_passed"])
        self.assertEqual(payload["detection_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
