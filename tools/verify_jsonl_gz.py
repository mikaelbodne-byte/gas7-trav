#!/usr/bin/env python3
"""Read-only integrity checker for gzip-compressed JSON Lines archives.

This program does not connect to Supabase, access Drive, or delete files.
For a meaningful end-to-end check, supply the expected SHA-256 digest from a
trusted manifest and compare the stored item count with that manifest.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from pathlib import Path


def verify(path: Path, expected_sha256: str | None = None, expected_count: int | None = None) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    digest = hashlib.sha256()
    count = 0
    with gzip.open(path, "rb") as stream:
        for line in stream:
            digest.update(line)
            if not line.strip():
                raise ValueError(f"Empty JSONL record at line {count + 1}")
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError(f"Record at line {count + 1} is not a JSON object")
            count += 1
    actual_hash = digest.hexdigest()
    if expected_sha256 is not None and actual_hash.lower() != expected_sha256.lower():
        raise ValueError("Uncompressed SHA-256 mismatch")
    if expected_count is not None and count != expected_count:
        raise ValueError(f"Record count mismatch: {count} != {expected_count}")
    return {"file": str(path), "records": count, "sha256_uncompressed": actual_hash,
            "hash_checked": expected_sha256 is not None, "count_checked": expected_count is not None}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="Path to .jsonl.gz archive")
    parser.add_argument("--sha256", help="Expected SHA-256 of uncompressed JSONL bytes")
    parser.add_argument("--count", type=int, help="Expected number of JSON objects")
    args = parser.parse_args()
    try:
        result = verify(args.archive, args.sha256, args.count)
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, **result}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
