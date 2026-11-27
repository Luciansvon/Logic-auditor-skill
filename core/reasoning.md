# Adaptive Reasoning Engine (`core/reasoning.md`)

Authoritative source for core reasoning methods and domain-adaptive selection. Reasoning methods guide *how* to probe an object; they never substitute for evidence (`E-01`).

## `R-01` — 10 Core Reasoning Methods
1. **First Principles:** strip design down to physical laws, hard constraints, or core requirements to expose flawed legacy assumptions.
2. **Inversion / Premortem:** assume total failure over the target horizon and trace backward to the most plausible failure chains (`C-04`).
3. **Causal / Root-Cause Analysis:** follow cause-effect chains from surface symptoms down to underlying mechanisms so distinct flaws are not conflated.
4. **Systems Thinking:** map dependencies, feedback loops, bottlenecks, and cascading failures when individually healthy parts interact.
5. **Second-Order Thinking:** evaluate downstream effects of a feature, mitigation, or decision on user behavior, system load, or long-term cost.
6. **Counterfactual Reasoning:** test "what if a core assumption breaks?" (dropped network, wet surface, invalid user input, policy change).
7. **Falsification:** construct competing hypotheses and actively seek evidence that **disproves** safety or correctness claims.
8. **Variant Analysis:** once one flaw pattern appears, sweep all analogous components for matching defects.
9. **Boundary / Stress Analysis:** probe extremes (min/max values, full queues, severe weather, unit-to-unit manufacturing variance, recovery states).
10. **Risk-Shifting / Trade-off Analysis:** check whether mitigating risk in one component silently transfers hazard or load elsewhere.

## `R-02` — Adaptive Selection Rule (Anti-Ritual)
- **Never run all 10 methods mechanically** on every lens.
- Select **1 to 3 high-leverage methods** matching the audit question, object domain, and auditor profile.

Quick domain guide:
- **Physical products & ergonomics:** First Principles, Boundary / Stress Analysis, Inversion / Premortem, Risk-Shifting.
- **Software, business logic & workflows:** Systems Thinking, Counterfactual Reasoning, Variant Analysis, Causal / Root-Cause.
- **AI skills, prompts & security:** Falsification, Inversion / Premortem, Second-Order Thinking, Boundary / Stress Analysis.
- **Business plans, research & policy docs:** First Principles, Second-Order Thinking, Falsification, Counterfactual Reasoning.

## `R-03` — Evidence Alignment
Every reasoning method applied MUST yield concrete inspection targets or test questions—never abstract commentary alone. Unverified counterfactuals or premortems remain `future_scenario` / `needs_validation` per [evidence.md](evidence.md).

## `R-04` — Discriminating Test Design
When competing explanations exist or decisive proof is missing, apply *Falsification* and *Boundary Analysis* to propose **the cheapest, sharpest discriminating test** with explicit pass/fail criteria.
