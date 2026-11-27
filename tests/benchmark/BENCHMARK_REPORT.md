# Deterministic Contract & Guardrail Benchmark Report

> **Scope Disclosure:** This report records actual deterministic validator and ground-truth fixture measurements across repeated runs. Live comparative LLM candidate runs (`A_baseline_plain_ai` through `E_real_swarm`) are supported by [score_benchmark.py](score_benchmark.py) and have not yet been executed against live model APIs.

## Summary Metrics (3 Repeated Runs)

| Metric | Measured Value |
| :--- | :--- |
| Ground-truth scenarios covered | 13 / 13 (`scenario_parity=True`) |
| Contract & guardrail fixture accuracy | 7 / 7 (100.0%) |
| Mean pass latency | 3.716 ms (stdev: 0.05 ms) |
| Token / API cost | `null` (deterministic local run; not fabricated) |

## Fixture-Level Results

| Fixture | Expected Valid | Actual Valid | Expected Error Codes | Actual Error Codes | Match |
| :--- | :---: | :---: | :--- | :--- | :---: |
| `valid_real_swarm_audit.json` | True | True | `none` | `none` | **PASS** |
| `valid_virtual_swarm_audit.json` | True | True | `none` | `none` | **PASS** |
| `invalid_virtual_consensus.json` | False | False | `LA-04` | `LA-04` | **PASS** |
| `invalid_single_auditor.json` | False | False | `LA-03` | `LA-03` | **PASS** |
| `invalid_voting_severity.json` | False | False | `EVIDENCE-01, VOTING-01` | `EVIDENCE-01, VOTING-01` | **PASS** |
| `invalid_budget_exhausted_pass.json` | False | False | `BUDGET-01, COVERAGE-01` | `BUDGET-01, COVERAGE-01` | **PASS** |
| `adversarial_external_injection.json` | False | False | `LA-05` | `LA-05` | **PASS** |
