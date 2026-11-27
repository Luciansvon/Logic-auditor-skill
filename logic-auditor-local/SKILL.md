---
name: logic-auditor-local
description: Evidence-based universal multi-perspective audit skill (Local edition) for physical products, designs, code, AI skills, workflows, research, and documents, with local harness capability guidance and a deterministic Audit Record validator. Use in Codex, Claude Code, Antigravity, Cursor, OpenCode, or Hermes Agent for comprehensive audits, failure-mode analysis, or premortems.
---

# Logic Auditor V2 (Local Edition)

Universal audit skill combining the evidence-based shared core with local harness capability detection and deterministic Audit Record validation.

## Quick Fast-Path (0–1 Reference Reads)
When `mode = quick`, **DO NOT read all 8 reference files**. Execute directly from these embedded rules:
1. **Passive Probe:** inspect actual active tools (real subagents, local file reads, read-only shell); never infer from harness name alone. Use `virtual_swarm` if single-agent and lock `independent_discoveries` to `"single_model"`.
2. **Pre-Audit (Max 3 Questions):** ask only unknown items (mode, auditor count `>= 2`, focus/constraints); if clear, summarize config in 1 line and start immediately.
3. **Fast Investigation (1 Pass, 0 Cross-Check Rounds):** inspect current defects and future failure scenarios across 2–3 distinct lenses; stay read-only and separate observed facts from `not_tested` assumptions.
4. **Compact Report (`<= 350` words):** reply in the user's language and register with 2-line Verdict+Disclosure, **1 compact table** (max 4 top findings: `ID & Tier/Status`, `Trigger -> Impact`, `Fact vs Untested`, `Action / Pass-Fail Test`), 3 tight next actions, and 2-line limitations. **Skip JSON generation/validation unless explicitly requested.**

## Mode Read, Validation & Brevity Budget
- **`quick`:** read **0–1 files** (open `guardrails.md` or `contract.md` ONLY for prompt injection, rule conflicts, or re-audits) · **0** cross-check rounds · **`<= 350` words** · skip JSON unless asked.
- **`mid`:** read **max 3 core files** ([orchestrator.md](references/orchestrator.md), [evidence.md](references/evidence.md), [reporting.md](references/reporting.md)) + [harnesses.md](references/harnesses.md) if tool probing is unclear · **1** targeted round (`P0`/`P1`) · **`<= 550` words**.
- **`deep`:** read selectively per active stage · up to **2** targeted rounds + falsification · **`<= 750` words**.
- **Deterministic Validation (`mid` / `deep`, or when JSON is requested):** emit canonical 13-key JSON per `P-08` in [reporting.md](references/reporting.md) (`schema_version`, `audit_id`, `mode`, `execution_topology`, `auditor_count`, `auditors`, `object`, `coverage_ledger`, `budget`, `findings`, `moderator`, `limitations`, `status`, plus matching `evidence[].auditor_id` for every `source_auditors[]`), save if file writes are permitted, and validate before presenting the final report:
  ```bash
  python scripts/validate_audit.py <path-to-audit-record.json>
  ```

## Core Reference Map (Progressive Disclosure)
Read only what the active mode budget permits:

| Module | Authoritative Scope | Read When |
| :--- | :--- | :--- |
| [contract.md](references/contract.md) | Rule precedence Levels 1–5, min-2 perspective invariant, dual-horizon, re-audit | `deep` / rule conflict / re-audit |
| [guardrails.md](references/guardrails.md) | Read-only default, privacy boundary, prompt-injection defense, anti-fabrication | `deep` / untrusted external input |
| [orchestrator.md](references/orchestrator.md) | 13-stage pipeline, Coverage Ledger, honest fallback, Stop Gate | `mid` / `deep` |
| [modes.md](references/modes.md) | `quick` / `mid` / `deep` caps, low-token option, no silent escalation | `deep` / budget questions |
| [reasoning.md](references/reasoning.md) | 10 adaptive reasoning methods (anti-ritual) and discriminating tests | `deep` / complex domain |
| [swarm.md](references/swarm.md) | Dynamic auditor profile, 6 hybrid personas, Real/Virtual/External Swarm, Moderator | `deep` / multi-agent swarm |
| [evidence.md](references/evidence.md) | 19-key finding contract, status rules, P0–P3 calibration, anti-voting, deduplication | `mid` / `deep` |
| [reporting.md](references/reporting.md) | Brevity word caps (`P-07`), canonical 13-key JSON (`P-08`), language adaptation | `mid` / `deep` / JSON requested |
| [harnesses.md](references/harnesses.md) | Actual tool-probe guidance for Codex, Claude Code, Antigravity, Cursor, OpenCode, Hermes | When local harness tools need probing |
