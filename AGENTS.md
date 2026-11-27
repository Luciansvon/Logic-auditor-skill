# Logic Auditor Skill — Project Guardrails

1. **Mode Latency Separation:** `quick` mode MUST operate on a fast-path from `SKILL.md` (0–1 reference reads, 0 cross-check rounds, no default JSON dump) so it finishes measurably faster than `mid` and `deep`.
2. **Hard Report Brevity:** Default User Reports MUST stay within hard word caps (`quick <= 350 words`, `mid <= 550 words`, `deep <= 750 words`) using one compact findings table instead of repetitive multi-paragraph blocks.
3. **Validator Key Parity:** Any change to Audit Record top-level or finding keys in `core/reporting.md` or `core/evidence.md` MUST match `logic-auditor-local/scripts/validate_audit.py` exactly and pass `python -m unittest discover -s tests -p "test_*.py" -v`.
4. **SSOT Discipline:** Edit only `core/*.md`, then run `python build/sync_editions.py` and `python build/sync_editions.py --check`. Never add non-Markdown files or script references inside `logic-auditor-web/`.
