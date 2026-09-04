# Talking-head demonstrations and scene choreography

Use this reference for presenter-led explanations, tutorials, reviews, training, product walkthroughs, and technical commentary where the audience should see both the speaker and concrete implementation or evidence.

The default visual promise is: **see the person, see the proof, understand the relationship**. Do not turn a talking-head video into uninterrupted face footage with decorative captions, and do not hide the speaker behind a full-screen slideshow for long stretches without a narrative reason.

When the demonstration and kinetic text must react at exact spoken moments, also use `realtime-content-animation.md`. It defines the shared semantic event track for presenter layout, evidence actions, dynamic words, and result feedback.

## Build a proof-led scene schedule

For every transcript beat, record:

- the claim or instruction;
- what the audience must understand or believe;
- the strongest available proof asset;
- the stage mode;
- speaker visibility and anchor;
- hero action and annotation target;
- entry/exit event, not just elapsed time;
- caption region and collision risks;
- source milliseconds plus composition frames.
- triggering source word indexes and the realtime motion event that fires at that phrase.

Use this evidence order:

1. a real screen recording, physical action, measured result, or before/after;
2. a verified screenshot, document excerpt, chart, or product state;
3. an accurate reconstruction clearly presented as an illustration;
4. a causal diagram or labeled abstraction;
5. generic B-roll only when it adds context or emotion rather than pretending to prove the claim.

Never fabricate a product state, metric, customer result, or implementation detail. Redact credentials and private data before a screen demonstration.

## Stage modes

| Mode | Use | Speaker | Demonstration |
| --- | --- | --- | --- |
| `speaker-full` | hook, opinion, framing, caveat, emotional emphasis | full or dominant | absent or quiet supporting graphic |
| `speaker-support` | one concise fact, label, quote, or object | dominant | card or object in secondary area |
| `demo-with-pip` | procedure, product feature, code, interface, physical demonstration | visible at roughly 24–34% of landscape width; somewhat larger in portrait | primary stage |
| `split` | comparison, cause/effect, speaker interpreting visible evidence | 35–48% of stage | remaining stage with shared baseline |
| `demo-detail` | small control, text, chart value, or exact implementation detail | small PiP or temporarily absent when density requires | cropped or magnified primary detail |
| `speaker-return` | synthesis, transition, warning, payoff, call to action | smoothly restored to dominant/full | recedes or resolves behind the speaker |

Do not mechanically cycle modes. Change state when the information state changes. A useful explanatory arc is `speaker-full → demo-with-pip → demo-detail or split → speaker-return`, but omit states that do not help the material.

## Continuous presenter architecture

Use four persistent layers in the master composition:

1. **Dialogue clock:** the edited presenter audio and source timing; it is the synchronization authority.
2. **Presenter stage:** one continuous visible presenter layer whose box, crop, corner radius, elevation, and anchor animate between schedule states.
3. **Evidence stage:** screen recording, product footage, diagram, screenshot, or comparison controlled by scene sequences.
4. **Global information layer:** captions, disclosure labels, progress, and accessibility-safe overlays above both stages.

Within the evidence and information layers, treat each spoken proof beat as an ordered micro-story: presenter transfer → evidence orientation → visible action → changed result → readable hold. Dynamic letters or keywords may support one of those phases, but must not compete with the proof or duplicate the caption line.

Avoid mounting a fresh audible presenter `<Video>` inside every scene. Repeated media instances can restart decoding, duplicate audio, create discontinuities, and make layout changes feel like cuts. Keep one audible presenter timeline where practical; make demonstration media muted unless its sound is intentionally mixed.

For a transcript-edited presenter made of multiple source segments, keep those segments in one explicit dialogue timeline. Drive layout from the output timeline after caption retiming, not from original source time.

## Picture-in-picture choreography

Treat PiP as a camera move, not a badge that suddenly appears.

- **Anticipate:** begin the presenter shrink or lateral shift a few frames before the demonstration becomes the semantic hero.
- **Transfer focus:** let the evidence stage brighten, sharpen, or expand as the presenter settles; avoid two equally forceful moves at the same instant.
- **Settle:** provide a short stable hold after the layout lands before animating a cursor, callout, or step.
- **Return:** resolve the current proof, then expand the presenter from the existing PiP position so spatial continuity is preserved.

At 30 fps, a professional starting range is roughly 12–20 frames for a layout transfer and 4–8 frames of visual settle. Serious or premium material may use 18–30 frames with little or no overshoot; energetic social material may use 8–15 frames with one restrained spring. Adjust to speech cadence and never cut through a word.

Landscape starting points:

- PiP width: about 24–34% of canvas;
- edge margin: about 5–8% of canvas;
- corner radius after shrink: about 2–4% of PiP width;
- keep eyes near the upper third inside the crop;
- use one consistent shadow direction and border treatment.

