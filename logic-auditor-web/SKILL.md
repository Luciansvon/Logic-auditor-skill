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

## Quick Fast-Path (0–1 Reference Reads)
When `mode = quick`, **DO NOT read all 8 reference files**. Execute directly from these embedded rules:
1. **Passive Probe:** check active tools silently; if no real subagent tool exists, run as `virtual_swarm` with `>= 2` distinct perspectives and lock `independent_discoveries` to `"single_model"`.
2. **Pre-Audit (Max 3 Questions):** ask only unknown items (mode, auditor count `>= 2`, focus/constraints); if clear, summarize config in 1 line and start immediately.
3. **Fast Investigation (1 Pass, 0 Cross-Check Rounds):** evaluate both current defects and future failure scenarios across 2–3 distinct lenses; strictly separate direct observed facts from untested assumptions (`not_tested`).
4. **Compact Report (`<= 350` words):** reply in the user's language and register with 2-line Verdict+Disclosure, **1 compact table** (max 4 top findings: `ID & Tier/Status`, `Trigger -> Impact`, `Fact vs Untested`, `Action / Pass-Fail Test`), 3 tight next actions, and 2-line limitations. **Do NOT print JSON unless explicitly requested.**

## Mode Read & Brevity Budget
- **`quick`:** read **0–1 files** (open `guardrails.md` or `contract.md` ONLY for prompt injection, rule conflicts, or re-audits) · **0** cross-check rounds · **`<= 350` words** · no inline JSON unless asked.
- **`mid`:** read **max 3 files** ([orchestrator.md](references/orchestrator.md), [evidence.md](references/evidence.md), [reporting.md](references/reporting.md)) · **1** targeted round (`P0`/`P1`) · **`<= 550` words** · no inline JSON unless asked.
- **`deep`:** read selectively per active stage · up to **2** targeted rounds + falsification · **`<= 750` words** · no inline JSON unless asked.

## Core Reference Map (Progressive Disclosure)
Read only what the active mode budget permits:

| Module | Authoritative Scope | Read When |
| :--- | :--- | :--- |
| [contract.md](references/contract.md) | Rule precedence Levels 1–5, min-2 perspective invariant, dual-horizon, re-audit | `deep` / rule conflict / re-audit |
| [guardrails.md](references/guardrails.md) | Read-only default, prompt-injection defense, External Swarm sanitization, anti-fabrication | `deep` / untrusted external input |
| [orchestrator.md](references/orchestrator.md) | 13-stage pipeline, Coverage Ledger, honest fallback, Stop Gate | `mid` / `deep` |
| [modes.md](references/modes.md) | `quick` / `mid` / `deep` caps, low-token option, no silent escalation | `deep` / budget questions |
| [reasoning.md](references/reasoning.md) | 10 adaptive reasoning methods (anti-ritual) and discriminating test design | `deep` / complex domain |
| [swarm.md](references/swarm.md) | Dynamic auditor profile, 6 hybrid personas, Real/Virtual/External Swarm, Moderator | `deep` / multi-agent swarm |
| [evidence.md](references/evidence.md) | 19-key finding contract, status rules, P0–P3 calibration, anti-voting, deduplication | `mid` / `deep` |
| [reporting.md](references/reporting.md) | Brevity word caps (`P-07`), canonical 13-key JSON (`P-08`), language adaptation | `mid` / `deep` / JSON requested |
