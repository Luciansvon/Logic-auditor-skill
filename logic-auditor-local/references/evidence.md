# Evidence Contract, Severity, and Aggregation (`core/evidence.md`)

Authoritative source for the structured finding schema, verification statuses, Severity vs Confidence calibration, deduplication, and anti-voting rules.

## `E-01` — Structured Finding Contract (`id` + 18 Content Fields, `LA-09`)
Every finding in the Audit Record MUST contain all of the following fields:
1. `id`: unique finding identifier (e.g., `F-001`).
2. `object_version`: audited baseline/version identifier.
3. `location`: specific target location (file/line, physical part, workflow step, or design element).
4. `finding_type`: time orientation (`current_issue` | `future_scenario`) per `C-04`.
5. `claim`: concise **`trigger -> mechanism -> impact`** chain.
6. `impact`: concrete or potential consequence if triggered.
7. `likelihood`: exposure frequency or probability (qualitative tier or `unknown`).
8. `severity`: risk tier (`P0` | `P1` | `P2` | `P3`).
9. `provisional`: boolean (`true` | `false`); `true` when missing decisive facts could shift the tier, with tier-shift conditions noted in `limitations`.
10. `confidence`: evidence strength (`low` | `medium` | `high`).
11. `evidence`: array of traceable evidence items (`source`, `observation`, `method`, `conditions`, `result`, `auditor_id`, and `provenance` such as `direct_observation` | `static_analysis` | `runtime_test` | `external_unverified`).
12. `verification_method`: check executed or `not_tested`.
13. `observed_result`: actual observed outcome (or explicit statement that verification was not run).
14. `status`: verification status (`confirmed` | `indication` | `needs_validation` | `rejected`).
15. `source_auditors`: list of reporting/supporting auditor IDs.
16. `independent_discoveries`: count of genuinely independent initial discoveries under `real_swarm`, or locked to `"single_model"` / `1` under `virtual_swarm` (`LA-04`).
17. `counterevidence`: array of refuting evidence, exceptions, or rejection rationale.
18. `recommendation`: fix or discriminating test, including **checkable pass/fail criteria** and any **risk-shifting** warning.
19. `limitations`: evidence gaps, assumptions, and tier-change triggers.

## `E-02` — Verification Status Rules (`status`)
- **`confirmed`:** direct evidence is sufficient to prove the specific claim.
  - Clear static contradictions prove specification/code contradiction, **not runtime or physical field impact** unless executed.
  - Physical or runtime claims with `verification_method: "not_tested"` MUST NOT be marked `confirmed`.
- **`indication`:** current signal observed on the object, but the full causal mechanism is not yet verified.
- **`needs_validation`:** plausible hypothesis or `future_scenario` lacking decisive evidence or discriminating test execution.
- **`rejected`:** refuted by counterevidence or misread; requires explicit rationale in `counterevidence` or `limitations`, never mere absence of search.

## `E-03` — Severity Calibration (`P0`–`P3`) and Provisional Tiers
Assess severity from impact magnitude, exposure likelihood/frequency, and decision urgency:
- **`P0` (Critical):** severe, hard-to-reverse impact (safety hazard, core function loss, fatal security/data damage) with strong evidence of occurrence or urgent exposure path.
- **`P1` (High):** major impact with a plausible path, or severe conditional scenario with near-term exposure.
- **`P2` (Medium):** bounded, recoverable disruption or low-exposure backed flaw; define triggers that escalate priority.
- **`P3` (Low):** minor or cosmetic issue easily addressed when relevant.

Tier discipline:
- **Never pad empty severity tiers** just to make a report look balanced.
- If `likelihood` is `unknown`, state its effect on tiering and set `provisional: true` when missing facts could shift the tier.

## `E-04` — Severity vs Confidence Separation
Severity (how bad if it happens) and Confidence (how strong current proof is) answer different questions:
- A `P0` risk with `confidence: "low"` still requires urgent verification or exposure containment—never downgrade it silently to `P3`.
- A minor defect with `confidence: "high"` remains `P3`.

## `E-05` — Anti-Voting & Virtual Swarm Lock (`LA-04`)
- **Evidence beats consensus.**
- Never raise `severity` solely because multiple auditors flagged the same issue (`severity_basis` must never be `majority_vote`). Only stronger impact or likelihood evidence changes severity.
- Multiple auditors citing the **exact same evidence slice** count as **one evidence base**.
- Under `virtual_swarm`, `independent_discoveries` MUST stay `"single_model"` (or `1`). Confidence in `virtual_swarm` rises only via new evidence or executed checks, never perspective count.

## `E-06` — Duplicate Aggregation
- Merge findings ONLY when they share the **same root cause, location/object, and failure mechanism**.
- **Never merge** distinct root causes just because surface symptoms look alike.
- When merging, **preserve every auditor's `evidence[]` entries and `auditor_id` provenance** inside `source_auditors[]` and `evidence[]`.
- Distinguish pre-debate independent discovery from post-debate agreement.

## `E-07` — Material Verification Priority
- Prioritize `P0` and `P1` findings for challenge or re-verification when tools and budget allow; otherwise mark `needs_validation` and flag as unverified.
- Escalate and test critical `P0`/`P1` findings raised by a **single minority auditor**; never discard them by headcount.

## `E-08` — Fact, Inference, and Hypothesis Separation
Every `evidence[]` entry must make clear whether it represents **direct observed fact**, **logical inference**, or **untested hypothesis**.

## `E-09` — External Swarm Provenance (`LA-05`)
Claims originating from `external_swarm` MUST carry `provenance: "external_unverified"` initially and cannot rise to `confirmed` or `indication` until Moderator verification attaches direct traceable evidence.
