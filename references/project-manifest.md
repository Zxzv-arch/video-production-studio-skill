# Project manifest

Use a JSON manifest for complex or repeatable projects. It is the bridge between transcription, editing, Remotion, an NLE, and delivery.

Prefer creating and updating the manifest through `scripts/video_project.py` for cross-agent projects. Its `project.json` adds workflow stage, gate, history, blockers, decisions, and next actions to the editorial fields below. Existing projects may adopt these fields without moving their media.

## Minimum structure

```json
{
  "project": "example",
  "version": 1,
  "sources": [
    {"id": "cam-a", "path": "media/cam-a.mp4", "role": "primary", "sha256": "optional"}
  ],
  "constraints": {
    "targetDurationSec": 60,
    "aspectRatios": ["16:9", "9:16"],
    "offlineOnly": true
  },
  "chapters": [
    {"id": "hook", "startMs": 0, "endMs": 4200, "purpose": "promise the outcome"}
  ],
  "edits": [
    {"sourceId": "cam-a", "sourceInMs": 800, "sourceOutMs": 4200, "timelineInMs": 0, "reason": "clean opening take"}
  ],
  "corrections": [
    {
      "id": "term-001",
      "sourceId": "cam-a",
      "sourceWordIndexes": [42, 43],
      "raw": "raw ASR tokens",
      "display": "verified display term",
      "confidence": 0.92,
      "basis": "product glossary or user confirmation",
      "status": "approved",
      "disclose": true
    }
  ],
  "visualBeats": [
    {"startMs": 1200, "endMs": 3600, "purpose": "demonstrate feature", "treatment": "ui-demo"}
  ],
  "assets": [
    {
      "id": "music-bed",
      "type": "music",
      "path": "assets/audio/music-bed.wav",
      "sourceUrl": "optional",
      "license": "user-provided or exact license identifier",
      "attribution": "required credit or empty",
      "licenseProof": "analysis/licenses/music-bed.txt",
      "usageConstraints": []
    }
  ],
  "deliverables": [
    {"id": "master", "width": 1920, "height": 1080, "fps": 30, "status": "planned"}
  ],
  "assumptions": [],
  "uncertainties": [],
  "workflow": {
    "stage": "visual-plan",
    "gate": "Map claims to purposeful visuals",
    "history": [],
    "nextActions": []
  },
  "artifacts": [],
  "blockers": []
}
```

## Rules

- Store paths relative to the project root when practical.
- Keep milliseconds for editorial time and frames for a specific rendered composition; record FPS whenever converting.
- Never overwrite the raw transcript with corrected captions.
- Give every raw word a stable index. Store display corrections in `corrections` with the affected source word indexes, original ASR text, replacement text, confidence, evidence/basis, review status, and disclosure flag.
- Apply only `approved` or `verified` corrections to ordinary display captions. Leave `needs-review` corrections unapplied unless the user explicitly requests a review render. Include applied corrections whose `disclose` value is true in the delivery notes.
- Record why content was removed when the decision may be revisited.
- Add a new manifest version or variant entry when timing changes materially.
- Track generated assets with prompt, provider/model, license or usage constraints, and whether they depict a real event.
- Track music, effects, stock, fonts, and generated media in `assets`; a local file without license provenance is not automatically cleared for publication.
- Update deliverable status only after the corresponding artifact exists and passes validation.

`scripts/build_edit_manifest.py` produces a deterministic starting manifest from SRT. Enrich it rather than treating its automatic chapters as final editorial structure.

After the EDL is approved, run `scripts/retime_captions.py` against the immutable word transcript and this manifest. It maps source time to output time, handles cut-boundary clipping and adjacent-boundary duplication, merges fragmented Latin/product tokens, applies reviewed display corrections, and emits karaoke-ready milliseconds plus frames. Do not retime already-retimed captions a second time.

For a word inside an edit segment, the canonical mapping is `outputMs = timelineInMs + (sourceMs - sourceInMs)`. In a single-source sequential cut this is equivalent to subtracting the removed duration before the word, but the segment formula remains correct for multiple sources, reordered clips, overlaps, and intentional replays. Clip or reject a word crossing an edit edge and surface that decision; never let a caption imply that an inaudible full word survived.
