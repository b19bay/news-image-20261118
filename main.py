#!/usr/bin/env python3
"""news-image-20261118 — reproduce the entry image.

Copies the pre-rendered entry.png (next to this file) to the output
directory as entry.png, after checking it against the competition gate
(1024x1024, 1,048,576 bytes). Standard library only; no network access.

Usage:
    python3 main.py            # writes /output/entry.png
    MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py   # writes /tmp/out/entry.png
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"

# Competition gate (RULES.txt): image must be at most 1024x1024 and at most
# 1,048,576 bytes. Fail loudly instead of shipping a non-compliant entry.
MAX_WIDTH = 1024
MAX_HEIGHT = 1024
MAX_BYTES = 1_048_576


def png_dimensions(data: bytes) -> tuple[int, int]:
    """Read width/height from a PNG IHDR chunk (stdlib only)."""
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    if not SOURCE.is_file():
        print(f"error: {SOURCE} not found", file=sys.stderr)
        return 1
    data = SOURCE.read_bytes()
    width, height = png_dimensions(data)
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        print(f"error: image is {width}x{height}, over the {MAX_WIDTH}x{MAX_HEIGHT} limit",
              file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"error: image is {len(data)} bytes, over the {MAX_BYTES} byte limit",
              file=sys.stderr)
        return 1
    target.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({width}x{height}, {len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
