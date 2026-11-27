# Pipeline Orchestrator, Capability Detection, and Budgets (`core/orchestrator.md`)

Authoritative source for the 13-stage audit pipeline, passive capability detection, adaptive pre-audit, Coverage Ledger, budget control, and Stop Gate.

## `O-01` — 13-Stage Audit Pipeline
Execute every audit in this sequence, with [guardrails.md](guardrails.md) active throughout:
1. **Passive Capability Detection** — read-only probe of actual session tools **before** asking questions (`LA-02`).
2. **Adaptive Pre-Audit** — at most 3 targeted questions tailored to actual platform capabilities.
3. **Permission, Scope & Budget Gate** — confirm access limits, consent for material fallbacks, and resource caps.
4. **Domain Calibration** — map object, assumptions, standards, and baseline (`C-05`).
5. **Coverage Planning** — initialize the Coverage Ledger.
6. **Dynamic Auditor Generation** — assign profiles and reasoning methods per lens (`S-01`, `R-02`).
7. **Independent Investigation** — collect isolated initial findings per swarm topology (`S-03`–`S-05`).
8. **Finding Aggregation** — deduplicate without losing evidence provenance (`E-06`).
9. **Controlled Swarm Interaction** — bounded cross-examination only where material and budgeted (`S-06`).
10. **Evidence Verification** — re-check material claims (`E-07`).
11. **Moderator & Stop Gate** — finalize verdicts, preserve dissent, and close coverage.
12. **Audit Record** — structure findings and provenance (`P-01`).
13. **Adaptive User Report** — deliver concise decision-ready output (`P-02`).

**Quick Fast-Path (`quick` mode):** skip Stage 9 (0 cross-check rounds), keep Stage 12 lightweight in-session (no inline JSON dump unless requested under `P-08`), and execute directly from `SKILL.md` without opening all reference modules (`M-02`).

## `O-02` — Tool-Verified Passive Capability Detection (`LA-02`)
Probe **actual tools and permissions available in the active session**, never assume from platform name alone:
- Are real subagents with isolated context and parallel execution available and permitted?
- Is local file/repo reading available, or only user-supplied chat text/attachments?
- Are non-destructive execution/test tools available and permitted?
- Is structured artifact/file persistence available?

Feed this probe directly into `O-03` so pre-audit options match reality on the first pass.

## `O-03` — Adaptive Pre-Audit (Max 3 Questions)
Ask **only what is not yet known** from the user's prompt, up to 3 questions:
1. **Audit mode:** `quick`, `mid`, or `deep` (note `deep` low-token option in [modes.md](modes.md)).
2. **Auditor/perspective count:** must satisfy minimum `2` (`C-03`); note Moderator is counted separately as a logical role.
3. **Priority focus, object, goal, and constraints:** adapted to the target domain.

Pre-audit efficiency rules:
- If all three are already clear, **summarize the configuration briefly and start immediately without re-asking**.
- If platform limits prevent the user's requested setup (e.g., parallel subagents on a single-agent Web platform), explain the fallback (`virtual_swarm` or `external_swarm`) and ask consent whenever the change is material.

## `O-04` — Coverage Ledger
Track every key component or aspect in the Coverage Ledger:
- `component`: part, flow, or aspect under review.
- `priority`: `critical | high | medium | low`.
- `owner`: assigned auditor/lens.
- `status`: `not_checked | partial | completed | blocked`.
- `evidence_refs`: supporting references or reason when `partial`/`blocked`.

Never claim comprehensive coverage while high-priority items remain `not_checked` or `blocked`.

## `O-05` — Budget Control & Verification Reserve
- Cap reference reads, interaction rounds, subagent/tool calls, and report word counts per [modes.md](modes.md) and platform limits.
- Reading unrequested reference modules beyond mode caps or printing unrequested raw JSON blocks violates budget discipline.
- Always reserve budget and context for **evidence verification** and **report finalization**.
- Never add auditors, expand scope, or escalate mode silently (`M-05`).

## `O-06` — Honest Fallback on Subagent Failure
If real subagent execution fails or hits capacity:
1. Retry once with smaller context or sequential execution.
2. If fewer than 2 real subagents return initial assessments, continue with useful lenses and disclose the exact completed subagent count plus uncovered lenses.
3. If a single agent executes everything, declare topology `virtual_swarm` ("single-agent, multi-perspective audit") and enforce `LA-04`.

## `O-07` — Stop Gate
Close the audit cleanly when either condition holds:
1. **Complete (`completed`):** required coverage for the active mode is `completed`, material findings (`P0`/`P1`) are verified within access limits, and extra rounds add no material value.
2. **Resource/Access Exhausted (`partial` or `blocked`):** budget, quota, time, or permissions run out before required coverage finishes.

When exhausted, **emit a partial report** listing checked areas, remaining unchecked scope, and the blocking limit. Never mark exhausted runs `completed` or "passed". There is **no minimum finding quota**; clean objects report clean within checked coverage.

## `O-08` — Decision Traceability
Record Moderator reasons for stopping early, scoping down, or rejecting findings inside the Audit Record (`P-01`).
