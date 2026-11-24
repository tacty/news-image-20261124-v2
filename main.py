#!/usr/bin/env python3
"""make.fun entry v2 — "Sum up 24 November's world news in one image".

Night-Edition design (dark tabloid: near-black background, red
masthead and footer bands, gold dateline, numbered colour-coded
stories — see news-image-template/DESIGN-RULES.md). Writes the
bundled front-page image to /output/entry.png. No network, no
randomness, no clock: every run writes exactly the same bytes.
"""
import filecmp
import os
import shutil
import struct
from pathlib import Path


def check_png(path: Path) -> None:
    """Refuse anything the gate would reject: not a PNG, over 1 MiB, or over 1024x1024."""
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"not a PNG file: {path}")
    if len(data) > 1_048_576:
        raise SystemExit(f"image over 1 MiB: {len(data)} bytes")
    width, height = struct.unpack(">II", data[16:24])
    if width > 1024 or height > 1024:
        raise SystemExit(f"image over 1024x1024: {width}x{height}")


def main() -> None:
    here = Path(__file__).resolve().parent
    src = here / "image.png"
    if not src.is_file():
        pngs = sorted(here.glob("*.png"))
        if len(pngs) == 1:
            src = pngs[0]
    if not src.is_file():
        raise SystemExit(f"bundled image not found: {src}")
    check_png(src)
    dst = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    if not filecmp.cmp(src, dst, shallow=False):
        raise SystemExit("written file does not match the bundled image")
    print(f"wrote {dst} ({dst.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
