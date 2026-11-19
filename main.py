#!/usr/bin/env python3
"""news-image-20261118 entry program (fresh rebuild).

Copies the bundled front-page image to the output directory as entry.png.
Python 3 standard library only; no network, no fonts, no rendering at run
time — the image is fully embedded in this repository.

Usage:
    python3 main.py                                  # writes /output/entry.png
    MAKEFUN_OUTPUT_DIR=/tmp/out1 python3 main.py     # writes /tmp/out1/entry.png
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
LIMIT_W, LIMIT_H, LIMIT_BYTES = 1024, 1024, 1_048_576


def check_png(blob):
    """Return (width, height) of a PNG blob, or raise on bad input."""
    if blob[:8] != b"\x89PNG\r\n\x1a\n" or len(blob) < 33:
        raise ValueError("entry.png is not a valid PNG")
    w, h = struct.unpack(">II", blob[16:24])
    if w > LIMIT_W or h > LIMIT_H:
        raise ValueError(f"image {w}x{h} exceeds {LIMIT_W}x{LIMIT_H}")
    if len(blob) > LIMIT_BYTES:
        raise ValueError(f"image {len(blob)} bytes exceeds {LIMIT_BYTES}")
    return w, h


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    blob = open(SOURCE, "rb").read()
    w, h = check_png(blob)
    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as f:
        f.write(blob)
    # Verify the copy landed intact before reporting success.
    got = open(dest, "rb").read()
    if hashlib.sha256(got).hexdigest() != hashlib.sha256(blob).hexdigest():
        raise ValueError(f"copy to {dest} failed verification")
    print(f"wrote {dest} ({w}x{h}, {len(blob)} bytes, "
          f"sha256 {hashlib.sha256(blob).hexdigest()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
