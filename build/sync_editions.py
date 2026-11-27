#!/usr/bin/env python3
"""SSOT synchronization and Web-purity checker for Logic Auditor V2."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = ROOT / "core"
WEB_DIR = ROOT / "logic-auditor-web"
WEB_REF_DIR = WEB_DIR / "references"
LOCAL_DIR = ROOT / "logic-auditor-local"
LOCAL_REF_DIR = LOCAL_DIR / "references"
MANIFEST_PATH = ROOT / "build" / "core_manifest.json"

LOCAL_ONLY_REFS = {"harnesses.md"}
FORBIDDEN_IN_CORE_AND_WEB = (
    re.compile(r"(?<![a-zA-Z0-9_-])scripts/", re.IGNORECASE),
    re.compile(r"(?<![a-zA-Z0-9_-])tools/", re.IGNORECASE),
    re.compile(r"validate_audit\.py", re.IGNORECASE),
    re.compile(r"\bpython3?\b", re.IGNORECASE),
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_lf(text: str) -> bytes:
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def scan_forbidden_patterns(path: Path, text: str) -> list[str]:
    hits: list[str] = []
    for pattern in FORBIDDEN_IN_CORE_AND_WEB:
        if pattern.search(text):
            hits.append(f"{path.relative_to(ROOT).as_posix()}: matches forbidden pattern '{pattern.pattern}'")
    return hits


def sync() -> int:
    if not CORE_DIR.is_dir():
        print(f"ERROR: core directory not found: {CORE_DIR}", file=sys.stderr)
        return 1

    core_files = sorted(CORE_DIR.glob("*.md"))
    if not core_files:
        print("ERROR: No .md modules found in core/", file=sys.stderr)
        return 1

    WEB_REF_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_REF_DIR.mkdir(parents=True, exist_ok=True)

    errors: list[str] = []
    manifest_files: dict[str, dict[str, object]] = {}
    core_names = {p.name for p in core_files}

    for src in core_files:
        raw_text = src.read_text(encoding="utf-8")
        errors.extend(scan_forbidden_patterns(src, raw_text))
        lf_bytes = normalize_lf(raw_text)
        # Keep core files deterministically normalized to LF.
        if src.read_bytes() != lf_bytes:
            src.write_bytes(lf_bytes)

        digest = sha256_bytes(lf_bytes)
        manifest_files[src.name] = {
            "sha256": digest,
            "bytes": len(lf_bytes),
        }

        (WEB_REF_DIR / src.name).write_bytes(lf_bytes)
        (LOCAL_REF_DIR / src.name).write_bytes(lf_bytes)

    # Remove stale files in Web and Local references (preserving local-only docs).
    for stale in WEB_REF_DIR.iterdir():
        if stale.is_file() and stale.name not in core_names:
            stale.unlink()

    for stale in LOCAL_REF_DIR.iterdir():
        if stale.is_file() and stale.name not in core_names and stale.name not in LOCAL_ONLY_REFS:
            stale.unlink()

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    manifest = {
        "schema_version": 1,
        "source_dir": "core",
        "files": manifest_files,
    }
    MANIFEST_PATH.write_bytes((json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))

    print(f"Synced {len(core_files)} core modules -> {WEB_REF_DIR.relative_to(ROOT).as_posix()} & {LOCAL_REF_DIR.relative_to(ROOT).as_posix()}")
    print(f"Manifest written: {MANIFEST_PATH.relative_to(ROOT).as_posix()}")
    return 0


def check() -> int:
    errors: list[str] = []

    if not CORE_DIR.is_dir():
        print("ERROR: core/ not found", file=sys.stderr)
        return 1

    core_files = sorted(CORE_DIR.glob("*.md"))
    if not core_files:
        errors.append("core/ contains no .md modules")

    if not MANIFEST_PATH.is_file():
        errors.append("build/core_manifest.json missing; run sync_editions.py first")
        manifest_files: dict[str, dict[str, object]] = {}
    else:
        manifest_data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        manifest_files = manifest_data.get("files", {})

    core_names = {p.name for p in core_files}
    if set(manifest_files.keys()) != core_names:
        errors.append(
            f"Manifest file list out of sync with core/: manifest={sorted(manifest_files)} core={sorted(core_names)}"
        )

    for src in core_files:
        src_bytes = src.read_bytes()
        if b"\r" in src_bytes:
            errors.append(f"{src.relative_to(ROOT).as_posix()}: contains CRLF/CR; LF required")
        src_text = src_bytes.decode("utf-8")
        errors.extend(scan_forbidden_patterns(src, src_text))

        src_hash = sha256_bytes(src_bytes)
        expected_entry = manifest_files.get(src.name)
        if not expected_entry or expected_entry.get("sha256") != src_hash:
            errors.append(f"Manifest checksum drift for {src.name}")

        for label, target_dir in (("web", WEB_REF_DIR), ("local", LOCAL_REF_DIR)):
            target = target_dir / src.name
            if not target.is_file():
                errors.append(f"Missing synced file in {label}: {target.relative_to(ROOT).as_posix()}")
            elif target.read_bytes() != src_bytes:
                errors.append(f"Byte mismatch with core in {label}: {target.relative_to(ROOT).as_posix()}")

    # Web purity check: strictly .md files only, no scripts/tools dirs, no local script refs.
    if not WEB_DIR.is_dir():
        errors.append("logic-auditor-web/ not found")
    else:
        for item in WEB_DIR.rglob("*"):
            rel = item.relative_to(ROOT).as_posix()
            if item.is_dir():
                if item.name in {"scripts", "tools", "__pycache__"}:
                    errors.append(f"Forbidden directory in Web package: {rel}")
                continue
            if item.suffix.lower() != ".md":
                errors.append(f"Forbidden non-Markdown file in Web package: {rel}")
                continue
            errors.extend(scan_forbidden_patterns(item, item.read_text(encoding="utf-8")))

        web_ref_names = {p.name for p in WEB_REF_DIR.iterdir() if p.is_file()} if WEB_REF_DIR.is_dir() else set()
        if web_ref_names != core_names:
            errors.append(f"Unexpected/missing files in logic-auditor-web/references/: {sorted(web_ref_names ^ core_names)}")

    if errors:
        for err in errors:
            print(f"FAIL: {err}", file=sys.stderr)
        return 1

    print(f"OK: {len(core_files)} core modules synced byte-for-byte to Web & Local; Web package is 100% pure Markdown.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize and validate Logic Auditor V2 SSOT editions.")
    parser.add_argument("--check", action="store_true", help="Verify sync parity and Web purity without modifying files.")
    args = parser.parse_args()
    return check() if args.check else sync()


if __name__ == "__main__":
    raise SystemExit(main())
