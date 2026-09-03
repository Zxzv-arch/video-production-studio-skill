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
  "visualBeats": [
    {"startMs": 1200, "endMs": 3600, "purpose": "demonstrate feature", "treatment": "ui-demo"}
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
- Record why content was removed when the decision may be revisited.
- Add a new manifest version or variant entry when timing changes materially.
- Track generated assets with prompt, provider/model, license or usage constraints, and whether they depict a real event.
- Update deliverable status only after the corresponding artifact exists and passes validation.

`scripts/build_edit_manifest.py` produces a deterministic starting manifest from SRT. Enrich it rather than treating its automatic chapters as final editorial structure.
