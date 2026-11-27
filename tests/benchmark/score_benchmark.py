#!/usr/bin/env python3
"""Reproducible multi-run benchmark scorer for Logic Auditor V2.

Scores candidate run JSON outputs against tests/benchmark/ground_truth.json
using Python 3 standard library only. Never fabricates token or cost metrics.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import statistics
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
VALIDATOR_PATH = ROOT / "logic-auditor-local" / "scripts" / "validate_audit.py"

SPEC = importlib.util.spec_from_file_location("validate_audit", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR_MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR_MOD)


def safe_div(num: float, den: float, default: float = 0.0) -> float:
    return num / den if den > 0 else default


def score_single_run(ground_truth: dict[str, Any], run_payload: dict[str, Any]) -> dict[str, Any]:
    gt_map = {item["id"]: item for item in ground_truth.get("scenarios", [])}
    outputs = {item["scenario_id"]: item for item in run_payload.get("scenario_outputs", [])}

    tp = 0
    fp = 0
    fn = 0
    sev_matches = 0
    sev_total = 0

    total_findings = 0
    evidence_valid_findings = 0
    guardrail_passes = 0
    coverage_passes = 0
    summary_passes = 0
    evaluated_scenarios = 0

    for scn_id, gt in gt_map.items():
        out = outputs.get(scn_id)
        if out is None:
            fn += len(gt.get("expected_defect_ids", []))
            continue

        evaluated_scenarios += 1
        expected_ids = set(gt.get("expected_defect_ids", []))
        predicted_ids = set(out.get("predicted_defect_ids", []))

        matched = expected_ids & predicted_ids
        tp += len(matched)
        fp += len(predicted_ids - expected_ids)
        fn += len(expected_ids - predicted_ids)

        expected_sevs = gt.get("expected_severities", {})
        predicted_sevs = out.get("predicted_severities", {})
        for defect_id in matched:
            sev_total += 1
            if predicted_sevs.get(defect_id) == expected_sevs.get(defect_id):
                sev_matches += 1

        audit_record = out.get("audit_record")
        if audit_record is not None:
            val_res = VALIDATOR_MOD.validate_record(audit_record)
            err_codes = {e["code"] for e in val_res["errors"]}
            if val_res["valid"]:
                guardrail_passes += 1
            if "COVERAGE-01" not in err_codes and "BUDGET-01" not in err_codes:
                coverage_passes += 1

            findings = audit_record.get("findings", [])
            if isinstance(findings, list):
                finding_bad_indices: set[int] = set()
                for err in val_res["errors"]:
                    path = err.get("path", "")
                    if path.startswith("$.findings[") and err["code"] in {"EVIDENCE-01", "LA-09"}:
                        idx_str = path.split("$.findings[", 1)[1].split("]", 1)[0]
                        if idx_str.isdigit():
                            finding_bad_indices.add(int(idx_str))
                for idx in range(len(findings)):
                    total_findings += 1
                    if idx not in finding_bad_indices:
                        evidence_valid_findings += 1

        if out.get("summary_fidelity_pass") is True:
            summary_passes += 1

    precision = safe_div(tp, tp + fp, default=1.0 if fn == 0 else 0.0)
    recall = safe_div(tp, tp + fn, default=1.0 if fp == 0 else 0.0)
    f1 = safe_div(2 * precision * recall, precision + recall, default=0.0)

    severity_cal = safe_div(sev_matches, sev_total, default=1.0 if fp == 0 and fn == 0 else 0.0)
    evidence_rate = safe_div(evidence_valid_findings, total_findings, default=1.0 if evaluated_scenarios > 0 else 0.0)
    coverage_rate = safe_div(coverage_passes, evaluated_scenarios, default=0.0)
    guardrail_rate = safe_div(guardrail_passes, evaluated_scenarios, default=0.0)
    summary_rate = safe_div(summary_passes, evaluated_scenarios, default=0.0)

    return {
        "candidate_id": run_payload.get("candidate_id", "unknown"),
        "run_id": run_payload.get("run_id", "unknown"),
        "evaluated_scenarios": evaluated_scenarios,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "severity_calibration_accuracy": round(severity_cal, 4),
        "evidence_quality_rate": round(evidence_rate, 4),
        "coverage_compliance_rate": round(coverage_rate, 4),
        "guardrail_pass_rate": round(guardrail_rate, 4),
        "summary_fidelity_pass_rate": round(summary_rate, 4),
        "duration_ms": run_payload.get("duration_ms"),
        "tokens": run_payload.get("tokens"),
        "cost_usd": run_payload.get("cost_usd"),
    }


def aggregate_runs(scored_runs: list[dict[str, Any]]) -> dict[str, Any]:
    if not scored_runs:
        raise ValueError("scored_runs must not be empty")

    metric_keys = (
        "precision",
        "recall",
        "f1",
        "false_positives",
        "severity_calibration_accuracy",
        "evidence_quality_rate",
        "coverage_compliance_rate",
        "guardrail_pass_rate",
        "summary_fidelity_pass_rate",
        "duration_ms",
        "tokens",
        "cost_usd",
    )

    summary: dict[str, dict[str, float] | None] = {}
    for key in metric_keys:
        vals = [run[key] for run in scored_runs if isinstance(run.get(key), (int, float))]
        if len(vals) != len(scored_runs) or not vals:
            summary[key] = None
            continue
        mean_val = statistics.mean(vals)
        stdev_val = statistics.stdev(vals) if len(vals) > 1 else 0.0
        summary[key] = {
            "mean": round(mean_val, 4),
            "stdev": round(stdev_val, 4),
        }

    return {
        "candidate_id": scored_runs[0].get("candidate_id", "unknown"),
        "run_count": len(scored_runs),
        "metrics": summary,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score Logic Auditor V2 benchmark runs.")
    parser.add_argument("--ground-truth", required=True, help="Path to ground_truth.json")
    parser.add_argument("--runs", nargs="+", required=True, help="One or more candidate run JSON files")
    args = parser.parse_args()

    gt = json.loads(Path(args.ground_truth).read_text(encoding="utf-8"))
    scored = [score_single_run(gt, json.loads(Path(p).read_text(encoding="utf-8"))) for p in args.runs]
    output = {
        "runs": scored,
        "aggregate": aggregate_runs(scored),
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
