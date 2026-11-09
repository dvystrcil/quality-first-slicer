"""Unit tests for tools/check-archive-manifest-coverage.py.

Each test builds a tiny git repository standing in for an OrcaSlicer checkout,
because the tool reads only git-tracked files.
"""

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "check-archive-manifest-coverage.py"
SPEC = importlib.util.spec_from_file_location("check_archive_manifest_coverage", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

H1 = "1" * 64
H2 = "2" * 64
H3 = "3" * 64
H4 = "a" * 64


def manifest(artifacts=(), excluded=()):
    return {
        "schema_version": 1,
        "upstream": {"repository": "https://example.test/x", "ref": "v0", "commit": "0" * 40},
        "artifacts": list(artifacts),
        "excluded_pins": list(excluded),
    }


def artifact(artifact_id, sha256, **extra):
    return {"id": artifact_id, "source_file": "deps/x.cmake", "urls": ["https://example.test/a.zip"],
            "sha256": sha256, **extra}


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.tree = self.root / "tree"
        self.tree.mkdir()
        subprocess.run(["git", "init", "-q", str(self.tree)], check=True)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, relpath, text, track=True):
        path = self.tree / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        if track:
            subprocess.run(["git", "-C", str(self.tree), "add", relpath], check=True)

    def check(self, data):
        path = self.root / "manifest.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return MODULE.check_coverage(self.tree, path)

    def test_fully_covered_tree_has_no_findings(self):
        self.write("deps/A/A.cmake", f"URL https://a.test/a.zip\nURL_HASH SHA256={H1}\n")
        result = self.check(manifest([artifact("a", H1)]))
        self.assertEqual(result["uncovered"], [])
        self.assertEqual(result["stale"], [])
        self.assertEqual(result["tree_hashes"], 1)

    def test_hash_missing_from_manifest_is_reported_with_location(self):
        self.write("deps/A/A.cmake", f"URL_HASH SHA256={H1}\n")
        self.write("deps/B/B.cmake", f"# header\nset(_b_hash \"{H2}\")\n")
        result = self.check(manifest([artifact("a", H1)]))
        self.assertEqual(result["uncovered"], [{"kind": "sha256", "value": H2, "where": ["deps/B/B.cmake:2"]}])

    def test_manifest_hash_absent_from_tree_is_stale(self):
        self.write("deps/A/A.cmake", f"URL_HASH SHA256={H1}\n")
        result = self.check(manifest([artifact("a", H1), artifact("gone", H3)]))
        self.assertEqual(result["stale"], [{"kind": "sha256", "value": H3, "id": "gone"}])

    def test_commented_out_hash_is_ignored(self):
        self.write("deps/A/A.cmake", f"  # URL_HASH SHA256={H2}\nURL_HASH SHA256={H1}\n")
        result = self.check(manifest([artifact("a", H1)]))
        self.assertEqual(result["uncovered"], [])
        self.assertEqual(result["tree_hashes"], 1)

    def test_uppercase_tree_hash_matches_lowercase_manifest(self):
        self.write("deps/A/A.cmake", f"URL_HASH SHA256={H4.upper()}\n")
        result = self.check(manifest([artifact("a", H4)]))
        self.assertEqual(result["uncovered"], [])
        self.assertEqual(result["stale"], [])

    def test_declared_and_excluded_hashes_count_as_covered(self):
        self.write("deps/A/A.cmake", f"URL_HASH SHA256={H2}\n")
        self.write("deps/B/B.cmake", f"set(PREBUILD_HASH \"{H3}\")\n")
        data = manifest(
            [artifact("a", H1, declared_sha256=H2)],
            [{"id": "b-bin", "source_file": "deps/B/B.cmake", "reason": "binary", "sha256": [H3]}],
        )
        result = self.check(data)
        self.assertEqual(result["uncovered"], [])
        # The corrected digest H1 is not in the tree, but the declared one is,
        # so the artifact is not stale.
        self.assertEqual(result["stale"], [])

    def test_git_repository_must_be_covered_by_an_excluded_pin(self):
        self.write("deps/G/G.cmake", 'GIT_REPOSITORY "https://example.test/g.git"\nGIT_TAG v1\n')
        result = self.check(manifest())
        self.assertEqual(result["uncovered"],
                         [{"kind": "git_repository", "value": "https://example.test/g.git",
                           "where": ["deps/G/G.cmake:1"]}])
        covered = self.check(manifest(excluded=[{"id": "g", "source_file": "deps/G/G.cmake", "reason": "git",
                                                 "git_repository": "https://example.test/g.git"}]))
        self.assertEqual(covered["uncovered"], [])

    def test_excluded_git_repository_absent_from_tree_is_stale(self):
        self.write("deps/A/A.cmake", f"URL_HASH SHA256={H1}\n")
        result = self.check(manifest([artifact("a", H1)], [
            {"id": "g", "source_file": "deps/G/G.cmake", "reason": "git",
             "git_repository": "https://example.test/g.git"}]))
        self.assertEqual(result["stale"], [{"kind": "git_repository", "value": "https://example.test/g.git", "id": "g"}])

    def test_untracked_and_non_cmake_files_are_ignored(self):
        self.write("deps/A/A.cmake", f"URL_HASH SHA256={H1}\n")
        self.write("deps/build/extracted/CMakeLists.txt", f"URL_HASH SHA256={H2}\n", track=False)
        self.write("deps_src/x/x.c", f"/* {H3} */\n")
        self.write("CMakeLists.txt", f"set(UV_SHA \"{H4}\")\n")
        result = self.check(manifest([artifact("a", H1), artifact("uv", H4)]))
        self.assertEqual(result["uncovered"], [])
        self.assertEqual(result["tree_hashes"], 2)

    def test_main_exit_codes(self):
        self.write("deps/A/A.cmake", f"URL_HASH SHA256={H1}\n")
        good = self.root / "good.json"
        good.write_text(json.dumps(manifest([artifact("a", H1)])), encoding="utf-8")
        bad = self.root / "bad.json"
        bad.write_text(json.dumps(manifest()), encoding="utf-8")
        self.assertEqual(MODULE.main(["--tree", str(self.tree), "--manifest", str(good)]), 0)
        self.assertEqual(MODULE.main(["--tree", str(self.tree), "--manifest", str(bad)]), 1)
        self.assertEqual(MODULE.main(["--tree", str(self.root / "missing"), "--manifest", str(good)]), 2)


if __name__ == "__main__":
    unittest.main()
