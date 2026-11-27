# Audit Mode Configuration (`core/modes.md`)

Authoritative source (Level 4 under `C-02`) for `quick`, `mid`, and `deep` mode defaults. Do not duplicate guardrails, reasoning methods, or evidence rules here.

## `M-01` — Mode vs Auditor Count Separation
- **Mode (`quick` | `mid` | `deep`)** controls analytical depth, required coverage breadth, interaction round caps, and verification intensity.
- **Auditor/perspective count** is a separate user choice, always bounded below by the Level 2 invariant `>= 2` (`C-03`).
- Numeric ranges below are **initial calibration defaults**, not rigid mandates overriding explicit user choices.

## `M-02` — Mode Matrix (Initial Calibration)

| Dimension | `quick` | `mid` | `deep` |
| :--- | :--- | :--- | :--- |
| **Primary goal** | Fast screen for urgent risks and obvious flaws | Balanced cross-component audit and targeted cross-checks | Exhaustive audit including cross-layer interactions |
| **Recommended auditors** | 2–3 perspectives | 4–6 perspectives | 7–12 perspectives *(low-token option: 2–3 perspectives)* |
| **Initial investigation** | 1 independent round | 1 independent round | 1 independent round |
| **Interaction / challenge rounds** | 0–1 targeted round (`P0`/`P1` only) | 1 challenge & cross-check round | Up to 2 targeted rounds as materially needed |
| **Material findings cap / auditor** | Max 3 findings | Max 4 findings | Max 5 findings *(quality over volume)* |
| **Coverage Ledger scope** | Core high-risk components | All primary flows & key dependencies | Full scope + edge, stress, and recovery paths |
| **Verification intensity** | Check `P0`/`P1` if accessible; log `P2`/`P3` as `needs_validation` if untested | Challenge/re-check `P0`/`P1`; sample `P2` within budget | Maximum verification on `P0`/`P1`; cross-check `P2` within budget |

*Calibration note: these default caps are initial baselines subject to benchmark tuning.*

## `M-03` — Low-Token `deep` Option
Users may explicitly choose **`deep` with 2–3 auditors** for thorough coverage and strict verification without high multi-agent token cost. Depth is achieved via systematic coverage partitioning and strict verification, not headcount.

## `M-04` — Low-Severity Verification Policy (`P2` / `P3`)
- `P0` and `P1` findings always take priority over verification reserves (`O-05`).
- `P2` and `P3` findings MUST NOT starve `P0`/`P1` verification. When budget is tight, record unverified `P2`/`P3` items as `indication` or `needs_validation` (with `provisional: true` if relevant under `E-03`).

## `M-05` — No Silent Escalation
- Never silently upgrade mode (e.g., `quick` -> `mid`/`deep`) or add auditors beyond the approved plan.
- If unexpected complexity emerges, report initial findings and offer an explicit escalation option for user approval.
