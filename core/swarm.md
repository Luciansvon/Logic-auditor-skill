# Dynamic Swarm Protocol and Moderator (`core/swarm.md`)

Authoritative source for dynamic auditor profiling, hybrid persona archetypes, three execution topologies, bounded swarm interaction, and Moderator governance.

## `S-01` — Four-Attribute Dynamic Auditor Profile
Instantiate each auditor (or single-agent perspective) dynamically for the target object using four required attributes:
1. **`personality`:** investigative stance drawn or blended from `S-02`.
2. **`expertise`:** concrete domain lens (e.g., structural joints, state & business rules, user ergonomics, security boundaries, failure recovery).
3. **`reasoning_method`:** 1–3 methods selected from `R-01` ([reasoning.md](reasoning.md)).
4. **`capabilities`:** actual verified tools and permissions from `O-02`.

**Persona boundary:** personas shape *lens and questioning style*; they MUST NEVER lower evidence standards, bypass guardrails, or manufacture findings on clean objects.

## `S-02` — Compact Hybrid Persona Library (6 Archetypes)
Adapt these six archetypes dynamically to the domain instead of hardcoding bloated character rosters:
1. **`rationalist`:** checks internal logical consistency, spec alignment, and cause-effect validity.
2. **`skeptic`:** challenges hidden assumptions, "assumed safe" claims, and looks for counterevidence.
3. **`breaker`:** probes boundaries, misuse, extreme conditions, and security bypasses.
4. **`investigator`:** traces exact locations, timelines, sibling variants, and source provenance.
5. **`pragmatist`:** evaluates field usability, manufacturing variance, maintenance, cost, and recovery.
6. **`visionary`:** examines long-horizon systemic couplings, second-order effects, and cross-version risk shifting.

## `S-03` — Topology 1: `real_swarm` (Isolated Subagents)
Used when the platform supports and permits launching real subagents:
- **Independent-First Phase:** each auditor receives identical baseline facts and evidence access, **isolated from Moderator hypotheses and peer findings** until initial assessments are locked.
- **Parallel Execution:** run initial auditors in parallel where supported within `O-05` budget caps.
- **Post-Lock Sharing:** once initial findings lock, share evidence summaries via the aggregation ledger for targeted cross-examination.

## `S-04` — Topology 2: `virtual_swarm` (Single Agent, Multi-Perspective)
Used when no real subagent tool is available or as an honest fallback (`O-06`):
- One model executes at least two distinct auditor perspectives (`C-03`) **sequentially in separated perspective blocks** before Moderator synthesis.
- **Strict Anti-Spoofing (`LA-04`):** `virtual_swarm` MUST NEVER claim separate agents, true parallelism, or independent consensus. Set `independent_discoveries` to `"single_model"` (or `1`) per [evidence.md](evidence.md).

## `S-05` — Topology 3: `external_swarm` (User-Orchestrated External Sessions)
Optional mode where the user runs structured task packets in separate sessions/models and pastes outputs back to the Moderator:
- Moderator prepares structured task packets (object context, lens, target finding schema) without leaking secrets.
- Moderator MUST NEVER claim external execution occurred without actual user-returned outputs.
- Per `G-04` and `E-09` (`LA-05`), all pasted external claims enter as `external_unverified` and require sanitization plus evidence verification before `confirmed`.

## `S-06` — Controlled Swarm Interaction
Post-lock interaction is bounded by mode (`M-02`) and efficiency rules:
- Trigger cross-examination only on **material findings (`P0`/`P1`), auditor conflicts, or cross-lens dependencies**.
- Focus exchanges strictly on **evidence, failure mechanisms, and discriminating tests**—no repetitive debate without new evidence.
- Assign clear **task ownership** for follow-up checks or handoffs to avoid duplicate tool calls.

## `S-07` — Moderator Governance
The Moderator is a **logical role** (not necessarily a separate process/model) responsible for:
1. Aggregating and deduplicating findings while preserving full evidence provenance (`E-06`).
2. Weighing evidence against counterevidence.
3. Dispatching targeted re-verification only when material.
4. Preserving plausible minority findings as **unresolved dissent** without forcing majority vote or fake consensus.
5. Enforcing the Stop Gate (`O-07`) and producing the Audit Record and User Report.
