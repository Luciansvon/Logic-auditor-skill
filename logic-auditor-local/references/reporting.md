# Dual-Layer Reporting and Language Adaptation (`core/reporting.md`)

Authoritative source for separating the structured Audit Record from the concise User Report, language register adaptation, and re-audit reporting.

## `P-01` — Layer 1: Structured Audit Record
Every audit produces a structured Audit Record containing:
- Audit ID, `mode`, `execution_topology` (`real_swarm` | `virtual_swarm` | `external_swarm`), actual `auditor_count`, and platform constraints.
- Domain calibration (`C-05`), Coverage Ledger (`O-04`), and budget/stop status (`completed` | `partial` | `blocked`).
- Full findings array conforming to `E-01` ([evidence.md](evidence.md)).
- Moderator decisions and unresolved dissent list (`S-07`).
- Observed tool/resource usage (zero fabricated metrics per `G-05`) and `limitations`.

**Persistence rule:** save the Audit Record as an artifact/file **only if the platform supports and permits it**. Otherwise keep the structured record in-session and **never claim persistence without actual storage**.

## `P-02` — Layer 2: Concise Adaptive User Report
Default user output MUST be **concise, decision-focused, and easy to scan**. Running in `deep` mode is **never an excuse for a bloated report**.

Default report structure:
1. **Verdict & Configuration Disclosure:** concise verdict scoped to actual coverage (`completed` / `partial` / `blocked`), stating mode, actual completed auditor/perspective count, and topology (`real_swarm` / `virtual_swarm` / `external_swarm`).
2. **Top Urgent Findings:** ranked highest-urgency first, showing:
   - `Tier & Status` (e.g., `P0 · Confirmed` or `P1 Provisional · Needs Validation`)
   - `Trigger -> Mechanism -> Impact` (include horizon/trigger condition for `future_scenario`)
   - `Evidence or Assumption` (fact vs inference clearly separated)
   - `Action / Discriminating Test` (include checkable **pass/fail criteria** for top actions)
3. **Prioritized Next Steps:** highest-leverage, lowest-cost action sequence.
4. **Unresolved Dissent & Material Limitations:** key disagreements, `not_checked` / `blocked` coverage items, and unexecuted physical/runtime tests.

## `P-03` — No Raw Swarm Dump
- Never dump raw multi-agent transcripts, lengthy internal reasoning, or low-value trivia into the default User Report.
- Never omit **critical material risks (`P0`/`P1`)** or **material limitations** for brevity.
- Provide full details or full Audit Record export only on user request or via an actually saved artifact.

## `P-04` — Language & Register Adaptation
Deliver the User Report in **the user's own language** and adapt tone/depth to one of three registers:
- **`everyday`:** plain language with concrete real-world analogies and practical impact, avoiding unexplained jargon.
- **`professional`:** decision-oriented product, operational, cost, timeline, and user-impact framing.
- **`technical`:** exact locations, state flows, technical specs, and measurable test criteria.

**Note:** casual chat phrasing does not automatically mean a novice user—judge domain fluency from the prompt's technical content and object details.

## `P-05` — Re-Audit Reporting Format
For incremental re-audits (`C-07`), summarize baseline comparison clearly:
- Old vs new object version and inspected delta.
- Explicit grouping into **`fixed`**, **`persists`**, **`new`**, and **`not_rechecked`**.
- Explicit statement that `not_rechecked` areas are not re-verified as safe.

## `P-06` — Record-to-Report Fidelity
Every count, severity tier, provisional flag, completed auditor count, and evidence status in the User Report MUST match the Audit Record 100%. Never soften risks or inflate confidence in summary prose.
