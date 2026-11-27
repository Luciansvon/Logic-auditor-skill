# Audit Mode Configuration (`core/modes.md`)

Authoritative source (Level 4 under `C-02`) for `quick`, `mid`, and `deep` mode defaults. Do not duplicate guardrails, reasoning methods, or evidence rules here.

## `M-01` — Mode vs Auditor Count Separation
- **Mode (`quick` | `mid` | `deep`)** controls reference-read budget, analytical depth, coverage breadth, interaction round caps, report word limits, and verification intensity.
- **Auditor/perspective count** is a separate user choice, always bounded below by the Level 2 invariant `>= 2` (`C-03`).
- Numeric ranges below are **calibration defaults**, not rigid mandates overriding explicit user choices.

## `M-02` — Mode Matrix (Latency, Depth & Brevity Calibration)

| Dimension | `quick` (Fast-Path) | `mid` (Balanced) | `deep` (Comprehensive) |
| :--- | :--- | :--- | :--- |
| **Primary goal** | Rapid screen for urgent risks and obvious flaws | Balanced cross-component audit and targeted cross-checks | Exhaustive audit including cross-layer interactions |
| **Reference read cap** | **0–1 files** (run from `SKILL.md` Quick Fast-Path; do NOT read all 8 references) | **Max 3 files** (`orchestrator.md`, `evidence.md`, `reporting.md`) | Selective reads per active stage |
| **Recommended auditors** | 2–3 perspectives | 4–6 perspectives | 7–12 perspectives *(low-token option: 2–3 perspectives)* |
| **Initial investigation** | 1 fast-pass | 1 independent round | 1 independent round |
| **Interaction / challenge rounds** | **0 rounds** (direct Moderator synthesis) | **1 targeted round** (`P0`/`P1` only) | **Up to 2 targeted rounds** + false-hypothesis falsification |
| **Report findings cap** | **Max 4 top findings** | **Max 7 key findings** | **Max 10 active findings** (+ rejected list) |
| **User Report word cap (`P-07`)** | **<= 350 words** (1 compact table + 3 actions) | **<= 550 words** | **<= 750 words** |
| **Audit Record JSON (`P-08`)** | **Omitted by default** (opt-in only) | Save to file locally; **opt-in only** inline on Web | Save & validate locally; **opt-in only** inline on Web |
| **Coverage Ledger scope** | Core high-risk components | All primary flows & key dependencies | Full scope + edge, stress, and recovery paths |
| **Verification intensity** | Check `P0`/`P1` if directly accessible; log untested items as `needs_validation` | Challenge/re-check `P0`/`P1`; sample `P2` within budget | Maximum verification on `P0`/`P1`; cross-check `P2` within budget |

*Calibration note: these default caps enforce real latency and length separation across modes.*

## `M-03` — Low-Token `deep` Option
Users may explicitly choose **`deep` with 2–3 auditors** for thorough coverage and strict verification without high multi-agent token cost. Depth is achieved via systematic coverage partitioning and strict verification, not headcount.

## `M-04` — Low-Severity Verification Policy (`P2` / `P3`)
- `P0` and `P1` findings always take priority over verification reserves (`O-05`).
- `P2` and `P3` findings MUST NOT starve `P0`/`P1` verification. When budget is tight, record unverified `P2`/`P3` items as `indication` or `needs_validation` (with `provisional: true` if relevant under `E-03`).

## `M-05` — No Silent Escalation
- Never silently upgrade mode (e.g., `quick` -> `mid`/`deep`) or add auditors beyond the approved plan.
- If unexpected complexity emerges, report initial findings and offer an explicit escalation option for user approval.
