---
name: video-production-studio
description: Self-contained production for professional talking-head explainers and other complex local videos, including transcript-driven edits, animated speaker-to-demo layouts, picture-in-picture choreography, real product or process demonstrations, Remotion scenes, captions, mixing, timelines, and multi-platform delivery. Use for substantial video creation or revision; do not use for simple playback, metadata lookup, or a one-off codec conversion with no editorial decisions.
license: Apache-2.0
metadata:
  self-contained: "true"
  required-agent-skills: "none"
---

# Video Production Studio

Turn source media into a verified, editable video package. The primary presentation pattern is a professional talking-head explanation that alternates visible speaker presence with concrete demonstrations and evidence. Treat spoken meaning and narrative purpose as the timing source; effects are not decoration.

## Self-contained capability contract

This folder contains the editorial and Remotion guidance required for the workflow. Do not tell the user to install, load, or invoke another video-editing or Remotion guidance skill. Do not pause merely because another agent skill is unavailable. Read the routed references in this folder and continue.

Execution software is different from an agent skill: FFmpeg is needed for many media operations, Python packages may be needed for local transcription, and Node.js plus Remotion are needed to render a Remotion composition. Detect these with `python scripts/video_project.py doctor`; use an available equivalent or report the exact missing executable only when the current deliverable truly depends on it. Doctor may show platform-specific bootstrap commands, but never run them without authorization to install local software.

Run `doctor --project-root <dir> --write --json` before choosing an engine. Read [references/environment-fallbacks.md](references/environment-fallbacks.md) when a required executable, package, GPU, GUI editor, browser, or network connection is absent. Continue with a lower-capability route when it still satisfies the deliverable; never pretend an unavailable component ran.

## Start or resume a guided project

For any request that combines two or more production disciplines, spans multiple sessions, or may be handed to another AI, read [references/guided-workflow.md](references/guided-workflow.md) first.

- Start a project with `python scripts/video_project.py init --project-root <dir> --source <media>`. Omit optional arguments in a terminal to use the interactive wizard.
- Resume by running `python scripts/video_project.py status --project-root <dir>` before making editorial changes.
- Persist stage, artifacts, assumptions, decisions, blockers, and next actions in `project.json`. Chat history is never the source of truth.
- Advance a stage only after its gate artifacts exist. Use `python scripts/video_project.py advance --project-root <dir> --artifact <path> --note <decision>`.
- A graphical NLE may be used for manual timeline work, but the manifest remains the portable handoff contract.

## Operating contract

- Preserve originals. Write intermediates and exports to clearly named new paths.
- Work locally by default. Do not upload footage, create accounts, spend credits, publish, or install a cloud service unless the user authorizes that action.
- Inspect duration, streams, frame rate, dimensions, rotation, color tags, and audio before designing the edit.
- Cache transcripts and derived media. Reuse them while the source hash and transcription settings are unchanged.
- Select a render mode before generating media. Default to `draft` while timing or motion is changing, promote to `review` for full-sequence approval, and use `master` only for an explicit final candidate or when full fidelity is required to judge the work.
- Never cut through a word. Pad ASR boundaries by 30–120 ms when accuracy is uncertain, and add short audio fades at every edit boundary.
- Keep dialogue intelligible above music and effects. Apply captions after visual overlays.
- Verify the final file by full decode plus visual samples. For substantial edits, watch or inspect the complete result at normal speed before declaring completion.
- Distinguish factual transcription from editorial rewriting. Mark uncertain names, numbers, and product terms for review instead of silently inventing corrections.

## Route the request

Choose only the references needed for the current job:

