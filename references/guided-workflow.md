# Guided cross-agent workflow

Use the project interface for work that is complex, resumable, or likely to move between Codex, OpenCode, Claude-compatible agents, an NLE, and Remotion. The interface is terminal-based and standard-library-only so it remains portable.

## Start

Interactive:

```text
python scripts/video_project.py init --project-root <project-directory> --source <video-file>
```

Non-interactive automation:

```text
python scripts/video_project.py init --non-interactive --project-root <project-directory> --source <video-file> --kind interview --audience "new customers" --target-duration 600 --aspect-ratio 16:9 --aspect-ratio 9:16 --caption-language zh --timeline both
```

The command creates folders and a `project.json` control file. It records source paths without copying or uploading the media. Initialization completes the intake gate and leaves the project at `inventory`.

## Resume contract

Every agent must:

1. Run `status` before editing.
2. Read `project.json`, then inspect only the files needed for the current stage.
3. Preserve `workflow.history`; append decisions instead of rewriting history.
4. Register every meaningful artifact with a path relative to the project root when possible.
5. Record uncertainties and blockers explicitly. Never infer that an absent artifact exists.
6. Leave `nextActions` concrete enough for an unfamiliar agent to continue without chat history.

```text
python scripts/video_project.py status --project-root <project-directory>
```

## Stage gates

| Stage | Required evidence before advancing |
|---|---|
| intake | source list and constraints |
| inventory | media inventory with stream, duration, dimensions, FPS, rotation, and audio data |
| transcript | raw transcript, word timestamps when dialogue-driven, and uncertainty notes |
| paper-edit | narrative outline plus keep/remove decisions or edit manifest |
| rough-cut | playable proxy or rough timeline |
| visual-plan | content-linked visual beats, B-roll plan, and motion purpose |
| preview | preview render plus representative review frames |
| fine-cut | approved timing in the source composition or editable timeline |
| finish | color, audio, captions, and export candidate |
| qa | full-decode report and visual/audio review notes |
| delivered | verified deliverables and handoff notes |

`advance` records an artifact and moves one stage at a time. It refuses to advance when no artifact is supplied. The agent must judge whether the supplied artifact actually satisfies the gate.

```text
python scripts/video_project.py advance --project-root <project-directory> --artifact analysis/media-inventory.json --note "Probed every source with ffprobe"
```

## Blockers

Use blockers only for conditions that require authority, private upload, payment, unavailable source material, or a story-changing decision.

```text
python scripts/video_project.py block --project-root <project-directory> --reason "Need pronunciation of the guest's surname"
python scripts/video_project.py unblock --project-root <project-directory> --index 1 --note "User confirmed pronunciation"
```

Do not advance to `delivered` while an open blocker exists.

## Human-friendly control surface

The terminal summary is the default interface. It shows the progress bar, current gate, registered artifacts, blockers, and next actions. Editors may also open `project.json` in a text editor, but scripts should perform state transitions to keep history consistent.

For a manual multi-track timeline, build the NLE project as described in `timeline-projects.md`, then register the project file as an artifact. For Remotion, keep source code and reusable graphics inside the guided project's `remotion/` directory and register the composition entry point.
