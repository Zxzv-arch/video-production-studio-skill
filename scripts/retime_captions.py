#!/usr/bin/env python3
"""Retime word captions through an edit manifest and emit karaoke-ready JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


LATINISH_RE = re.compile(r"^[A-Za-z0-9._+#@/&'|-]+$")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def word_ms(word: dict[str, Any], key: str) -> int:
    ms_key = f"{key}Ms"
    if ms_key in word:
        return round(float(word[ms_key]))
    if key in word:
        return round(float(word[key]) * 1000)
    raise ValueError(f"Word is missing {key!r} or {ms_key!r}: {word}")


def normalize_words(payload: Any, default_source_id: str) -> list[dict[str, Any]]:
    raw_words = payload.get("words") if isinstance(payload, dict) else payload
    if not isinstance(raw_words, list):
        raise ValueError("Words JSON must be a list or an object containing a 'words' list")
    words: list[dict[str, Any]] = []
    for index, item in enumerate(raw_words):
        if not isinstance(item, dict) or "text" not in item:
            raise ValueError(f"Invalid word at index {index}")
        start_ms = word_ms(item, "start")
        end_ms = word_ms(item, "end")
        if end_ms < start_ms:
            raise ValueError(f"Word end precedes start at index {index}")
        words.append(
            {
                "rawText": str(item["text"]),
                "sourceStartMs": start_ms,
                "sourceEndMs": end_ms,
                "confidence": item.get("confidence"),
                "sourceId": str(item.get("sourceId", default_source_id)),
                "sourceWordIndexes": [int(item.get("index", index))],
            }
        )
    return words


def normalize_edits(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    raw_edits = manifest.get("edits")
    if not isinstance(raw_edits, list) or not raw_edits:
        raise ValueError("Edit manifest needs a non-empty 'edits' list")
    edits: list[dict[str, Any]] = []
    rolling_timeline_ms = 0
    for index, item in enumerate(raw_edits):
        if not isinstance(item, dict):
            raise ValueError(f"Invalid edit at index {index}")
        try:
            source_in = round(float(item["sourceInMs"]))
            source_out = round(float(item["sourceOutMs"]))
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"Edit {index} needs numeric sourceInMs/sourceOutMs") from error
        if source_out <= source_in:
            raise ValueError(f"Edit {index} has a non-positive source duration")
        timeline_in = round(float(item.get("timelineInMs", rolling_timeline_ms)))
        edits.append(
            {
                "index": index,
                "sourceId": str(item.get("sourceId", "primary")),
                "sourceInMs": source_in,
                "sourceOutMs": source_out,
                "timelineInMs": timeline_in,
            }
        )
        rolling_timeline_ms = max(rolling_timeline_ms, timeline_in + source_out - source_in)
    return sorted(edits, key=lambda edit: (edit["timelineInMs"], edit["index"]))


def retime_words(
    words: list[dict[str, Any]], edits: list[dict[str, Any]], min_overlap: float, dedupe_ms: int
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    output: list[dict[str, Any]] = []
    dropped: list[dict[str, Any]] = []
    for edit in edits:
        for word in words:
            if word["sourceId"] != edit["sourceId"]:
                continue
            overlap_start = max(word["sourceStartMs"], edit["sourceInMs"])
            overlap_end = min(word["sourceEndMs"], edit["sourceOutMs"])
            if overlap_end <= overlap_start:
                continue
            duration = max(1, word["sourceEndMs"] - word["sourceStartMs"])
            overlap_ratio = (overlap_end - overlap_start) / duration
            if overlap_ratio < min_overlap:
                dropped.append(
                    {
                        "reason": "cut-boundary-overlap-below-threshold",
                        "text": word["rawText"],
                        "sourceWordIndexes": word["sourceWordIndexes"],
                        "overlapRatio": round(overlap_ratio, 4),
                    }
                )
                continue
            output.append(
                {
                    **word,
                    "text": word["rawText"],
                    "startMs": edit["timelineInMs"] + overlap_start - edit["sourceInMs"],
                    "endMs": edit["timelineInMs"] + overlap_end - edit["sourceInMs"],
                    "editIndex": edit["index"],
                    "clipped": overlap_start != word["sourceStartMs"] or overlap_end != word["sourceEndMs"],
                }
            )

    output.sort(key=lambda item: (item["startMs"], item["endMs"], item["editIndex"]))
    deduped: list[dict[str, Any]] = []
    last_by_source_word: dict[tuple[str, int], int] = {}
    for item in output:
        key = (item["sourceId"], item["sourceWordIndexes"][0])
        previous_index = last_by_source_word.get(key)
        previous = deduped[previous_index] if previous_index is not None else None
        if previous is not None and item["startMs"] <= previous["endMs"] + dedupe_ms:
            previous_duration = previous["endMs"] - previous["startMs"]
            item_duration = item["endMs"] - item["startMs"]
            rejected = previous if item_duration > previous_duration else item
            if item_duration > previous_duration:
                deduped[previous_index] = item
            dropped.append(
                {
                    "reason": "adjacent-edit-boundary-duplicate",
                    "text": rejected["rawText"],
                    "sourceWordIndexes": rejected["sourceWordIndexes"],
                    "editIndex": rejected["editIndex"],
                }
            )
            continue
        deduped.append(item)
        last_by_source_word[key] = len(deduped) - 1
    return deduped, dropped


def clean_latin_text(value: str) -> str:
    return value.replace("|", "")


def is_latinish(value: str) -> bool:
    stripped = value.strip()
    return bool(stripped) and bool(LATINISH_RE.fullmatch(stripped))


def merge_latin_runs(words: list[dict[str, Any]], max_gap_ms: int) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    for item in words:
        current = dict(item)
        current["text"] = clean_latin_text(current["text"])
        previous = merged[-1] if merged else None
        raw_current = item["rawText"]
        can_join = bool(
            previous
            and previous["sourceId"] == current["sourceId"]
            and current["sourceWordIndexes"][0] == previous["sourceWordIndexes"][-1] + 1
            and current["startMs"] - previous["endMs"] <= max_gap_ms
            and not raw_current[:1].isspace()
            and is_latinish(previous["text"] + clean_latin_text(raw_current))
        )
        if not can_join:
            merged.append(current)
            continue
        previous["text"] += clean_latin_text(raw_current)
        previous["rawText"] += raw_current
        previous["endMs"] = max(previous["endMs"], current["endMs"])
        previous["sourceEndMs"] = max(previous["sourceEndMs"], current["sourceEndMs"])
        previous["sourceWordIndexes"].extend(current["sourceWordIndexes"])
        confidences = [value for value in [previous.get("confidence"), current.get("confidence")] if value is not None]
        previous["confidence"] = min(confidences) if confidences else None
        previous["clipped"] = previous["clipped"] or current["clipped"]
    return [item for item in merged if item["text"]]


def match_text(value: str) -> str:
    return re.sub(r"[\s|]+", "", value).casefold()


def apply_corrections(
    words: list[dict[str, Any]], corrections: list[dict[str, Any]], include_review: bool
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    applied: list[dict[str, Any]] = []
    not_applied: list[dict[str, Any]] = []
    output = list(words)
    allowed_statuses = {"approved", "verified"}
    if include_review:
        allowed_statuses.add("needs-review")

    for correction_index, correction in enumerate(corrections):
        correction_id = str(correction.get("id", f"correction-{correction_index + 1:04}"))
        status = str(correction.get("status", "needs-review"))
        indexes = correction.get("sourceWordIndexes")
        display = correction.get("display")
        if status not in allowed_statuses:
            not_applied.append({"id": correction_id, "reason": "review-required", "status": status})
            continue
        if not isinstance(indexes, list) or not indexes or not isinstance(display, str) or not display:
            not_applied.append({"id": correction_id, "reason": "missing-sourceWordIndexes-or-display"})
            continue
        wanted = {int(index) for index in indexes}
        correction_source = correction.get("sourceId")
        positions = [
            position
            for position, item in enumerate(output)
            if wanted.intersection(item["sourceWordIndexes"])
            and (correction_source is None or item["sourceId"] == str(correction_source))
        ]
        if not positions or positions != list(range(positions[0], positions[-1] + 1)):
            not_applied.append({"id": correction_id, "reason": "words-not-contiguous-on-output-timeline"})
            continue
        selected = output[positions[0] : positions[-1] + 1]
        found = {index for item in selected for index in item["sourceWordIndexes"]}
        if found != wanted:
            not_applied.append({"id": correction_id, "reason": "word-index-set-mismatch"})
            continue
        raw = "".join(item["rawText"] for item in selected)
        expected_raw = correction.get("raw")
        if isinstance(expected_raw, str) and match_text(raw) != match_text(expected_raw):
            not_applied.append({"id": correction_id, "reason": "raw-text-mismatch", "observedRaw": raw})
            continue
        confidences = [item.get("confidence") for item in selected if item.get("confidence") is not None]
        replacement = {
            **selected[0],
            "text": display,
            "rawText": raw,
            "startMs": selected[0]["startMs"],
            "endMs": selected[-1]["endMs"],
            "sourceStartMs": min(item["sourceStartMs"] for item in selected),
            "sourceEndMs": max(item["sourceEndMs"] for item in selected),
            "sourceWordIndexes": sorted(found),
            "confidence": min(confidences) if confidences else correction.get("confidence"),
            "correctionId": correction_id,
            "correctionStatus": status,
        }
        output[positions[0] : positions[-1] + 1] = [replacement]
        applied.append(
            {
                "id": correction_id,
                "raw": raw,
                "display": display,
                "sourceWordIndexes": sorted(found),
                "confidence": correction.get("confidence"),
                "status": status,
                "basis": correction.get("basis"),
                "disclose": bool(correction.get("disclose", True)),
            }
        )
    return output, applied, not_applied


def frame_for(ms: int, fps: float) -> int:
    return round(ms * fps / 1000)


def page_captions(words: list[dict[str, Any]], max_chars: int, max_duration_ms: int, max_gap_ms: int) -> list[dict[str, Any]]:
    pages: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []

    def flush() -> None:
        if not current:
            return
        current[-1]["pageBreakAfter"] = True
        pages.append(
            {
                "id": f"page-{len(pages) + 1:04}",
                "startMs": current[0]["startMs"],
                "endMs": current[-1]["endMs"],
                "text": "".join(item["text"] for item in current).strip(),
                "captionIndexes": [item["captionIndex"] for item in current],
            }
        )
        current.clear()

    for item in words:
        proposed_text = "".join(part["text"] for part in [*current, item]).strip()
        proposed_duration = item["endMs"] - (current[0]["startMs"] if current else item["startMs"])
        gap = item["startMs"] - current[-1]["endMs"] if current else 0
        if current and (len(proposed_text) > max_chars or proposed_duration > max_duration_ms or gap > max_gap_ms):
            flush()
        current.append(item)
    flush()
    return pages


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("words", type=Path, help="Word JSON from transcribe_local.py")
    parser.add_argument("manifest", type=Path, help="Edit manifest containing sourceInMs/sourceOutMs/timelineInMs edits")
    parser.add_argument("output", type=Path)
    parser.add_argument("--fps", type=float, default=30.0)
    parser.add_argument("--source-id", default="primary", help="Default source ID for words without sourceId")
    parser.add_argument("--min-word-overlap", type=float, default=0.6)
    parser.add_argument("--boundary-dedupe-ms", type=int, default=80)
    parser.add_argument("--latin-join-gap-ms", type=int, default=180)
    parser.add_argument("--max-page-chars", type=int, default=28)
    parser.add_argument("--max-page-duration", type=float, default=2.8)
    parser.add_argument("--max-page-gap", type=float, default=0.65)
    parser.add_argument("--include-review-corrections", action="store_true")
    args = parser.parse_args()

    if args.fps <= 0 or not 0 < args.min_word_overlap <= 1:
        parser.error("--fps must be positive and --min-word-overlap must be within (0, 1]")
    try:
        words_payload = load_json(args.words)
        manifest = load_json(args.manifest)
        if not isinstance(manifest, dict):
            raise ValueError("Edit manifest must be a JSON object")
        words = normalize_words(words_payload, args.source_id)
        edits = normalize_edits(manifest)
        retimed, dropped = retime_words(words, edits, args.min_word_overlap, args.boundary_dedupe_ms)
        merged = merge_latin_runs(retimed, args.latin_join_gap_ms)
        corrections = manifest.get("corrections", [])
        if not isinstance(corrections, list):
            raise ValueError("Manifest 'corrections' must be a list")
        corrected, applied, not_applied = apply_corrections(merged, corrections, args.include_review_corrections)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))

    captions: list[dict[str, Any]] = []
    for index, item in enumerate(corrected):
        start_ms = int(item["startMs"])
        end_ms = int(item["endMs"])
        captions.append(
            {
                "captionIndex": index,
                "text": item["text"],
                "startMs": start_ms,
                "endMs": end_ms,
                "timestampMs": start_ms,
                "startFrame": frame_for(start_ms, args.fps),
                "endFrame": max(frame_for(end_ms, args.fps), frame_for(start_ms, args.fps) + 1),
                "confidence": item.get("confidence"),
                "sourceId": item["sourceId"],
                "sourceWordIndexes": item["sourceWordIndexes"],
                "clipped": item["clipped"],
                **({"correctionId": item["correctionId"]} if item.get("correctionId") else {}),
                **({"correctionStatus": item["correctionStatus"]} if item.get("correctionStatus") else {}),
            }
        )
    pages = page_captions(
        captions,
        args.max_page_chars,
        round(args.max_page_duration * 1000),
        round(args.max_page_gap * 1000),
    )
    output = {
        "schema": "video-production-studio/karaoke-captions@1",
        "fps": args.fps,
        "timelineDurationMs": max((edit["timelineInMs"] + edit["sourceOutMs"] - edit["sourceInMs"] for edit in edits), default=0),
        "captions": captions,
        "pages": pages,
        "correctionsApplied": applied,
        "correctionsNotApplied": not_applied,
        "droppedAtCuts": dropped,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "captions": len(captions),
                "pages": len(pages),
                "correctionsApplied": len(applied),
                "droppedAtCuts": len(dropped),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
