# Local Harness Capability & Adapter Guide

Supplements [orchestrator.md](orchestrator.md) for local environments. Core rule: **always detect capabilities from tools and permissions actually active in the session, never from harness name alone.**

## 1. Six Target Harnesses Quick Matrix

| Harness | Real Subagent Check (`real_swarm`) | Local Evidence Access | Artifact Persistence | Operational Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Codex** | Check whether a subagent/delegation tool is enabled in-session | Read-only file reads and approved shell commands | Workspace artifact files if permitted | Stay read-only by default; never edit target objects unasked |
| **Claude Code** | Check availability of isolated-context subagent spawning | File read/search tools and read-only shell checks | Local files/artifacts per directory permissions | Respect tool allowlists; isolate initial auditor context |
| **Antigravity** | Check `invoke_subagent` in the active tool list | `read_file` and read-only `run_command` checks | Session artifact directory or target files | Level 1 platform policy overrides mode settings |
| **Cursor** | Check whether multi-agent/subagent delegation is active | Workspace reads and approved terminal checks | Workspace files if authorized by user | Fall back cleanly to `virtual_swarm` with disclosure if single-agent |
| **OpenCode** | Check exposed agent-delegation tools in the session | Repo reads and read-only inspection commands | Local files when permitted | Enforce round caps early to keep verification budget intact |
| **Hermes Agent** | Check parallel worker/delegation support in active runtime | File and terminal access per workspace policy | Session artifacts or structured output | Log restricted tools explicitly under `limitations` |

## 2. Topology Selection from Passive Probe

1. **`real_swarm`:** select only when a real subagent tool is available **and** session policy permits launching at least 2 isolated-context auditors.
2. **`virtual_swarm`:** select automatically when no real subagent tool exists, permissions restrict to single-agent execution, or token budget requires single-model cycling. Lock `independent_discoveries` to `"single_model"` (or `1`) per `LA-04`.
3. **`external_swarm`:** select only when the user explicitly opts to run task packets in external sessions/models and paste outputs back. Treat all pasted claims as `external_unverified` (`LA-05`).

## 3. Deterministic Local Validator

When Python 3 and read-only CLI execution are available, validate the Audit Record JSON before finalizing the report:

```bash
python scripts/validate_audit.py <path-to-audit-record.json>
```

Notes:
- Read-only: inspects only the target JSON file and checks structural invariants (`LA-03`, `LA-04`, `LA-05`, `LA-09`, `BUDGET-01`, evidence/coverage rules).
- Deterministic validation verifies structure and invariants, not real-world semantic truth; evidence honesty remains the Moderator's responsibility.
