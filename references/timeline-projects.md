# Editable multi-track timelines

Use when the user wants to drag clips, refine cuts visually, collaborate with a human editor, or continue in an NLE.

## Decide whether a timeline is necessary

A scripted render is sufficient for deterministic graphics, templated explainers, and batch variants. Use a visual timeline when subjective timing, many alternate takes, multicam, detailed audio work, or frequent manual rearrangement dominates.

## Recommended track architecture

- V1: primary camera or screen recording
- V2: alternate angles and corrective punch-ins
- V3: B-roll and demonstrations
- V4: motion graphics and callouts
- V5: captions and accessibility graphics
- A1–A2: dialogue and alternate microphones
- A3: room tone or ambience
- A4: music
- A5: sound effects

Keep stable clip IDs and source timecodes. Never bake captions or graphics into an intermediate if the user expects to edit those layers later.

## Interchange

Prefer the target editor's native project when it is reliable. Otherwise use supported interchange such as XML, EDL, or OTIO, and include the source directory layout. Test a small round-trip before generating a large project because effects, speed ramps, nested sequences, and caption styling often do not translate perfectly.

Treat a native-editor integration as an optional adapter, not a prerequisite. Before writing a draft, detect the editor version, draft schema, target path, and adapter/library availability; inspect an existing harmless draft when possible. Clone templates before replacing assets and never overwrite an original draft. If the adapter is missing or unverified on the current platform, deliver the portable manifest, stable clip IDs, track map, captions, and a small interchange file instead of claiming a native project works.

For CapCut/Jianying-style drafts, keep captions, text, audio, effects, and video on separate editable tracks. Record any native asset identifiers separately from semantic intent so another editor or backend can substitute them. Headless export is an independent capability: verify it explicitly rather than assuming that draft generation implies export automation.

## Division of labor

Automation should handle transcription, selects, silence candidates, proxy creation, first assembly, caption timing, relinking metadata, and repeatable exports. The visual editor should handle subjective trims, performance choices, music feel, and finishing decisions that benefit from direct playback.

Chat-based editors are useful when transcript editing and a timeline must live in one interface. They are optional; a local NLE plus the manifest can provide equivalent editorial control without uploading footage.
