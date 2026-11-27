#!/usr/bin/env python3
"""Deterministic Audit Record validator for Logic Auditor V2 (Local Edition).

Uses Python 3 standard library only (zero external dependencies) and operates
strictly read-only on the target JSON file.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL_KEYS = (
    "schema_version",
    "audit_id",
    "mode",
    "execution_topology",
    "auditor_count",
    "auditors",
    "object",
    "coverage_ledger",
    "budget",
    "findings",
    "moderator",
    "limitations",
    "status",
)

REQUIRED_FINDING_FIELDS = (
    "id",
    "object_version",
    "location",
    "finding_type",
    "claim",
    "impact",
    "likelihood",
    "severity",
    "provisional",
    "confidence",
    "evidence",
    "verification_method",
    "observed_result",
    "status",
    "source_auditors",
    "independent_discoveries",
    "counterevidence",
    "recommendation",
    "limitations",
)

VALID_MODES = {"quick", "mid", "deep"}
VALID_TOPOLOGIES = {"real_swarm", "virtual_swarm", "external_swarm"}
VALID_AUDIT_STATUSES = {"completed", "partial", "blocked"}
VALID_FINDING_TYPES = {"current_issue", "future_scenario"}
VALID_SEVERITIES = {"P0", "P1", "P2", "P3"}
VALID_CONFIDENCE = {"low", "medium", "high"}
VALID_FINDING_STATUSES = {"confirmed", "indication", "needs_validation", "rejected"}
VALID_COVERAGE_STATUSES = {"not_checked", "partial", "completed", "blocked"}

INJECTION_PATTERNS = (
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
    re.compile(r"override\s+(the\s+)?(guardrail|contract|rules?)", re.IGNORECASE),
    re.compile(r"(set|downgrade|change)\s+severity\s+to\s+P[0-3]", re.IGNORECASE),
    re.compile(r"skip\s+verification", re.IGNORECASE),
    re.compile(r"abaikan\s+instruksi\s+sebelumnya", re.IGNORECASE),
    re.compile(r"lewati\s+verifikasi", re.IGNORECASE),
)


def add_error(errors: list[dict[str, str]], code: str, message: str, path: str = "") -> None:
    entry = {"code": code, "message": message}
    if path:
        entry["path"] = path
    errors.append(entry)


def add_warning(warnings: list[dict[str, str]], code: str, message: str, path: str = "") -> None:
    entry = {"code": code, "message": message}
    if path:
        entry["path"] = path
    warnings.append(entry)


def collect_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(collect_strings(item))
        return out
    if isinstance(value, dict):
        out = []
        for v in value.values():
            out.extend(collect_strings(v))
        return out
    return []


def validate_record(data: Any) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    if not isinstance(data, dict):
        add_error(errors, "SCHEMA-01", "Audit Record must be a JSON object.", "$")
        return {"valid": False, "errors": errors, "warnings": warnings}

    for key in REQUIRED_TOP_LEVEL_KEYS:
        if key not in data:
            add_error(errors, "SCHEMA-02", f"Missing required top-level field: '{key}'.", f"$.{key}")

    mode = data.get("mode")
    if mode is not None and mode not in VALID_MODES:
        add_error(errors, "SCHEMA-03", f"Invalid mode value: {mode!r}.", "$.mode")

    topology = data.get("execution_topology")
    if topology is not None and topology not in VALID_TOPOLOGIES:
        add_error(errors, "SCHEMA-04", f"Invalid execution_topology value: {topology!r}.", "$.execution_topology")

    audit_status = data.get("status")
    if audit_status is not None and audit_status not in VALID_AUDIT_STATUSES:
        add_error(errors, "SCHEMA-05", f"Invalid audit status value: {audit_status!r}.", "$.status")

    # LA-03: Minimum 2 distinct auditors/perspectives invariant.
    auditor_count = data.get("auditor_count")
    auditors = data.get("auditors")
    if not isinstance(auditor_count, int) or auditor_count < 2:
        add_error(errors, "LA-03", "Minimum 2 auditors/perspectives invariant violated in auditor_count.", "$.auditor_count")

    if not isinstance(auditors, list) or len(auditors) < 2:
        add_error(errors, "LA-03", "The auditors array must contain at least 2 auditors/perspectives.", "$.auditors")
    else:
        lenses: set[str] = set()
        for idx, auditor in enumerate(auditors):
            if not isinstance(auditor, dict):
                add_error(errors, "SCHEMA-06", "Each auditor entry must be an object.", f"$.auditors[{idx}]")
                continue
            lens_val = str(auditor.get("expertise") or auditor.get("lens") or auditor.get("role") or "").strip().lower()
            if lens_val:
                lenses.add(lens_val)
        if len(lenses) < 2:
            add_error(errors, "LA-03", "At least 2 auditors must have distinct lenses/expertise.", "$.auditors")

    # BUDGET-01: Exhausted budget cannot have status 'completed'.
    budget = data.get("budget")
    if isinstance(budget, dict):
        if budget.get("exhausted") is True and audit_status == "completed":
            add_error(
                errors,
                "BUDGET-01",
                "Exhausted budget (budget.exhausted=true) must report status 'partial' or 'blocked', never 'completed'.",
                "$.status",
            )
    elif budget is not None:
        add_error(errors, "SCHEMA-07", "Field budget must be an object.", "$.budget")

    # COVERAGE-01: Unchecked or blocked coverage items must be disclosed in limitations.
    coverage = data.get("coverage_ledger")
    limitations = data.get("limitations")
    has_incomplete_coverage = False
    if isinstance(coverage, list):
        for idx, item in enumerate(coverage):
            if not isinstance(item, dict):
                add_error(errors, "SCHEMA-08", "Each coverage_ledger entry must be an object.", f"$.coverage_ledger[{idx}]")
                continue
            cov_status = item.get("status")
            if cov_status not in VALID_COVERAGE_STATUSES:
                add_error(errors, "SCHEMA-09", f"Invalid coverage status: {cov_status!r}.", f"$.coverage_ledger[{idx}].status")
            if cov_status in {"not_checked", "blocked"}:
                has_incomplete_coverage = True
    elif coverage is not None:
        add_error(errors, "SCHEMA-10", "Field coverage_ledger must be an array.", "$.coverage_ledger")

    if has_incomplete_coverage and (not isinstance(limitations, list) or len(limitations) == 0):
        add_error(
            errors,
            "COVERAGE-01",
            "Coverage includes 'not_checked' or 'blocked' items without explanation in limitations.",
            "$.limitations",
        )

    if has_incomplete_coverage and audit_status == "completed":
        add_warning(
            warnings,
            "COVERAGE-WARN",
            "Status is 'completed' while some coverage items remain unchecked/blocked; verify those items are non-mandatory.",
            "$.status",
        )

    # Validate each finding (LA-04, LA-05, LA-09, EVIDENCE-01, VOTING-01).
    findings = data.get("findings")
    if not isinstance(findings, list):
        add_error(errors, "SCHEMA-11", "Field findings must be an array.", "$.findings")
        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}

    for idx, finding in enumerate(findings):
        fpath = f"$.findings[{idx}]"
        if not isinstance(finding, dict):
            add_error(errors, "SCHEMA-12", "Each finding must be an object.", fpath)
            continue

        for req in REQUIRED_FINDING_FIELDS:
            if req not in finding:
                add_error(errors, "LA-09", f"Missing required finding contract field: '{req}'.", f"{fpath}.{req}")

        ftype = finding.get("finding_type")
        if ftype is not None and ftype not in VALID_FINDING_TYPES:
            add_error(errors, "LA-09", f"Invalid finding_type: {ftype!r}.", f"{fpath}.finding_type")

        severity = finding.get("severity")
        if severity is not None and severity not in VALID_SEVERITIES:
            add_error(errors, "LA-09", f"Invalid severity: {severity!r}.", f"{fpath}.severity")

        if "provisional" in finding and not isinstance(finding.get("provisional"), bool):
            add_error(errors, "LA-09", "Field provisional must be a boolean.", f"{fpath}.provisional")

        confidence = finding.get("confidence")
        if confidence is not None and confidence not in VALID_CONFIDENCE:
            add_error(errors, "LA-09", f"Invalid confidence: {confidence!r}.", f"{fpath}.confidence")

        fstatus = finding.get("status")
        if fstatus is not None and fstatus not in VALID_FINDING_STATUSES:
            add_error(errors, "LA-09", f"Invalid finding status: {fstatus!r}.", f"{fpath}.status")

        # VOTING-01: Never escalate or assign severity by majority vote.
        if finding.get("severity_basis") == "majority_vote":
            add_error(
                errors,
                "VOTING-01",
                "Severity must never be assigned or escalated based on majority vote.",
                f"{fpath}.severity_basis",
            )

        # LA-04: Lock independent_discoveries under Virtual Swarm.
        ind_disc = finding.get("independent_discoveries")
        if topology == "virtual_swarm":
            valid_virtual_disc = (ind_disc == "single_model") or (
                isinstance(ind_disc, int) and not isinstance(ind_disc, bool) and ind_disc == 1
            )
            if not valid_virtual_disc:
                add_error(
                    errors,
                    "LA-04",
                    "Under virtual_swarm, independent_discoveries must be 'single_model' or 1 (independent consensus claims forbidden).",
                    f"{fpath}.independent_discoveries",
                )

        evidence = finding.get("evidence")
        source_auditors = finding.get("source_auditors")
        ver_method = finding.get("verification_method")
        counterevidence = finding.get("counterevidence")
        f_limitations = finding.get("limitations")

        # EVIDENCE-01: Evidence integrity per status.
        if not isinstance(evidence, list):
            add_error(errors, "EVIDENCE-01", "Field evidence must be an array.", f"{fpath}.evidence")
            evidence_list: list[dict[str, Any]] = []
        else:
            evidence_list = [e for e in evidence if isinstance(e, dict)]
            if len(evidence_list) != len(evidence):
                add_error(errors, "EVIDENCE-01", "Every evidence item must be an object.", f"{fpath}.evidence")

        if fstatus == "confirmed":
            if len(evidence_list) == 0:
                add_error(errors, "EVIDENCE-01", "A 'confirmed' finding requires at least one evidence entry.", f"{fpath}.evidence")
            for e_idx, ev in enumerate(evidence_list):
                if not str(ev.get("source", "")).strip() or not str(ev.get("observation", "")).strip():
                    add_error(
                        errors,
                        "EVIDENCE-01",
                        "Each evidence entry on a 'confirmed' finding requires non-empty 'source' and 'observation'.",
                        f"{fpath}.evidence[{e_idx}]",
                    )

            test_domain = str(finding.get("test_domain", "")).strip().lower()
            is_untested = str(ver_method or "").strip().lower() == "not_tested"
            static_only = finding.get("static_contradiction_only") is True
            if is_untested and (test_domain in {"physical", "runtime"} or not static_only):
                add_error(
                    errors,
                    "EVIDENCE-01",
                    "Physical or runtime claims with verification_method='not_tested' cannot be marked 'confirmed'.",
                    f"{fpath}.status",
                )

        if fstatus == "rejected":
            has_counter = isinstance(counterevidence, list) and len(counterevidence) > 0
            has_lim = isinstance(f_limitations, list) and len(f_limitations) > 0
            if not (has_counter or has_lim):
                add_error(
                    errors,
                    "EVIDENCE-01",
                    "A 'rejected' finding requires rationale in counterevidence or limitations.",
                    f"{fpath}.status",
                )

        # Merged duplicates must preserve every reporting auditor's provenance.
        if isinstance(source_auditors, list) and len(source_auditors) > 1:
            ev_auditors = {str(ev.get("auditor_id", "")).strip() for ev in evidence_list if ev.get("auditor_id")}
            missing_prov = [a for a in source_auditors if str(a).strip() not in ev_auditors]
            if missing_prov:
                add_error(
                    errors,
                    "EVIDENCE-01",
                    f"Merged findings must preserve auditor_id provenance in evidence[] (missing: {missing_prov}).",
                    f"{fpath}.evidence",
                )

        # LA-05: External Swarm provenance and prompt-injection quarantine.
        source_origin = str(finding.get("source_origin", "")).strip().lower()
        is_external = source_origin == "external" or (topology == "external_swarm" and source_origin != "local")
        if is_external:
            provenances = {str(ev.get("provenance", "")).strip() for ev in evidence_list}
            moderator_verified = finding.get("moderator_verified") is True
            if not moderator_verified and "external_unverified" not in provenances:
                add_error(
                    errors,
                    "LA-05",
                    "Unverified external_swarm claims must carry provenance='external_unverified' in evidence[].",
                    f"{fpath}.evidence",
                )
            if fstatus == "confirmed" and not moderator_verified:
                add_error(
                    errors,
                    "LA-05",
                    "External claims cannot be marked 'confirmed' without moderator_verified=true.",
                    f"{fpath}.status",
                )

        if finding.get("injection_quarantined") is not True:
            text_blobs = (
                collect_strings(finding.get("claim"))
                + collect_strings(finding.get("impact"))
                + collect_strings(finding.get("recommendation"))
                + collect_strings(finding.get("evidence"))
                + collect_strings(finding.get("limitations"))
            )
            for blob in text_blobs:
                for pattern in INJECTION_PATTERNS:
                    if pattern.search(blob):
                        add_error(
                            errors,
                            "LA-05",
                            f"Detected unquarantined prompt-injection pattern (injection_quarantined!=true): '{pattern.pattern}'.",
                            fpath,
                        )
                        break

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic Audit Record validator for Logic Auditor V2.")
    parser.add_argument("audit_record", help="Path to the Audit Record JSON file to validate.")
    args = parser.parse_args()

    target = Path(args.audit_record)
    if not target.is_file():
        output = {
            "valid": False,
            "errors": [{"code": "IO-01", "message": f"File not found: {target}"}],
            "warnings": [],
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return 1

    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        output = {
            "valid": False,
            "errors": [{"code": "JSON-01", "message": f"Invalid JSON: {exc}"}],
            "warnings": [],
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return 1

    result = validate_record(payload)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
