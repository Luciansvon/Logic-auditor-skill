#!/usr/bin/env python3
"""Adversarial test suite for the Logic Auditor V2 deterministic validator."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURES = ROOT / "tests" / "fixtures"
VALIDATOR_PATH = ROOT / "logic-auditor-local" / "scripts" / "validate_audit.py"

SPEC = importlib.util.spec_from_file_location("validate_audit", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR_MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR_MOD)

REQUIRED_SCENARIO_CATEGORIES = {
    "known_defect",
    "clean_object",
    "ambiguous_case",
    "rule_conflict",
    "duplicate_findings",
    "wrong_majority",
    "prompt_injection",
    "tool_failure",
    "budget_exhaustion",
    "no_subagent_platform",
    "untested_physical_risk",
    "everyday_vs_technical_language",
    "object_revision_reaudit",
}


class AdversarialTests(unittest.TestCase):
    def run_validator_cli(self, fixture_name: str) -> tuple[int, dict]:
        proc = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), str(FIXTURES / fixture_name)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        payload = json.loads(proc.stdout)
        return proc.returncode, payload

    def test_valid_real_swarm_audit_passes(self) -> None:
        code, result = self.run_validator_cli("valid_real_swarm_audit.json")
        self.assertEqual(code, 0, msg=result)
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_valid_virtual_swarm_audit_passes(self) -> None:
        code, result = self.run_validator_cli("valid_virtual_swarm_audit.json")
        self.assertEqual(code, 0, msg=result)
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_virtual_swarm_independent_consensus_rejected_la04(self) -> None:
        code, result = self.run_validator_cli("invalid_virtual_consensus.json")
        self.assertEqual(code, 1)
        codes = {err["code"] for err in result["errors"]}
        self.assertIn("LA-04", codes)

    def test_single_auditor_rejected_la03(self) -> None:
        code, result = self.run_validator_cli("invalid_single_auditor.json")
        self.assertEqual(code, 1)
        codes = {err["code"] for err in result["errors"]}
        self.assertIn("LA-03", codes)

    def test_voting_severity_and_empty_evidence_rejected(self) -> None:
        code, result = self.run_validator_cli("invalid_voting_severity.json")
        self.assertEqual(code, 1)
        codes = {err["code"] for err in result["errors"]}
        self.assertIn("VOTING-01", codes)
        self.assertIn("EVIDENCE-01", codes)

    def test_budget_exhausted_completed_rejected(self) -> None:
        code, result = self.run_validator_cli("invalid_budget_exhausted_pass.json")
        self.assertEqual(code, 1)
        codes = {err["code"] for err in result["errors"]}
        self.assertIn("BUDGET-01", codes)
        self.assertIn("COVERAGE-01", codes)

    def test_external_injection_rejected_la05(self) -> None:
        code, result = self.run_validator_cli("adversarial_external_injection.json")
        self.assertEqual(code, 1)
        codes = {err["code"] for err in result["errors"]}
        self.assertIn("LA-05", codes)

    def test_untested_physical_claim_cannot_be_confirmed(self) -> None:
        base = json.loads((FIXTURES / "valid_real_swarm_audit.json").read_text(encoding="utf-8"))
        mutated = copy.deepcopy(base)
        mutated["findings"][1]["status"] = "confirmed"
        mutated["findings"][1]["test_domain"] = "physical"
        result = VALIDATOR_MOD.validate_record(mutated)
        self.assertFalse(result["valid"])
        self.assertIn("EVIDENCE-01", {e["code"] for e in result["errors"]})

    def test_rejected_finding_requires_rationale(self) -> None:
        base = json.loads((FIXTURES / "valid_virtual_swarm_audit.json").read_text(encoding="utf-8"))
        mutated = copy.deepcopy(base)
        mutated["findings"][0]["status"] = "rejected"
        mutated["findings"][0]["counterevidence"] = []
        mutated["findings"][0]["limitations"] = []
        result = VALIDATOR_MOD.validate_record(mutated)
        self.assertFalse(result["valid"])
        self.assertIn("EVIDENCE-01", {e["code"] for e in result["errors"]})

    def test_adversarial_scenarios_catalog_covers_all_13_cases(self) -> None:
        catalog = json.loads((FIXTURES / "adversarial_scenarios.json").read_text(encoding="utf-8"))
        scenarios = catalog.get("scenarios", [])
        categories = {item["category"] for item in scenarios}
        self.assertEqual(categories, REQUIRED_SCENARIO_CATEGORIES)


if __name__ == "__main__":
    unittest.main()
