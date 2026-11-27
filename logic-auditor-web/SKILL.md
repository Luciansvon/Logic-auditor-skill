---
name: logic-auditor-web
description: Evidence-based universal multi-perspective audit skill (pure Markdown Web edition) for physical products, designs, code, AI skills, workflows, research, and documents. Detects current defects and future failure scenarios in Quick, Mid, or Deep mode with zero bundled scripts. Use for comprehensive audits, blind-spot detection, failure-mode analysis, or premortems on Web platforms.
---

# Logic Auditor V2 (Web Edition)

Modular, token-efficient, evidence-based universal audit skill packaged purely in Markdown for Web environments.

## Web Edition Boundaries
- Bundles **zero custom scripts, executables, or external dependencies**.
- Uses **only native platform tools and permissions** actually available and authorized in the active session.
- If the platform lacks real subagents, execute as `virtual_swarm` (or `external_swarm` if the user runs separate sessions) and disclose the topology honestly.

## Execution Flow
Follow the 13-stage pipeline in [orchestrator.md](references/orchestrator.md):
1. **Passive Capability Detection:** probe available session capabilities silently (subagent support, file reading, native tools, or chat-only input) before asking questions.
2. **Adaptive Pre-Audit (Max 3 Questions):** ask only what is still unknown:
   - Mode: `quick`, `mid`, or `deep` (note `deep` low-token option with 2–3 perspectives).
   - Auditor/perspective count (minimum `2`; Moderator is counted separately).
   - Focus, target object, goal, and priority constraints.
   If all three are already clear, summarize the configuration briefly and start immediately.
3. **Permission & Budget Gate -> Domain Calibration -> Coverage Ledger:** lock limits and map components before probing.
4. **Independent Investigation -> Aggregation -> Targeted Cross-Check -> Moderator & Stop Gate:** enforce strict evidence standards and emit a partial audit if budgets exhaust.
5. **Audit Record & User Report:** deliver a concise report in the user's language and register, without raw transcript dumps or hidden critical risks.

## Core Reference Map (Progressive Disclosure)
Read only the reference module needed for the active stage:

| Module | Authoritative Scope | Read When |
| :--- | :--- | :--- |
| [contract.md](references/contract.md) | Rule precedence Levels 1–5, min-2 perspective invariant, dual-horizon, re-audit | Audit start & re-audits |
| [guardrails.md](references/guardrails.md) | Read-only default, prompt-injection defense, External Swarm sanitization, anti-fabrication | All stages |
| [orchestrator.md](references/orchestrator.md) | 13-stage pipeline, Coverage Ledger, honest fallback, Stop Gate | Orchestration & closing |
| [modes.md](references/modes.md) | `quick` / `mid` / `deep` baselines, low-token option, no silent escalation | Setup & budget checks |
| [reasoning.md](references/reasoning.md) | 10 adaptive reasoning methods (anti-ritual) and discriminating test design | Lens & test design |
| [swarm.md](references/swarm.md) | Dynamic auditor profile, 6 hybrid personas, Real/Virtual/External Swarm, Moderator | Running perspectives |
| [evidence.md](references/evidence.md) | 19-key finding contract, status rules, P0–P3 calibration, anti-voting, deduplication | Aggregating & verifying |
| [reporting.md](references/reporting.md) | Audit Record vs concise User Report, language adaptation, re-audit formatting | Finalizing output |
