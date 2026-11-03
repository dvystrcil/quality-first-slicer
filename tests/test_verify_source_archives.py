"""Unit tests for tools/verify-source-archives.py (network access is mocked)."""

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from io import BytesIO

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "verify-source-archives.py"
SPEC = importlib.util.spec_from_file_location("verify_source_archives", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class FakeResponse(BytesIO):
    def __init__(self, payload: bytes, final_url: str = "https://example.test/archive"):
        super().__init__(payload)
        self.final_url = final_url

    def geturl(self):
        return self.final_url

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.close()


class VerifySourceArchivesTests(unittest.TestCase):
    def test_sha256_file_returns_digest_and_size(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "payload.bin"
            payload = b"known fixture\x00bytes"
            path.write_bytes(payload)
            digest, size = MODULE.sha256_file(path)
        self.assertEqual(digest, hashlib.sha256(payload).hexdigest())
        self.assertEqual(size, len(payload))

    def test_load_manifest_rejects_invalid_digest(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps({
                "schema_version": 1,
                "artifacts": [{"id": "fixture", "urls": ["https://example.test/a"], "sha256": "bad"}],
            }))
            with self.assertRaisesRegex(ValueError, "invalid SHA-256"):
                MODULE.load_manifest(path)

    @patch.object(MODULE.urllib.request, "urlopen")
    def test_verify_artifact_passes_for_matching_download(self, urlopen):
        payload = b"archive fixture"
        urlopen.return_value = FakeResponse(payload)
        artifact = {
            "id": "fixture",
            "source_file": "deps/fixture.cmake",
            "urls": ["https://example.test/archive"],
            "sha256": hashlib.sha256(payload).hexdigest(),
        }
        with tempfile.TemporaryDirectory() as directory:
            result = MODULE.verify_artifact(artifact, Path(directory))
            cached = Path(directory) / "fixture.archive"
            self.assertTrue(cached.is_file())
            self.assertEqual(cached.read_bytes(), payload)
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["cached"])
        self.assertEqual(result["bytes"], len(payload))

    @patch.object(MODULE.urllib.request, "urlopen")
    def test_verify_artifact_fails_on_hash_mismatch(self, urlopen):
        urlopen.return_value = FakeResponse(b"unexpected bytes")
        artifact = {
            "id": "fixture",
            "urls": ["https://example.test/archive"],
            "sha256": hashlib.sha256(b"expected bytes").hexdigest(),
        }
        with tempfile.TemporaryDirectory() as directory:
            result = MODULE.verify_artifact(artifact, Path(directory))
            self.assertFalse((Path(directory) / "fixture.archive").exists())
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["attempts"][0]["status"], "HASH_MISMATCH")

    @patch.object(MODULE.urllib.request, "urlopen")
    def test_cached_archive_is_reverified_without_network(self, urlopen):
        payload = b"cached archive"
        artifact = {
            "id": "fixture",
            "urls": ["https://example.test/archive"],
            "sha256": hashlib.sha256(payload).hexdigest(),
        }
        with tempfile.TemporaryDirectory() as directory:
            cached = Path(directory) / "fixture.archive"
            cached.write_bytes(payload)
            result = MODULE.verify_artifact(artifact, Path(directory))
        urlopen.assert_not_called()
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["cached"])


if __name__ == "__main__":
    unittest.main()
