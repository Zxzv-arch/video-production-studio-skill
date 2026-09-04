#!/usr/bin/env python3
"""Full-decode a delivery and validate metadata, color tags, and optional loudness."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def find_ffmpeg(explicit: str | None) -> str:
    candidate = explicit or os.environ.get("FFMPEG_BIN") or shutil.which("ffmpeg")
    if not candidate:
        raise RuntimeError("FFmpeg not found. Pass --ffmpeg or set FFMPEG_BIN.")
    return candidate


def find_ffprobe(ffmpeg: str, explicit: str | None) -> str:
    candidate = explicit or os.environ.get("FFPROBE_BIN") or shutil.which("ffprobe")
    if candidate:
        return candidate
    ffmpeg_path = Path(ffmpeg)
    sibling = ffmpeg_path.with_name("ffprobe.exe" if os.name == "nt" else "ffprobe")
    if ffmpeg_path.parent != Path(".") and sibling.is_file():
        return str(sibling)
    raise RuntimeError("FFprobe not found. Pass --ffprobe or set FFPROBE_BIN.")


def ratio(value: str | None) -> float | None:
    if not value or value in {"0/0", "N/A"}:
        return None
    if "/" in value:
        numerator, denominator = value.split("/", 1)
        return float(numerator) / float(denominator) if float(denominator) else None
    return float(value)


def inspect(ffprobe: str, path: Path) -> dict[str, Any]:
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout).strip() or "FFprobe failed")
    payload = json.loads(result.stdout)
    streams = payload.get("streams", [])
    video = next((stream for stream in streams if stream.get("codec_type") == "video"), None)
    audio = next((stream for stream in streams if stream.get("codec_type") == "audio"), None)
    duration_value = payload.get("format", {}).get("duration") or (video or {}).get("duration")
    duration = float(duration_value) if duration_value not in {None, "N/A"} else None
    return {
        "durationSec": duration,
        "width": video.get("width") if video else None,
        "height": video.get("height") if video else None,
        "fps": (ratio(video.get("avg_frame_rate")) or ratio(video.get("r_frame_rate"))) if video else None,
        "hasVideo": video is not None,
        "hasAudio": audio is not None,
        "videoCodec": video.get("codec_name") if video else None,
        "audioCodec": audio.get("codec_name") if audio else None,
        "pixelFormat": video.get("pix_fmt") if video else None,
        "colorRange": video.get("color_range") if video else None,
        "colorSpace": video.get("color_space") if video else None,
        "colorTransfer": video.get("color_transfer") if video else None,
        "colorPrimaries": video.get("color_primaries") if video else None,
    }


def measure_loudness(ffmpeg: str, path: Path) -> dict[str, float | None]:
    result = subprocess.run(
        [ffmpeg, "-hide_banner", "-nostats", "-i", str(path), "-filter_complex", "ebur128=peak=true", "-f", "null", os.devnull],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = result.stderr + result.stdout
    if result.returncode != 0:
        raise RuntimeError(output.strip() or "EBU R128 measurement failed")
    integrated = re.findall(r"^\s*I:\s*(-?\d+(?:\.\d+)?)\s+LUFS", output, re.MULTILINE)
    true_peak = re.findall(r"^\s*Peak:\s*(-?\d+(?:\.\d+)?)\s+dBFS", output, re.MULTILINE)
    return {
        "integratedLufs": float(integrated[-1]) if integrated else None,
        "truePeakDbfs": float(true_peak[-1]) if true_peak else None,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--ffmpeg", help="Path to FFmpeg executable")
    parser.add_argument("--ffprobe", help="Path to FFprobe executable")
    parser.add_argument("--expect-resolution", metavar="WIDTHxHEIGHT")
    parser.add_argument("--expect-duration", type=float, help="Expected duration in seconds")
    parser.add_argument("--tolerance", type=float, default=0.25, help="Duration tolerance in seconds")
    parser.add_argument("--require-audio", action="store_true")
    parser.add_argument("--expect-pixel-format")
    parser.add_argument("--expect-color-range")
    parser.add_argument("--expect-color-space")
    parser.add_argument("--expect-color-transfer")
    parser.add_argument("--expect-color-primaries")
    parser.add_argument("--require-color-tags", action="store_true")
    parser.add_argument("--measure-loudness", action="store_true")
    parser.add_argument("--expect-lufs", type=float)
    parser.add_argument("--lufs-tolerance", type=float, default=1.0)
    parser.add_argument("--max-true-peak", type=float, help="Maximum accepted dBFS true peak, for example -1.5")
    parser.add_argument("--skip-decode", action="store_true", help="Inspect metadata without full decoding")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    if not args.input.is_file() or args.input.stat().st_size < 1024:
        errors.append("Input is missing or too small to be a valid delivery")
        print(json.dumps({"passed": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1

    try:
        ffmpeg = find_ffmpeg(args.ffmpeg)
        ffprobe = find_ffprobe(ffmpeg, args.ffprobe)
    except RuntimeError as error:
        print(json.dumps({"passed": False, "errors": [str(error)]}, ensure_ascii=False, indent=2))
        return 1

    try:
        metadata = inspect(ffprobe, args.input)
    except (RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"passed": False, "errors": [str(error)]}, ensure_ascii=False, indent=2))
        return 1
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

    color_expectations = {
        "pixelFormat": args.expect_pixel_format,
        "colorRange": args.expect_color_range,
        "colorSpace": args.expect_color_space,
        "colorTransfer": args.expect_color_transfer,
        "colorPrimaries": args.expect_color_primaries,
    }
    for field, expected in color_expectations.items():
        if expected and metadata.get(field) != expected:
            errors.append(f"Expected {field}={expected}, got {metadata.get(field)}")
    missing_color = [field for field in ["colorRange", "colorSpace", "colorTransfer", "colorPrimaries"] if not metadata.get(field)]
    if metadata["hasVideo"] and missing_color:
        message = "Missing video color metadata: " + ", ".join(missing_color)
        if args.require_color_tags:
            errors.append(message)
        else:
            warnings.append(message)

    loudness = None
    if args.measure_loudness or args.expect_lufs is not None or args.max_true_peak is not None:
        if not metadata["hasAudio"]:
            errors.append("Cannot measure loudness because no audio stream was detected")
        else:
            try:
                loudness = measure_loudness(ffmpeg, args.input)
            except RuntimeError as error:
                errors.append(str(error))
            if loudness:
                measured_lufs = loudness["integratedLufs"]
                measured_peak = loudness["truePeakDbfs"]
                if args.expect_lufs is not None and (measured_lufs is None or abs(measured_lufs - args.expect_lufs) > args.lufs_tolerance):
                    errors.append(f"Expected loudness {args.expect_lufs:.1f} LUFS ± {args.lufs_tolerance:.1f}, got {measured_lufs}")
                if args.max_true_peak is not None and (measured_peak is None or measured_peak > args.max_true_peak):
                    errors.append(f"Expected true peak <= {args.max_true_peak:.1f} dBFS, got {measured_peak}")

    decode_error = None
    if not args.skip_decode:
        result = subprocess.run([ffmpeg, "-hide_banner", "-v", "error", "-xerror", "-i", str(args.input), "-f", "null", os.devnull], capture_output=True, text=True, encoding="utf-8", errors="replace")
        if result.returncode != 0:
            decode_error = (result.stderr or result.stdout).strip()
            errors.append("Full decode failed")

    report = {
        "passed": not errors,
        "file": str(args.input),
        "sizeBytes": args.input.stat().st_size,
        "metadata": metadata,
        "loudness": loudness,
        "decodeError": decode_error,
        "warnings": warnings,
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