In portrait, test a top or upper-corner presenter crop above the caption region; a landscape PiP percentage cannot simply be copied. Switch anchor only when the current demonstration or captions need the occupied area. Animate across a meaningful path at a scene boundary instead of teleporting the window from corner to corner.

## Demonstration animation vocabulary

Choose one hero action for each proof beat:

- **Orient:** zoom from overview to the relevant region, then stop.
- **Act:** show the real cursor, tap, drag, code change, assembly step, or physical action.
- **Confirm:** highlight the changed state, checkmark, measured value, or before/after.
- **Explain:** add a short label, connector, mask, or causal arrow only after the real state is visible.
- **Compare:** lock both states to a shared baseline; animate a divider or matched crop rather than unrelated entrances.

Useful supporting animation includes a focus mask, magnified crop, cursor trail, numbered step chip, anchored annotation line, progress rail, data count, or diagram connector. Ambient motion may add depth but must not compete with the proof.

Avoid perpetual zooming, repeated bounce entrances, random glitch, full-frame spins, large animated blur, and motion on every word. Reserve a signature transition for a meaningful chapter or transformation.

## Remotion implementation pattern

- Put the scene schedule in a typed data module with `from`, `durationInFrames`, `mode`, claim, evidence asset, presenter anchor, and optional focus target.
- Add speech-linked semantic events for important keywords, steps, UI actions, diagram states, metrics, and results. Store event timing in output frames produced from the same word timestamps as captions.
- Keep the presenter layer mounted outside the per-scene `<Sequence>` elements. Derive its current and previous layout boxes from the active cue and interpolate between them with clamped frame-based easing.
- Put each major evidence scene in its own named component. Use `<Sequence premountFor={...}>` for media-bearing scenes; keep edit-critical timings explicit.
- Use `<Video>` and `<Audio>` from `@remotion/media`, local assets through `staticFile()`, and a muted evidence track unless its audio is intentionally used.
- Drive motion with `useCurrentFrame()`, `interpolate()`, and `Easing`; never use CSS transitions, keyframes, timers, or unseeded randomness.
- For Studio-editable hero objects, use descriptive names, inline interpolation, and individual `scale`, `translate`, and `rotate` properties. Keep complex scheduling data-driven only where that portability is more valuable than direct timeline editing.
- Keep captions as a global final layer. They must not resize, follow, or disappear with the PiP window.

Generate the bundled starter with:

```text
python scripts/bootstrap_remotion_project.py <project-directory> --template talking-head-demo
```

The starter renders without media by showing labeled placeholders. Replace its empty `speakerSrc` and `demoSrc` values with assets in `public/`, then replace the example cues and callouts with the approved transcript-linked schedule.

## Schedule schema

Store the portable editorial form in `project.json` or the edit manifest:

```json
{
  "id": "feature-demo",
  "startMs": 8200,
  "endMs": 15400,
  "sceneType": "demo-with-pip",
  "claim": "The presenter explains how the feature is configured",
  "purpose": "demonstrate",
  "evidenceAsset": "assets/demo/settings.mp4",
  "speaker": {"visible": true, "anchor": "top-right"},
  "focusTarget": {"x": 0.18, "y": 0.32, "width": 0.42, "height": 0.22},
  "heroAction": "cursor changes the setting and the result updates",
  "motionEvents": [
    {"kind": "keyword", "startMs": 8420, "endMs": 9200, "label": "configure", "sourceWordIndexes": [118]},
    {"kind": "ui-action", "startMs": 9360, "endMs": 10500, "label": "enable setting", "sourceWordIndexes": [121, 122]},
    {"kind": "result", "startMs": 10500, "endMs": 12300, "label": "setting enabled", "sourceWordIndexes": [123, 124]}
  ],
  "captionRegion": "bottom-safe"
}
```

Coordinates are normalized to the evidence stage, not the whole canvas. Convert milliseconds to frames once using the composition FPS and the same rounding convention as retimed captions. Reject overlaps or gaps that are not deliberate.

## Professional review gates

Render stills immediately before, during, and after every layout transfer, plus the peak of every demonstration action. Review the complete sequence for:

- continuous dialogue and lip sync through scene changes;
- stable face crop and eye line in every PiP anchor;
- evidence legibility at actual delivery size;
- visible action followed by an understandable result;
- no cursor, callout, face, or disclosure collision with captions;
- enough settled hold to read each demonstrated state;
- purposeful return to the speaker after dense evidence;
- consistent corner radius, elevation, motion direction, and easing;
- no private data, invented UI, or unlabeled reconstruction.

In `draft`, reduce raster size and expensive effects but preserve scene timing, layout geometry, and the presenter/evidence handoff. A draft that changes choreography cannot reliably approve the master.
