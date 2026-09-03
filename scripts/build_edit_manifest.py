#!/usr/bin/env python3
"""Create a deterministic starter edit manifest from an SRT file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


TIME_RE = re.compile(r"(?P<h>\d{2}):(?P<m>\d{2}):(?P<s>\d{2})[,.](?P<ms>\d{3})")


def to_ms(value: str) -> int:
    match = TIME_RE.fullmatch(value.strip())
    if not match:
        raise ValueError(f"Invalid SRT timestamp: {value}")
    parts = {key: int(number) for key, number in match.groupdict().items()}
    return ((parts["h"] * 60 + parts["m"]) * 60 + parts["s"]) * 1000 + parts["ms"]


def parse_srt(path: Path) -> list[dict]:
    blocks = re.split(r"\r?\n\s*\r?\n", path.read_text(encoding="utf-8-sig").strip())
    cues: list[dict] = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) < 2:
            continue
        timing_index = next((i for i, line in enumerate(lines) if "-->" in line), None)
        if timing_index is None:
            continue
        start_text, end_text = [part.strip() for part in lines[timing_index].split("-->", 1)]
        cues.append(
            {
                "id": f"caption-{len(cues) + 1:04}",
                "startMs": to_ms(start_text),
                "endMs": to_ms(end_text.split()[0]),
                "text": " ".join(lines[timing_index + 1 :]),
            }
        )
    if not cues:
        raise ValueError(f"No subtitle cues found in {path}")
    return cues


def build_chapters(cues: list[dict], gap_ms: int, max_ms: int) -> list[dict]:
    chapters: list[dict] = []
    start_index = 0
    for index in range(1, len(cues)):
        gap = cues[index]["startMs"] - cues[index - 1]["endMs"]
        duration = cues[index - 1]["endMs"] - cues[start_index]["startMs"]
        if gap >= gap_ms or duration >= max_ms:
            selected = cues[start_index:index]
            chapters.append({"id": f"chapter-{len(chapters)+1:02}", "startMs": selected[0]["startMs"], "endMs": selected[-1]["endMs"], "summary": selected[0]["text"], "status": "needs-editorial-review"})
            start_index = index
    selected = cues[start_index:]
    chapters.append({"id": f"chapter-{len(chapters)+1:02}", "startMs": selected[0]["startMs"], "endMs": selected[-1]["endMs"], "summary": selected[0]["text"], "status": "needs-editorial-review"})
    return chapters


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("srt", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--project", help="Project name; defaults to SRT stem")
    parser.add_argument("--source", help="Optional primary media path")
    parser.add_argument("--gap", type=float, default=1.2, help="Chapter break silence in seconds")
    parser.add_argument("--max-chapter", type=float, default=30.0, help="Maximum automatic chapter duration")
    parser.add_argument("--keyword", action="append", default=[], metavar="REGEX=TREATMENT", help="Repeatable semantic event rule")
    args = parser.parse_args()

    cues = parse_srt(args.srt)
    rules: list[tuple[re.Pattern, str]] = []
    for raw_rule in args.keyword:
        if "=" not in raw_rule:
            parser.error(f"Keyword must be REGEX=TREATMENT: {raw_rule}")
        pattern, treatment = raw_rule.split("=", 1)
        rules.append((re.compile(pattern, re.IGNORECASE), treatment))

    events = []
    for cue in cues:
        for pattern, treatment in rules:
            if pattern.search(cue["text"]):
                events.append({"startMs": cue["startMs"], "endMs": cue["endMs"], "captionId": cue["id"], "treatment": treatment, "status": "suggested"})

    manifest = {
        "project": args.project or args.srt.stem,
        "version": 1,
        "sources": ([{"id": "primary", "path": args.source, "role": "primary"}] if args.source else []),
        "constraints": {"offlineOnly": True, "aspectRatios": [], "targetDurationSec": None},
        "captions": cues,
        "chapters": build_chapters(cues, round(args.gap * 1000), round(args.max_chapter * 1000)),
        "visualBeats": events,
        "edits": [],
        "deliverables": [],
        "assumptions": [],
        "uncertainties": [],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "captions": len(cues), "chapters": len(manifest["chapters"]), "visualBeats": len(events)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
