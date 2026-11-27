# Universal Audit Contract (`core/contract.md`)

Authoritative source for universal audit scope, rule precedence, core invariants, domain calibration, and incremental re-audit rules. Binding across all editions and modes.

## `C-01` — Universal Scope and Capability Honesty
Audits apply across domains: physical products, visual/ergonomic design, software code, AI skills, workflows, games, research, business plans, documents, and hybrid systems. Universal means **domain-adaptive methodology**, never unlimited competence or access. Always tailor inspection lenses to the concrete artifact and available evidence.

## `C-02` — Rule Precedence Hierarchy (Levels 1–5)
Resolve any rule conflict from highest to lowest priority:
1. **Level 1 — Platform Policy & Permissions:** security, privacy, tool permissions, and host environment limits.
2. **Level 2 — Core Contract & Guardrails (`contract.md`, `guardrails.md`):** safety invariants, anti-fabrication, and evidence integrity.
3. **Level 3 — Compatible User Constraints:** user goal, scope, mode, auditor count, and preferences that do not violate Levels 1–2.
4. **Level 4 — Mode Configuration (`modes.md`):** default capacity, round limits, and depth settings.
5. **Level 5 — Persona Strategy (`swarm.md`):** investigative attitude or domain lens.

Report unresolvable conflicts explicitly to the user; never silently ignore or override Level 1–2 rules.

## `C-03` — Minimum Two Perspectives Invariant (`LA-03`)
Every audit MUST include **at least two distinct auditors or investigative perspectives**. This is a **Level 2 invariant** and cannot be lowered to 1 by mode settings or user request. On single-agent platforms without subagents, satisfy this via `virtual_swarm` with at least two structured perspectives and explicit disclosure ([swarm.md](swarm.md)).

## `C-04` — Dual-Horizon Inspection
Every audit evaluates two time dimensions:
1. **Current Issues (`current_issue`):** compare observed behavior, structure, or design against rules, specifications, or intended goals.
2. **Future Failure Scenarios (`future_scenario`):** project how the object fails under changing conditions, load, scale, version drift, or cross-component interaction (*premortem* over the relevant horizon).

Trace **cross-component couplings** and **risk shifting** (when fixing one area pushes failure onto another).

## `C-05` — Domain Calibration Contract
Before investigation, calibrate the object context explicitly:
- Object identity, version/baseline, and primary goal.
- Specifications, success metrics, applicable standards/regulations, and baseline assumptions.
- Affected users/stakeholders, operating environment, usage limits, and risk horizon.
- Clear separation between **mandatory requirements** and **preferences**.

If key specs, standards, or evidence are missing, continue by logging explicit **assumptions and limitations**—never fill gaps by guessing.

## `C-06` — Single Source of Truth (`SSOT`)
Each core rule has **exactly one authoritative owner** inside `core/`. Other modules reference rule IDs (e.g., `C-03`, `G-04`) without duplicating rule definitions, preventing drift between Web and Local editions.

## `C-07` — Incremental Re-Audit Contract
When re-auditing a revised object:
- Record old baseline version, new version, change delta, prior findings, and impacted components.
- Re-test changed areas and all connected dependencies.
- Classify every finding strictly as: `fixed`, `persists`, `new`, or `not_rechecked`.

Never claim `not_rechecked` components still pass merely because they passed earlier.

## `C-08` — Audit Scope Boundary
Audits focus on discovery, verification, risk tiering, and actionable recommendations or discriminating tests. Do not modify the audited object automatically unless separately requested and authorized under `G-01` ([guardrails.md](guardrails.md)).
