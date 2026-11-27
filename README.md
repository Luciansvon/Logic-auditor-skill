# Logic Auditor V2

Universal, modular, evidence-based multi-perspective audit skill for physical products, designs, software, AI skills, workflows, games, research, business plans, and documents.

Builds from **one authoritative core (`core/`)** into **two standalone editions**:
- **Web Edition ([logic-auditor-web/](logic-auditor-web/SKILL.md)):** 100% pure Markdown (`0` scripts, `0` executables, `0` dependencies).
- **Local Edition ([logic-auditor-local/](logic-auditor-local/SKILL.md)):** synced core + 6-harness probe guide + deterministic Python 3 stdlib Audit Record validator.

> Responds in the user's own language and register (`everyday`, `professional`, or `technical`) while keeping skill internals concise and token-efficient.

---

## Architecture

```text
core/ (8 SSOT modules — edit here only)
  ├── contract.md      (precedence Levels 1–5, min-2 invariant, dual-horizon, re-audit)
  ├── guardrails.md    (read-only default, prompt-injection defense, anti-fabrication)
  ├── orchestrator.md  (13-stage pipeline, passive probe, Coverage Ledger, Stop Gate)
  ├── modes.md         (quick / mid / deep + low-token deep option)
  ├── reasoning.md     (10 adaptive methods, anti-ritual selection)
  ├── swarm.md         (dynamic auditor, 6 personas, Real/Virtual/External Swarm)
  ├── evidence.md      (19-key finding contract, P0–P3, anti-voting, deduplication)
  └── reporting.md     (Audit Record vs concise User Report, register adaptation)
        │
        │  python build/sync_editions.py
        ├───────────────────────────────────────┐
        ▼                                       ▼
logic-auditor-web/                      logic-auditor-local/
  ├── SKILL.md                            ├── SKILL.md
  └── references/ (pure .md snapshot)     ├── references/ (synced core + harnesses.md)
                                          └── scripts/validate_audit.py (stdlib only)
```

---

## Quick Start

### 1. Web Edition (`logic-auditor-web/`)
Upload or attach the [logic-auditor-web/](logic-auditor-web/SKILL.md) directory (`SKILL.md` + `references/`) to any Web AI platform. It uses zero bundled scripts and adapts automatically to native platform tools or single-agent `virtual_swarm`.

### 2. Local Edition (`logic-auditor-local/`)
Supported target harnesses (documented in [harnesses.md](logic-auditor-local/references/harnesses.md)): **Codex**, **Claude Code**, **Antigravity**, **Cursor**, **OpenCode**, and **Hermes Agent**.

Install in PowerShell (example for user skills directory):

```powershell
git clone https://github.com/Luciansvon/Logic-auditor-skill.git
$target = Join-Path $env:USERPROFILE '.agents\skills\logic-auditor-local'
Copy-Item -Path '.\Logic-auditor-skill\logic-auditor-local' -Destination $target -Recurse -Force
```

Validate any generated Audit Record JSON locally (Python 3 stdlib only, read-only):

```bash
python logic-auditor-local/scripts/validate_audit.py <path-to-audit-record.json>
```

---

## Key Mechanics

* **Passive Probe Before Pre-Audit (`LA-02`):** detects actual active tools/subagents first, then asks at most 3 targeted questions (mode, auditor count `>= 2`, focus/constraints).
* **Three Modes + Low-Token Deep:** `quick` (2–3 recommended), `mid` (4–6), `deep` (7–12, or **low-token `deep` with 2–3 perspectives**). Auditor count is chosen separately and locked to minimum `2` (`LA-03`).
* **Dual-Horizon & Re-Audit:** probes both `current_issue` and `future_scenario` (*premortem*), plus incremental re-audits (`fixed | persists | new | not_rechecked`).
* **Evidence Over Voting (`LA-04`, `LA-05`):** severity (`P0`–`P3`) never escalates by headcount; `virtual_swarm` locks `independent_discoveries` to `single_model`; `external_swarm` inputs enter as `external_unverified` and are sanitized against prompt injection.

| Tier | Practical Meaning | Action Posture |
| :--- | :--- | :--- |
| **P0 · Critical** | Severe, hard-to-reverse impact with strong evidence or urgent exposure path | Contain/halt exposure immediately and verify fix |
| **P1 · High** | Major impact with plausible path or near-term conditional risk | Test or mitigate before next release/decision (mark `provisional` if key data is missing) |
| **P2 · Medium** | Bounded, recoverable disruption or low-exposure flaw | Schedule fix/test and define escalation triggers |
| **P3 · Low** | Minor or cosmetic issue | Monitor or fix when relevant |

---

## Development Sync, Tests & Benchmark Status

Synchronize `core/` into both editions and verify zero drift + pure Markdown Web packaging:

```bash
python build/sync_editions.py
python build/sync_editions.py --check
```

Run the full consistency, adversarial, and benchmark unit test suite:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Run the deterministic contract & guardrail benchmark across 13 ground-truth scenarios and 7 Audit Record fixtures:

```bash
python tests/benchmark/run_deterministic_benchmark.py
```

See [BENCHMARK_REPORT.md](tests/benchmark/BENCHMARK_REPORT.md) for measured deterministic results. Live multi-run LLM comparative evaluations (`A_baseline_plain_ai` through `E_real_swarm`) are supported by [score_benchmark.py](tests/benchmark/score_benchmark.py) and remain to be executed with live model sessions before making statistical superiority claims.

---

## References & License Hygiene

This clean-room implementation draws verified architectural principles from public research and open specifications (zero verbatim code or text copied from restrictively licensed repositories such as AGPL-3.0 `666ghj/MiroFish` or CC-BY-SA-4.0 `trailofbits/skills`):

* Skill format & progressive disclosure: [Agent Skills Specification](https://agentskills.io/specification), [Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)
* Evidence, coverage & verification workflows: [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill), [trailofbits/skills](https://github.com/trailofbits/skills), [obra/superpowers](https://github.com/obra/superpowers), [scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
* Multi-perspective & reasoning designs: [666ghj/MiroFish](https://github.com/666ghj/MiroFish), [thinking-toolkit](https://github.com/ponomr/thinking-toolkit), [multi-perspective-meeting](https://github.com/Kim-FengLei/multi-perspective-meeting), [council-skill](https://github.com/tsenart/council-skill), [Leka74/openbot](https://github.com/Leka74/openbot), [CopilotKit/OpenBot](https://github.com/CopilotKit/OpenBot)
* Multi-agent failure modes, evals & security: [Anthropic Multi-Agent Research](https://www.anthropic.com/research/multi-agent-research-system), [Demystifying Evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents), [MAST (arXiv:2503.13657)](https://arxiv.org/abs/2503.13657), [Free-MAD (arXiv:2509.11035)](https://arxiv.org/abs/2509.11035), [Problem Drift (arXiv:2502.19559)](https://arxiv.org/abs/2502.19559), [Adaptive Debate (arXiv:2504.05047)](https://arxiv.org/abs/2504.05047), [AgentDojo](https://github.com/ethz-spylab/agentdojo), [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html), [NASA SE Handbook Appendix](https://www.nasa.gov/reference/system-engineering-handbook-appendix/), [W3C PROV Primer](https://www.w3.org/TR/prov-primer/)

Licensed under the [MIT License](LICENSE).
