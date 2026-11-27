---
name: logic-auditor-local
description: Evidence-based universal multi-perspective audit skill (Local edition) for physical products, designs, code, AI skills, workflows, research, and documents, with local harness capability guidance and a deterministic Audit Record validator. Use in Codex, Claude Code, Antigravity, Cursor, OpenCode, or Hermes Agent for comprehensive audits, failure-mode analysis, or premortems.
---

# Logic Auditor V2 (Local Edition)

Universal audit skill combining the evidence-based shared core with local harness capability detection and deterministic Audit Record validation.

## Local Execution Flow
Follow the 13-stage pipeline in [orchestrator.md](references/orchestrator.md) with local environment controls:
1. **Passive Capability Detection:** check actual active tools in the session (real subagent tool, local file reading, read-only shell permission, artifact storage)—never infer capabilities from harness name alone. See [harnesses.md](references/harnesses.md) for Codex, Claude Code, Antigravity, Cursor, OpenCode, and Hermes Agent.
2. **Adaptive Pre-Audit (Max 3 Questions):** ask only unknown items (`quick`/`mid`/`deep` mode, auditor count `>= 2`, and focus/constraints).
3. **Evidence-Based Investigation & Cross-Check:** run `real_swarm` when isolated subagents are available and permitted, or `virtual_swarm` with honest disclosure when running single-agent. Stay read-only unless non-destructive tests are explicitly authorized.
4. **Deterministic Validation Before Final Report:** when file writes and read-only CLI execution are permitted, write the structured Audit Record JSON and validate it before presenting the User Report:
   ```bash
   python scripts/validate_audit.py <path-to-audit-record.json>
   ```
   Resolve every schema or invariant violation reported (e.g., `LA-03`, `LA-04`, `LA-05`, `BUDGET-01`) prior to final output.
5. **Adaptive User Report:** deliver a concise summary matching the user's language and register per [reporting.md](references/reporting.md).

## Core Reference Map (Progressive Disclosure)

| Module | Authoritative Scope | Read When |
| :--- | :--- | :--- |
| [contract.md](references/contract.md) | Rule precedence Levels 1–5, min-2 perspective invariant, dual-horizon, re-audit | Audit start & re-audits |
| [guardrails.md](references/guardrails.md) | Read-only default, privacy boundary, prompt-injection defense, anti-fabrication | All stages |
| [orchestrator.md](references/orchestrator.md) | 13-stage pipeline, Coverage Ledger, honest fallback, Stop Gate | Orchestration & closing |
| [modes.md](references/modes.md) | `quick` / `mid` / `deep` baselines, low-token option, no silent escalation | Setup & budget checks |
| [reasoning.md](references/reasoning.md) | 10 adaptive reasoning methods (anti-ritual) and discriminating tests | Lens & test design |
| [swarm.md](references/swarm.md) | Dynamic auditor profile, 6 hybrid personas, Real/Virtual/External Swarm, Moderator | Running perspectives |
| [evidence.md](references/evidence.md) | 19-key finding contract, status rules, P0–P3 calibration, anti-voting, deduplication | Aggregating & verifying |
| [reporting.md](references/reporting.md) | Audit Record vs concise User Report, language adaptation, re-audit formatting | Finalizing output |
| [harnesses.md](references/harnesses.md) | Actual tool-probe guidance for Codex, Claude Code, Antigravity, Cursor, OpenCode, Hermes | Session start in CLI/IDE |
