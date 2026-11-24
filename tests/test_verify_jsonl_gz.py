"""Purely synthetic tests: no production data or credentials."""
import gzip
import hashlib
import tempfile
import unittest
from pathlib import Path
from tools.verify_jsonl_gz import verify


class ArchiveVerifierTest(unittest.TestCase):
    def make_file(self, raw: bytes) -> Path:
        self.tmp = tempfile.TemporaryDirectory()
        path = Path(self.tmp.name) / "synthetic.jsonl.gz"
        with gzip.open(path, "wb") as f:
            f.write(raw)
        self.addCleanup(self.tmp.cleanup)
        return path

    def test_valid_archive(self):
        raw = b'{"id":1}\n{"id":2}\n'
        path = self.make_file(raw)
        result = verify(path, hashlib.sha256(raw).hexdigest(), 2)
        self.assertEqual(result["records"], 2)
        self.assertTrue(result["hash_checked"])

    def test_bad_digest_is_rejected(self):
        path = self.make_file(b'{"id":1}\n')
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            verify(path, "0" * 64, 1)

    def test_wrong_count_is_rejected(self):
        path = self.make_file(b'{"id":1}\n')
        with self.assertRaisesRegex(ValueError, "count"):
            verify(path, expected_count=2)

    def test_invalid_json_is_rejected(self):
        path = self.make_file(b'not-json\n')
        with self.assertRaises(ValueError):
            verify(path)


if __name__ == "__main__":
    unittest.main()