- Long interviews, podcasts, filler removal, silence tightening, speaker-based edits: read [references/transcript-editing.md](references/transcript-editing.md).
- Cut selection, pacing, transitions, color, sound, captions, speed changes, and compositing: read [references/editorial-craft.md](references/editorial-craft.md).
- Content-driven explainers, kinetic typography, diagrams, UI demonstrations, or Remotion: read [references/remotion-and-motion.md](references/remotion-and-motion.md).
- Talking-head explainers that combine a visible speaker with screen recordings, product proof, diagrams, animated picture-in-picture, or semantic scene scheduling: read [references/talking-head-demonstrations.md](references/talking-head-demonstrations.md), [references/realtime-content-animation.md](references/realtime-content-animation.md), and [references/remotion-and-motion.md](references/remotion-and-motion.md).
- Product demos, cinematic shot planning, camera language, styleframes, or screen-capture storytelling: read [references/shot-direction.md](references/shot-direction.md).
- B-roll planning, generated visuals, highlight extraction, or multiple short versions: read [references/broll-and-variants.md](references/broll-and-variants.md).
- Long-form-to-short-form selection, vertical reframing, candidate scoring, or batch social clips: read [references/shortform-selection.md](references/shortform-selection.md).
- Energetic social edits, karaoke captions, punch-ins, title/progress treatments, or fast talking-head/diagram switching: read [references/short-form-pop.md](references/short-form-pop.md).
- A user-editable multi-track timeline or interchange with an NLE: read [references/timeline-projects.md](references/timeline-projects.md).
- Missing or uncertain software, GPU, fonts, browser, NLE, ASR, network, or disk capacity: read [references/environment-fallbacks.md](references/environment-fallbacks.md).
- Complex projects combining several modes: read [references/complex-workflows.md](references/complex-workflows.md) and maintain the manifest described in [references/project-manifest.md](references/project-manifest.md).
- Cross-agent handoff, first-time setup, resumable work, or step-by-step guidance: read [references/guided-workflow.md](references/guided-workflow.md).
- Render cost, preview fidelity, caching, Remotion concurrency, or deciding between draft/review/master: read [references/render-modes.md](references/render-modes.md).
- Color, sound, subtitles, codecs, delivery, and quality control: read [references/finishing-and-qa.md](references/finishing-and-qa.md).
- Music selection, licensing records, cue maps, dialogue ducking, or sound-effect design: read [references/music-and-sound.md](references/music-and-sound.md).

## Default execution shape

1. Initialize or resume the guided project. Inventory source material and constraints: audience, destination, aspect ratios, target duration, must-keep moments, privacy, login/network limits, and delivery format. Select and record the current render mode; use `draft` when approval state is unknown. Infer low-risk defaults instead of blocking.
2. Transcribe speech with word timestamps when dialogue drives the cut. Use `scripts/transcribe_local.py` when Faster Whisper is available.
3. Build a semantic outline: hook, setup, development, proof, payoff, and call to action. Map each spoken claim to one visual purpose.
   For a talking-head explainer, also build one speech-linked event schedule that drives the presenter layout, evidence state, and selective semantic typography. Keep the speaker visible for trust and interpretation; give the main stage to real demonstrations or evidence when the words describe a concrete action or result.
4. Create an edit manifest before heavy rendering. Use `scripts/build_edit_manifest.py` to seed timings from SRT, then enrich it with editorial decisions.
5. After edit timing is approved, generate output-timeline word captions with `scripts/retime_captions.py`; keep raw word timing immutable and corrections disclosed.
6. In `draft`, render representative stills or short ranges before a complete low-resolution preview. Correct timing, hierarchy, caption placement, and motion language before promotion.
7. Promote to `review` for a complete sequence. Promote to `master` only after timing and motion are approved, unless full fidelity is necessary for an earlier color, codec, or effects decision. Render the master from original-quality media when possible and avoid repeatedly encoding the same pixels.
8. Finish audio and color in `master`, export the requested variants, and run `scripts/validate_delivery.py` on every final file. Do not pay master-level finishing and full-decode costs for disposable drafts.
9. Record validation reports, final paths, applied caption corrections, licensing notes, and unresolved uncertainties before advancing the workflow to `delivered`.

## Editorial decision rules

- A visual must clarify, prove, contrast, locate, demonstrate, or emotionally support the current line. If it does none of these, remove it.
- Change visual state when the information state changes, not on a fixed timer. Use the six-second attention rule only as a diagnostic.
- Prefer clean cuts and purposeful reframing. Reserve glitch, zoom, flash, and whip effects for semantic impacts or chapter changes.
- Maintain one hero action per beat. Supporting and ambient motion must remain subordinate.
- For talking heads, alternate trust-building face time with diagrams, UI, examples, and B-roll. Do not cover the face or captions with persistent graphics.
- Prefer visible implementation over decorative motion: when the speaker explains a step, feature, comparison, or result, show the corresponding real screen, object, process, or clearly labeled reconstruction. Use animated picture-in-picture to preserve speaker continuity while the evidence becomes primary.
- Synchronize PiP, demonstration actions, and dynamic words to the same output-timeline transcript events. Animate only important concepts, actions, and verified values; ordinary spoken subtitles remain the readable global caption layer.
- For generated B-roll, disclose uncertainty and avoid presenting synthetic imagery as documentary evidence.

## Deliverables

Unless the user asks for only one file, leave a coherent package:

- final video and requested platform variants;
- editable project or source composition when one was created;
- captions/transcript and an edit manifest;
- a contact sheet or representative review frames;
- a concise note listing assumptions, uncertain transcript terms, and verification performed.

Stop and request direction only when a missing choice would materially change the story, incur cost, upload private media, publish externally, or overwrite valuable work.
