#!/usr/bin/env python3
"""Validate the active skill inventory and cross-agent metadata."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
CATALOG = SKILLS_DIR / "README.md"
PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
ROOT_README = ROOT / "README.md"


def frontmatter(text: str, path: Path, errors: list[str]) -> str:
    if not text.startswith("---\n"):
        errors.append(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return ""

    end = text.find("\n---\n", 4)
    if end == -1:
        errors.append(f"{path.relative_to(ROOT)}: unterminated YAML frontmatter")
        return ""

    return text[4:end]


def duplicates(values: list[str]) -> list[str]:
    return sorted({value for value in values if values.count(value) > 1})


def main() -> int:
    errors: list[str] = []
    skill_dirs = sorted(
        path.name
        for path in SKILLS_DIR.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
    active = set(skill_dirs)

    for name in skill_dirs:
        skill_path = SKILLS_DIR / name / "SKILL.md"
        skill_text = skill_path.read_text()
        metadata = frontmatter(skill_text, skill_path, errors)

        declared_name = re.search(r"(?m)^name:\s*(.+?)\s*$", metadata)
        if not declared_name:
            errors.append(f"skills/{name}/SKILL.md: missing name")
        elif declared_name.group(1).strip("\"'") != name:
            errors.append(
                f"skills/{name}/SKILL.md: declares name "
                f"{declared_name.group(1)!r}"
            )

        if not re.search(r"(?m)^description:\s*(?:.+|\|)\s*$", metadata):
            errors.append(f"skills/{name}/SKILL.md: missing description")

        manual = bool(
            re.search(
                r"(?m)^disable-model-invocation:\s*true\s*$",
                metadata,
            )
        )

        codex_path = SKILLS_DIR / name / "agents" / "openai.yaml"
        if not codex_path.is_file():
            errors.append(f"skills/{name}/agents/openai.yaml: missing")
            continue

        codex = codex_path.read_text()
        required_interface = {
            "interface": r"(?m)^interface:\s*$",
            "display_name": r'(?m)^  display_name:\s*"[^"]+"\s*$',
            "short_description": (
                r'(?m)^  short_description:\s*"[^"]+"\s*$'
            ),
        }
        for field, pattern in required_interface.items():
            if not re.search(pattern, codex):
                errors.append(
                    f"skills/{name}/agents/openai.yaml: missing or invalid "
                    f"{field}"
                )

        codex_manual = bool(
            re.search(
                r"(?m)^  allow_implicit_invocation:\s*false\s*$",
                codex,
            )
        )
        if manual and not codex_manual:
            errors.append(
                f"skills/{name}: manual in SKILL.md but not in Codex metadata"
            )
        if not manual and codex_manual:
            errors.append(
                f"skills/{name}: model-invoked in SKILL.md but manual in "
                "Codex metadata"
            )

    catalog_text = CATALOG.read_text()
    catalog_entries = re.findall(
        r"\[`([^`]+)`\]\(([^/)]+)/SKILL\.md\)",
        catalog_text,
    )
    catalog_names = [label for label, _ in catalog_entries]
    catalog_paths = [path for _, path in catalog_entries]
    for label, path in catalog_entries:
        if label != path:
            errors.append(
                f"skills/README.md: label {label!r} points to {path!r}"
            )

    for duplicate in duplicates(catalog_paths):
        errors.append(f"skills/README.md: duplicate entry {duplicate}")

    catalog_set = set(catalog_paths)
    for missing in sorted(active - catalog_set):
        errors.append(f"skills/README.md: missing {missing}")
    for stale in sorted(catalog_set - active):
        errors.append(f"skills/README.md: stale entry {stale}")
    if catalog_paths != sorted(catalog_paths):
        errors.append("skills/README.md: skill entries are not alphabetical")

    try:
        plugin_data = json.loads(PLUGIN.read_text())
    except (json.JSONDecodeError, OSError) as error:
        errors.append(f".claude-plugin/plugin.json: {error}")
        plugin_data = {}

    raw_plugin_entries = plugin_data.get("skills", [])
    if not isinstance(raw_plugin_entries, list):
        errors.append(".claude-plugin/plugin.json: skills must be an array")
        raw_plugin_entries = []

    plugin_names: list[str] = []
    for entry in raw_plugin_entries:
        if not isinstance(entry, str):
            errors.append(
                ".claude-plugin/plugin.json: every skill entry must be a string"
            )
            continue
        match = re.fullmatch(r"\./skills/([^/]+)", entry)
        if not match:
            errors.append(
                f".claude-plugin/plugin.json: invalid skill path {entry!r}"
            )
            continue
        plugin_names.append(match.group(1))

    for duplicate in duplicates(plugin_names):
        errors.append(f".claude-plugin/plugin.json: duplicate {duplicate}")

    plugin_set = set(plugin_names)
    for missing in sorted(active - plugin_set):
        errors.append(f".claude-plugin/plugin.json: missing {missing}")
    for stale in sorted(plugin_set - active):
        errors.append(f".claude-plugin/plugin.json: stale entry {stale}")
    if plugin_names != sorted(plugin_names):
        errors.append(".claude-plugin/plugin.json: skills are not alphabetical")

    root_readme = ROOT_README.read_text()
    count_match = re.search(
        r"collection currently contains\s+(\d+)(?:\s+published)?\s+skills",
        root_readme,
    )
    if not count_match:
        errors.append("README.md: missing active skill count")
    elif int(count_match.group(1)) != len(active):
        errors.append(
            "README.md: reports "
            f"{count_match.group(1)} skills; found {len(active)}"
        )

    if catalog_names != catalog_paths:
        errors.append("skills/README.md: skill labels and paths differ")

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(active)} skills: catalog, plugin, Codex metadata, "
        "and invocation policies agree."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
