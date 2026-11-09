#!/usr/bin/env python3
"""Check that a source-archive manifest covers every pin in an OrcaSlicer checkout.

The archive manifests in audit/ are transcribed by hand from upstream CMake.
This check makes the transcription falsifiable in both directions:

* uncovered: a SHA-256 literal, or a GIT_REPOSITORY, on a non-comment line of a
  git-tracked CMake file that the manifest does not account for. A SHA-256 is
  accounted for by an artifact's ``sha256`` or ``declared_sha256``, or by an
  excluded pin's ``sha256`` list. A Git repository is accounted for by an
  excluded pin's ``git_repository``.
* stale: a manifest artifact none of whose hashes occurs in the tree, or an
  excluded pin hash or repository that no longer occurs in the tree.

It reads only files that git tracks, so build directories with extracted
third-party sources are ignored. Commented-out lines (first non-blank character
``#``) are ignored. It does not evaluate CMake: it cannot tell whether a pin is
reachable in a given configuration, only that the manifest names it.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

HEX64 = re.compile(r"(?<![0-9A-Fa-f])[0-9A-Fa-f]{64}(?![0-9A-Fa-f])")
GIT_REPOSITORY = re.compile(r"\bGIT_REPOSITORY\s+\"?([^\s\")]+)")


def tracked_cmake_files(tree: Path) -> list[str]:
    output = subprocess.run(
        ["git", "-C", str(tree), "ls-files", "-z"],
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8")
    names = [name for name in output.split("\0") if name]
    return sorted(n for n in names if n.endswith(".cmake") or Path(n).name == "CMakeLists.txt")


def scan_tree(tree: Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    hashes: dict[str, list[str]] = {}
    repositories: dict[str, list[str]] = {}
    for name in tracked_cmake_files(tree):
        text = (tree / name).read_text(encoding="utf-8", errors="replace")
        for number, line in enumerate(text.splitlines(), start=1):
            if line.lstrip().startswith("#"):
                continue
            where = f"{name}:{number}"
            for match in HEX64.finditer(line):
                hashes.setdefault(match.group(0).lower(), []).append(where)
            for match in GIT_REPOSITORY.finditer(line):
                repositories.setdefault(match.group(1), []).append(where)
    return hashes, repositories


def check_coverage(tree: Path, manifest_path: Path) -> dict[str, Any]:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    tree_hashes, tree_repositories = scan_tree(tree)

    covered_hashes: set[str] = set()
    covered_repositories: set[str] = set()
    stale: list[dict[str, str]] = []

    for item in data.get("artifacts", []):
        own = {item["sha256"].lower()}
        if item.get("declared_sha256"):
            own.add(item["declared_sha256"].lower())
        covered_hashes |= own
        if not own & tree_hashes.keys():
            stale.append({"kind": "sha256", "value": item["sha256"].lower(), "id": item["id"]})

    for pin in data.get("excluded_pins", []):
        for value in pin.get("sha256", []):
            covered_hashes.add(value.lower())
            if value.lower() not in tree_hashes:
                stale.append({"kind": "sha256", "value": value.lower(), "id": pin["id"]})
        repository = pin.get("git_repository")
        if repository:
            covered_repositories.add(repository)
            if repository not in tree_repositories:
                stale.append({"kind": "git_repository", "value": repository, "id": pin["id"]})

    uncovered = [
        {"kind": "sha256", "value": value, "where": where}
        for value, where in sorted(tree_hashes.items())
        if value not in covered_hashes
    ] + [
        {"kind": "git_repository", "value": value, "where": where}
        for value, where in sorted(tree_repositories.items())
        if value not in covered_repositories
    ]
    return {
        "tree_hashes": len(tree_hashes),
        "tree_git_repositories": len(tree_repositories),
        "uncovered": uncovered,
        "stale": stale,
    }


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tree", type=Path, required=True, help="OrcaSlicer git checkout at the manifest's commit")
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args(argv)

    if not (args.tree / ".git").exists():
        print(f"ERROR: not a git checkout: {args.tree}", file=sys.stderr)
        return 2
    try:
        result = check_coverage(args.tree, args.manifest)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    for item in result["uncovered"]:
        print(f"UNCOVERED {item['kind']} {item['value']} at {', '.join(item['where'])}")
    for item in result["stale"]:
        print(f"STALE     {item['kind']} {item['value']} (manifest id {item['id']})")
    print(
        f"Scanned {result['tree_hashes']} SHA-256 literal(s) and "
        f"{result['tree_git_repositories']} GIT_REPOSITORY value(s): "
        f"{len(result['uncovered'])} uncovered, {len(result['stale'])} stale"
    )
    return 0 if not result["uncovered"] and not result["stale"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
