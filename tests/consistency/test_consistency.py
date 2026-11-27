#!/usr/bin/env python3
"""Consistency test suite for SSOT parity, Web purity, layout, and links."""

from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CORE_DIR = ROOT / "core"
WEB_DIR = ROOT / "logic-auditor-web"
LOCAL_DIR = ROOT / "logic-auditor-local"
SYNC_SCRIPT = ROOT / "build" / "sync_editions.py"

EXPECTED_CORE_FILES = [
    "contract.md",
    "evidence.md",
    "guardrails.md",
    "modes.md",
    "orchestrator.md",
    "reasoning.md",
    "reporting.md",
    "swarm.md",
]

RULE_HEADING_RE = re.compile(r"^##\s+`([CGOMRSEP]-\d{2})`", re.MULTILINE)
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


class ConsistencyTests(unittest.TestCase):
    def test_legacy_and_dev_infra_coupling_removed(self) -> None:
        self.assertFalse((ROOT / "logic-audit-panel").exists(), "Legacy folder logic-audit-panel/ must be removed.")
        self.assertFalse((ROOT / ".bima").exists(), ".bima/ must not exist in standalone mode.")
        self.assertFalse((ROOT / ".github").exists(), ".github/ must not exist in standalone mode.")

    def test_standalone_repo_hygiene_files_exist(self) -> None:
        for rel in ("README.md", "LICENSE", ".gitattributes", ".gitignore", "build/sync_editions.py"):
            path = ROOT / rel
            self.assertTrue(path.is_file(), f"Required standalone file missing: {rel}")

    def test_sync_check_passes_with_zero_drift(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(SYNC_SCRIPT), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=f"sync --check failed:\n{proc.stdout}\n{proc.stderr}")

    def test_core_modules_complete_and_unique_rule_ids(self) -> None:
        actual = sorted(p.name for p in CORE_DIR.glob("*.md"))
        self.assertEqual(actual, EXPECTED_CORE_FILES)

        seen_ids: dict[str, str] = {}
        for name in EXPECTED_CORE_FILES:
            text = (CORE_DIR / name).read_text(encoding="utf-8")
            ids = RULE_HEADING_RE.findall(text)
            self.assertGreater(len(ids), 0, f"No rule IDs found in core/{name}")
            for rule_id in ids:
                self.assertNotIn(
                    rule_id,
                    seen_ids,
                    f"Duplicate rule ID {rule_id} in core/{name} and {seen_ids.get(rule_id)}",
                )
                seen_ids[rule_id] = name

    def test_web_edition_is_pure_markdown_only(self) -> None:
        self.assertTrue((WEB_DIR / "SKILL.md").is_file())
        for item in WEB_DIR.rglob("*"):
            if item.is_dir():
                self.assertNotIn(item.name, {"scripts", "tools", "__pycache__"})
                continue
            self.assertEqual(item.suffix.lower(), ".md", f"Forbidden non-Markdown file in Web package: {item}")
            content = item.read_text(encoding="utf-8")
            self.assertNotRegex(content, r"(?<![a-zA-Z0-9_-])scripts/")
            self.assertNotRegex(content, r"(?<![a-zA-Z0-9_-])tools/")
            self.assertNotIn("validate_audit.py", content)

    def test_local_edition_layout_and_frontmatter(self) -> None:
        self.assertTrue((LOCAL_DIR / "SKILL.md").is_file())
        self.assertTrue((LOCAL_DIR / "references" / "harnesses.md").is_file())
        self.assertTrue((LOCAL_DIR / "scripts" / "validate_audit.py").is_file())

        for edition_name, skill_dir in (("logic-auditor-web", WEB_DIR), ("logic-auditor-local", LOCAL_DIR)):
            text = (skill_dir / "SKILL.md").read_text(encoding="utf-8").replace("\r\n", "\n")
            match = FRONTMATTER_RE.match(text)
            self.assertIsNotNone(match, f"Invalid YAML frontmatter in {edition_name}/SKILL.md")
            fm = match.group(1)
            self.assertIn(f"name: {edition_name}", fm)
            self.assertRegex(fm, r"description:\s+\S+")

    def test_no_broken_relative_markdown_links(self) -> None:
        scan_files = [ROOT / "README.md"]
        for base_dir in (CORE_DIR, WEB_DIR, LOCAL_DIR, ROOT / "tests" / "benchmark"):
            scan_files.extend(base_dir.rglob("*.md"))
        for md_file in scan_files:
            if not md_file.is_file():
                continue
            text = md_file.read_text(encoding="utf-8")
            for target in MD_LINK_RE.findall(text):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                resolved = (md_file.parent / target).resolve()
                self.assertTrue(
                    resolved.exists(),
                    f"Broken link in {md_file.relative_to(ROOT).as_posix()}: {target}",
                )


if __name__ == "__main__":
    unittest.main()
