from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.retime_captions import apply_corrections, merge_latin_runs, normalize_edits, retime_words
from scripts.transcribe_local import caption_groups


class CaptionPipelineTests(unittest.TestCase):
    def test_caption_groups_do_not_split_latin_fragments(self) -> None:
        words = [
            {"text": " Note", "start": 0.0, "end": 0.2},
            {"text": "Com", "start": 0.2, "end": 0.35},
            {"text": "merce", "start": 0.35, "end": 0.6},
            {"text": " 很好。", "start": 0.6, "end": 1.0},
        ]
        groups = caption_groups(words, max_chars=6, max_duration=5.5)
        self.assertEqual(groups[0]["text"], "NoteCommerce")

    def test_retime_clips_and_deduplicates_boundary_word(self) -> None:
        words = [
            {
                "rawText": " hello",
                "sourceStartMs": 900,
                "sourceEndMs": 1100,
                "confidence": 0.9,
                "sourceId": "primary",
                "sourceWordIndexes": [0],
            }
        ]
        edits = normalize_edits(
            {
                "edits": [
                    {"sourceId": "primary", "sourceInMs": 0, "sourceOutMs": 1050, "timelineInMs": 0},
                    {"sourceId": "primary", "sourceInMs": 950, "sourceOutMs": 2000, "timelineInMs": 1050},
                ]
            }
        )
        retimed, dropped = retime_words(words, edits, min_overlap=0.25, dedupe_ms=80)
        self.assertEqual(len(retimed), 1)
        self.assertEqual(dropped[0]["reason"], "adjacent-edit-boundary-duplicate")

    def test_latin_fragments_and_approved_correction_collapse(self) -> None:
        base = {
            "sourceId": "primary",
            "confidence": 0.8,
            "editIndex": 0,
            "clipped": False,
        }
        words = [
            {**base, "text": " Note", "rawText": " Note", "startMs": 0, "endMs": 100, "sourceStartMs": 0, "sourceEndMs": 100, "sourceWordIndexes": [0]},
            {**base, "text": "|", "rawText": "|", "startMs": 100, "endMs": 110, "sourceStartMs": 100, "sourceEndMs": 110, "sourceWordIndexes": [1]},
            {**base, "text": "Com", "rawText": "Com", "startMs": 110, "endMs": 200, "sourceStartMs": 110, "sourceEndMs": 200, "sourceWordIndexes": [2]},
            {**base, "text": "merce", "rawText": "merce", "startMs": 200, "endMs": 300, "sourceStartMs": 200, "sourceEndMs": 300, "sourceWordIndexes": [3]},
        ]
        merged = merge_latin_runs(words, max_gap_ms=180)
        self.assertEqual(merged[0]["text"].strip(), "NoteCommerce")
        corrected, applied, rejected = apply_corrections(
            merged,
            [
                {
                    "id": "term-1",
                    "sourceWordIndexes": [0, 1, 2, 3],
                    "raw": "Note|Commerce",
                    "display": "nopCommerce",
                    "status": "approved",
                    "basis": "product glossary",
                }
            ],
            include_review=False,
        )
        self.assertEqual(corrected[0]["text"], "nopCommerce")
        self.assertEqual(applied[0]["id"], "term-1")
        self.assertEqual(rejected, [])

    def test_review_correction_is_not_silently_applied(self) -> None:
        word = {
            "text": " Core",
            "rawText": " Core",
            "startMs": 0,
            "endMs": 200,
            "sourceStartMs": 0,
            "sourceEndMs": 200,
            "sourceId": "primary",
            "sourceWordIndexes": [0],
            "confidence": 0.4,
            "editIndex": 0,
            "clipped": False,
        }
        corrected, applied, rejected = apply_corrections(
            [word],
            [{"sourceWordIndexes": [0], "raw": "Core", "display": ".NET Core", "status": "needs-review"}],
            include_review=False,
        )
        self.assertEqual(corrected[0]["text"], " Core")
        self.assertEqual(applied, [])
        self.assertEqual(rejected[0]["reason"], "review-required")

    def test_cli_emits_karaoke_shape_and_frames(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            words_path = root / "words.json"
            manifest_path = root / "manifest.json"
            output_path = root / "karaoke.json"
            words_path.write_text(
                json.dumps(
                    {
                        "words": [
                            {"index": 0, "sourceId": "primary", "text": " hello", "start": 1.0, "end": 1.3, "confidence": 0.95},
                            {"index": 1, "sourceId": "primary", "text": " world", "start": 1.35, "end": 1.7, "confidence": 0.9},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            manifest_path.write_text(
                json.dumps({"edits": [{"sourceId": "primary", "sourceInMs": 900, "sourceOutMs": 1800, "timelineInMs": 0}], "corrections": []}),
                encoding="utf-8",
            )
            script = Path(__file__).resolve().parents[1] / "scripts" / "retime_captions.py"
            result = subprocess.run(
                [sys.executable, str(script), str(words_path), str(manifest_path), str(output_path), "--fps", "30"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema"], "video-production-studio/karaoke-captions@1")
            self.assertEqual(payload["captions"][0]["startMs"], 100)
            self.assertEqual(payload["captions"][0]["startFrame"], 3)
            self.assertTrue(payload["captions"][-1]["pageBreakAfter"])


if __name__ == "__main__":
    unittest.main()
