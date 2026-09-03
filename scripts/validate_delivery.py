#!/usr/bin/env python3
"""Full-decode a delivered video and validate basic technical expectations."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def find_ffmpeg(explicit: str | None) -> str:
    candidate = explicit or os.environ.get("FFMPEG_BIN") or shutil.which("ffmpeg")
    if not candidate:
        raise RuntimeError("FFmpeg not found. Pass --ffmpeg or set FFMPEG_BIN.")
    return candidate


def inspect(ffmpeg: str, path: Path) -> dict:
    result = subprocess.run([ffmpeg, "-hide_banner", "-i", str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    output = result.stderr + result.stdout
    duration_match = re.search(r"Duration:\s*(\d{2}):(\d{2}):(\d{2}\.\d+)", output)
    video_match = re.search(r"Video:.*?(\d{2,5})x(\d{2,5})", output)
    fps_match = re.search(r"([\d.]+)\s*fps", output)
    duration = None
    if duration_match:
        duration = int(duration_match.group(1)) * 3600 + int(duration_match.group(2)) * 60 + float(duration_match.group(3))
    return {
        "durationSec": duration,
        "width": int(video_match.group(1)) if video_match else None,
        "height": int(video_match.group(2)) if video_match else None,
        "fps": float(fps_match.group(1)) if fps_match else None,
        "hasVideo": "Video:" in output,
        "hasAudio": "Audio:" in output,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--ffmpeg", help="Path to FFmpeg executable")
    parser.add_argument("--expect-resolution", metavar="WIDTHxHEIGHT")
    parser.add_argument("--expect-duration", type=float, help="Expected duration in seconds")
    parser.add_argument("--tolerance", type=float, default=0.25, help="Duration tolerance in seconds")
    parser.add_argument("--require-audio", action="store_true")
    parser.add_argument("--skip-decode", action="store_true", help="Inspect metadata without full decoding")
    args = parser.parse_args()

    errors: list[str] = []
    if not args.input.is_file() or args.input.stat().st_size < 1024:
        errors.append("Input is missing or too small to be a valid delivery")
        print(json.dumps({"passed": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1

    try:
        ffmpeg = find_ffmpeg(args.ffmpeg)
    except RuntimeError as error:
        print(json.dumps({"passed": False, "errors": [str(error)]}, ensure_ascii=False, indent=2))
        return 1

    metadata = inspect(ffmpeg, args.input)
    if not metadata["hasVideo"]:
        errors.append("No video stream detected")
    if args.require_audio and not metadata["hasAudio"]:
        errors.append("Required audio stream is missing")
    if args.expect_resolution:
        width, height = [int(value) for value in args.expect_resolution.lower().split("x", 1)]
        if (metadata["width"], metadata["height"]) != (width, height):
            errors.append(f"Expected {width}x{height}, got {metadata['width']}x{metadata['height']}")
    if args.expect_duration is not None:
        if metadata["durationSec"] is None or abs(metadata["durationSec"] - args.expect_duration) > args.tolerance:
            errors.append(f"Expected duration {args.expect_duration:.3f}s ± {args.tolerance:.3f}s, got {metadata['durationSec']}")

    decode_error = None
    if not args.skip_decode:
        result = subprocess.run([ffmpeg, "-hide_banner", "-v", "error", "-xerror", "-i", str(args.input), "-f", "null", os.devnull], capture_output=True, text=True, encoding="utf-8", errors="replace")
        if result.returncode != 0:
            decode_error = (result.stderr or result.stdout).strip()
            errors.append("Full decode failed")

    report = {"passed": not errors, "file": str(args.input), "sizeBytes": args.input.stat().st_size, "metadata": metadata, "decodeError": decode_error, "errors": errors}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
