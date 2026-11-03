#!/usr/bin/env python3
"""Download OrcaSlicer dependency archives and verify their declared SHA-256.

This deliberately does not extract archives or execute build scripts. It checks
that downloaded bytes match the hashes declared by the pinned upstream CMake
source. A match is integrity evidence, not proof that the upstream source or
license is trustworthy.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def download(url: str, destination: Path) -> dict[str, Any]:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        raise ValueError(f"refusing non-HTTPS URL: {url}")

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "quality-first-slicer-source-audit/1.0"},
    )
    digest = hashlib.sha256()
    size = 0

    with urllib.request.urlopen(request, timeout=60) as response:
        final_url = response.geturl()
        if urllib.parse.urlparse(final_url).scheme != "https":
            raise ValueError(f"download redirected to non-HTTPS URL: {final_url}")
        with destination.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                output.write(chunk)
                digest.update(chunk)
                size += len(chunk)

    return {"final_url": final_url, "sha256": digest.hexdigest(), "bytes": size}


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("unsupported or missing manifest schema_version")
    if not isinstance(data.get("artifacts"), list):
        raise ValueError("manifest artifacts must be a list")

    seen: set[str] = set()
    for artifact in data["artifacts"]:
        artifact_id = artifact.get("id")
        expected = artifact.get("sha256", "")
        urls = artifact.get("urls")
        if not isinstance(artifact_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", artifact_id):
            raise ValueError(f"invalid artifact id: {artifact_id!r}")
        if artifact_id in seen:
            raise ValueError(f"duplicate artifact id: {artifact_id}")
        seen.add(artifact_id)
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected):
            raise ValueError(f"invalid SHA-256 for {artifact_id}")
        if not isinstance(urls, list) or not urls or not all(isinstance(u, str) for u in urls):
            raise ValueError(f"artifact {artifact_id} must have one or more URLs")
    return data


def verify_artifact(
    artifact: dict[str, Any],
    cache_dir: Path,
    preserve_mismatches_dir: Path | None = None,
) -> dict[str, Any]:
    artifact_id = artifact["id"]
    expected = artifact["sha256"].lower()
    cache_dir.mkdir(parents=True, exist_ok=True)
    if preserve_mismatches_dir is not None:
        preserve_mismatches_dir.mkdir(parents=True, exist_ok=True)
    cached = cache_dir / f"{artifact_id}.archive"

    if cached.is_file():
        observed, size = sha256_file(cached)
        if observed == expected:
            return {
                "id": artifact_id,
                "status": "PASS",
                "source_file": artifact.get("source_file"),
                "expected_sha256": expected,
                "observed_sha256": observed,
                "bytes": size,
                "cached": True,
                "url": None,
                "attempts": [],
            }

    attempts: list[dict[str, Any]] = []
    for url in artifact["urls"]:
        fd, temporary_name = tempfile.mkstemp(
            prefix=f".{artifact_id}.", suffix=".part", dir=cache_dir
        )
        os.close(fd)
        temporary = Path(temporary_name)
        try:
            result = download(url, temporary)
            attempt = {"url": url, **result}
            if result["sha256"].lower() == expected:
                os.replace(temporary, cached)
                return {
                    "id": artifact_id,
                    "status": "PASS",
                    "source_file": artifact.get("source_file"),
                    "expected_sha256": expected,
                    "observed_sha256": result["sha256"],
                    "bytes": result["bytes"],
                    "cached": False,
                    "url": result["final_url"],
                    "attempts": attempts + [attempt],
                }
            attempt["status"] = "HASH_MISMATCH"
            if preserve_mismatches_dir is not None:
                preserved = preserve_mismatches_dir / (
                    f"{artifact_id}.{len(attempts) + 1}.mismatch.archive"
                )
                os.replace(temporary, preserved)
                attempt["preserved_path"] = str(preserved)
            attempts.append(attempt)
        except (OSError, ValueError, urllib.error.URLError) as exc:
            attempts.append({"url": url, "status": "DOWNLOAD_ERROR", "error": str(exc)})
        finally:
            temporary.unlink(missing_ok=True)

    return {
        "id": artifact_id,
        "status": "FAIL",
        "source_file": artifact.get("source_file"),
        "expected_sha256": expected,
        "observed_sha256": None,
        "bytes": None,
        "cached": False,
        "url": None,
        "attempts": attempts,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("audit/orcaslicer-v2.4.2-source-archives.json"),
    )
    parser.add_argument("--cache-dir", type=Path, default=Path(".cache/source-archives"))
    parser.add_argument("--report", type=Path, default=Path("archive-verification-report.json"))
    parser.add_argument(
        "--preserve-mismatches-dir",
        type=Path,
        help="optional directory in which to retain downloaded archives that fail SHA-256",
    )
    parser.add_argument(
        "--artifact",
        action="append",
        dest="artifacts",
        help="verify only this artifact ID; may be supplied more than once",
    )
    args = parser.parse_args()

    try:
        manifest = load_manifest(args.manifest)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: cannot load manifest: {exc}", file=sys.stderr)
        return 2

    selected = manifest["artifacts"]
    if args.artifacts:
        wanted = set(args.artifacts)
        known = {item["id"] for item in selected}
        unknown = wanted - known
        if unknown:
            print(f"ERROR: unknown artifact ID(s): {', '.join(sorted(unknown))}", file=sys.stderr)
            return 2
        selected = [item for item in selected if item["id"] in wanted]

    args.cache_dir.mkdir(parents=True, exist_ok=True)
    if args.preserve_mismatches_dir is not None:
        args.preserve_mismatches_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for artifact in selected:
        result = verify_artifact(
            artifact, args.cache_dir, preserve_mismatches_dir=args.preserve_mismatches_dir
        )
        results.append(result)
        print(f"{result['status']:4} {result['id']}: {result.get('observed_sha256') or 'no verified digest'}")

    passed = sum(item["status"] == "PASS" for item in results)
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "upstream": manifest["upstream"],
        "manifest": str(args.manifest),
        "summary": {"passed": passed, "failed": len(results) - passed, "total": len(results)},
        "results": results,
        "excluded_pins": manifest.get("excluded_pins", []),
        "limitations": [
            "A matching digest proves byte-level agreement with the manifest hash only.",
            "The expected hashes were transcribed from upstream CMake and must be independently checked against that pinned source revision.",
            "This does not inspect archive contents, license notices, source provenance, patches, or binary redistribution.",
            "Archives retained after hash mismatches are diagnostic evidence only and must not be extracted or executed as trusted source.",
        ],
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Report: {args.report}")
    print(f"Result: {passed}/{len(results)} archives verified")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
