#!/usr/bin/env python3
"""Transcribe media locally with Faster Whisper and emit reusable edit artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


LATINISH_RE = re.compile(r"^[A-Za-z0-9._+#@/&'|-]+$")


def caption_units(words: list[dict], max_join_gap: float = 0.18) -> list[dict]:
    """Merge ASR fragments that belong to one Latin/product token for grouping only."""
    units: list[dict] = []
    for original in words:
        item = dict(original)
        raw_text = str(item["text"])
        item["text"] = raw_text.replace("|", "")
        previous = units[-1] if units else None
        candidate = (str(previous["text"]) + item["text"]).strip() if previous else ""
        can_join = bool(
            previous
            and item["start"] - previous["end"] <= max_join_gap
            and not raw_text[:1].isspace()
            and candidate
            and LATINISH_RE.fullmatch(candidate)
        )
        if not can_join:
            if item["text"]:
                units.append(item)
            continue
        previous["text"] += item["text"]
        previous["end"] = max(previous["end"], item["end"])
    return units


def timestamp(seconds: float) -> str:
    millis = max(0, round(seconds * 1000))
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def caption_groups(words: list[dict], max_chars: int, max_duration: float) -> list[dict]:
    groups: list[dict] = []
    current: list[dict] = []
    punctuation = set("。！？!?；;：:")

    def flush() -> None:
        if not current:
            return
        groups.append(
            {
                "start": current[0]["start"],
                "end": current[-1]["end"],
                "text": "".join(item["text"] for item in current).strip(),
            }
        )
        current.clear()

    for word in caption_units(words):
        if current and word["start"] - current[-1]["end"] > 0.65:
            flush()
        current.append(word)
        text = "".join(item["text"] for item in current).strip()
        duration = current[-1]["end"] - current[0]["start"]
        if len(text) >= max_chars or duration >= max_duration or (text and text[-1] in punctuation):
            flush()
    flush()
    return [group for group in groups if group["text"]]


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Input audio or video file")
    parser.add_argument("--output-dir", type=Path, help="Output directory; defaults beside input")
    parser.add_argument("--model", default="small", help="Faster Whisper model name or local path")
    parser.add_argument("--language", default=None, help="Language code such as zh or en; auto-detect if omitted")
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda", "auto"])
    parser.add_argument("--compute-type", default="int8", help="For example int8, float16, or float32")
    parser.add_argument("--prompt", default=None, help="Optional terminology prompt")
    parser.add_argument("--source-id", default="primary", help="Stable source ID used by edit manifests")
    parser.add_argument("--max-caption-chars", type=int, default=28)
    parser.add_argument("--max-caption-duration", type=float, default=5.5)
    args = parser.parse_args()

    if not args.input.is_file():
        parser.error(f"Input file does not exist: {args.input}")

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("Install Faster Whisper first: python -m pip install faster-whisper", file=sys.stderr)
        return 2

    output_dir = args.output_dir or args.input.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = args.input.stem
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    segments, info = model.transcribe(
        str(args.input),
        language=args.language,
        initial_prompt=args.prompt,
        word_timestamps=True,
        vad_filter=True,
        condition_on_previous_text=True,
    )

    words: list[dict] = []
    raw_segments: list[dict] = []
    for segment_index, segment in enumerate(segments):
        raw_segments.append({"start": segment.start, "end": segment.end, "text": segment.text.strip()})
        for word in segment.words or []:
            if word.start is None or word.end is None:
                continue
            words.append(
                {
                    "index": len(words),
                    "sourceId": args.source_id,
                    "text": word.word,
                    "start": round(float(word.start), 3),
                    "end": round(float(word.end), 3),
                    "confidence": round(float(word.probability), 4),
                    "segment": segment_index,
                }
            )

    groups = caption_groups(words, args.max_caption_chars, args.max_caption_duration)
    transcript_path = output_dir / f"{stem}.transcript.txt"
    words_path = output_dir / f"{stem}.words.json"
    srt_path = output_dir / f"{stem}.captions.srt"

    transcript_path.write_text("\n".join(segment["text"] for segment in raw_segments), encoding="utf-8")
    words_path.write_text(
        json.dumps(
            {
                "source": str(args.input),
                "sourceId": args.source_id,
                "language": info.language,
                "languageProbability": info.language_probability,
                "duration": info.duration,
                "segments": raw_segments,
                "words": words,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    srt_path.write_text(
        "\n\n".join(
            f"{index}\n{timestamp(group['start'])} --> {timestamp(group['end'])}\n{group['text']}"
            for index, group in enumerate(groups, 1)
        )
        + "\n",
        encoding="utf-8",
    )

    print(json.dumps({"transcript": str(transcript_path), "words": str(words_path), "captions": str(srt_path), "wordCount": len(words)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
