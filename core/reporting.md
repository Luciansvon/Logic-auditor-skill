# Dual-Layer Reporting and Language Adaptation (`core/reporting.md`)

Authoritative source for separating the structured Audit Record from the concise User Report, hard brevity budgets, canonical JSON keys, language adaptation, and re-audit reporting.

## `P-01` — Layer 1: Structured Audit Record
Every audit maintains a structured Audit Record containing:
- Audit ID, `mode`, `execution_topology` (`real_swarm` | `virtual_swarm` | `external_swarm`), actual `auditor_count`, and platform constraints.
- Domain calibration (`C-05`), Coverage Ledger (`O-04`), and budget/stop status (`completed` | `partial` | `blocked`).
- Full findings array conforming to `E-01` ([evidence.md](evidence.md)).
- Moderator decisions and unresolved dissent list (`S-07`).
- Observed tool/resource usage (zero fabricated metrics per `G-05`) and `limitations`.

**Persistence rule:** save the Audit Record as an artifact/file **only if the platform supports and permits it**. Otherwise keep the structured record in-session and **never claim persistence without actual storage**.

## `P-02` — Layer 2: Concise Adaptive User Report
Default user output MUST be **concise, decision-focused, and easy to scan**. Running in `deep` mode is **never an excuse for a bloated report**.

Default report structure:
1. **Verdict & Configuration Disclosure (2 lines):** verdict scoped to actual coverage (`completed` / `partial` / `blocked`), stating mode, actual completed auditor/perspective count, and topology (`real_swarm` / `virtual_swarm` / `external_swarm`).
2. **Top Findings Table:** ranked highest-urgency first in one compact table (`ID & Tier/Status`, `Trigger -> Impact`, `Fact vs Untested`, `Action / Pass-Fail Test`).
3. **Prioritized Next Steps (3–4 tight bullets):** highest-leverage, lowest-cost action sequence.
4. **Unresolved Dissent & Material Limitations (2–4 tight bullets):** key disagreements, `not_checked` / `blocked` coverage items, and unexecuted physical/runtime tests.

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

## `P-07` — Hard Brevity Budget & Single-Table Layout
Enforce strict default User Report word caps:
- **`quick`:** **`<= 350` words** (max 4 top findings in 1 compact table + 3 next actions).
- **`mid`:** **`<= 550` words** (max 7 key findings in 1 compact table).
- **`deep`:** **`<= 750` words** (max 10 active findings in 1 compact table + compact rejected-hypothesis line).

Do NOT write repetitive multi-paragraph essays per finding; place all findings into the single compact Markdown table from `P-02`.

## `P-08` — Opt-In JSON Output & Canonical Top-Level Schema Keys
- **Do NOT print raw JSON Audit Records inline** in default user responses (especially in `quick` mode or Web chat) unless explicitly requested by the user or saved to a local artifact.
- Whenever a JSON Audit Record IS emitted or saved, it MUST use these **exact 13 top-level keys**:
  `schema_version`, `audit_id`, `mode`, `execution_topology`, `auditor_count`, `auditors`, `object`, `coverage_ledger`, `budget`, `findings`, `moderator`, `limitations`, `status`
- Never substitute alternative top-level names (such as `auditor_profiles`, `stop_status`, or nesting `status` solely inside `stop_gate`).
- Structural invariants:
  - `auditors`: array of `>= 2` objects, each with distinct `expertise` (or `lens`).
  - `budget`: object containing boolean `exhausted` (`true` requires top-level `status` to be `"partial"` or `"blocked"`, never `"completed"`).
  - `findings`: each item contains all 19 keys from `E-01`, locks `independent_discoveries` to `"single_model"` (or `1`) under `virtual_swarm` (`LA-04`), and includes an `evidence[]` entry with matching `auditor_id` for every ID in `source_auditors[]` (`E-06`).
