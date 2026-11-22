#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261122.

Copies the pre-rendered entry image (entry/entry.png, drawn in code by
compose.py) to the output directory as entry.png, then verifies the copy
byte for byte with SHA-256 and makes it world-readable (mode 0644).

Standard library only, no network. Deterministic: the same input bytes
always produce the same output bytes.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry", "entry.png")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if not os.path.isfile(SOURCE):
        print("missing source image: %s" % SOURCE, file=sys.stderr)
        return 1
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, "entry.png")
    expected = sha256_of(SOURCE)
    shutil.copyfile(SOURCE, destination)
    os.chmod(destination, 0o644)
    actual = sha256_of(destination)
    if actual != expected:
        print("SHA-256 mismatch: %s != %s" % (actual, expected),
              file=sys.stderr)
        return 1
    size = os.path.getsize(destination)
    print("entry.png: %s (%d bytes, source %d bytes)"
          % (actual, size, os.path.getsize(SOURCE)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
