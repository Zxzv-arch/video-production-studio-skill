# Complex video workflows

Use this reference when a request combines long-form editing, motion graphics, B-roll, multiple formats, or several source clips.

## Decompose by decisions, not software

Separate the project into five independently verifiable layers:

1. **Editorial:** what is kept, removed, reordered, and emphasized.
2. **Visual explanation:** what the viewer sees for each spoken claim.
3. **Sound:** dialogue repair, music, ambience, and punctuation effects.
4. **Graphics and captions:** brand system, motion language, accessibility.
5. **Delivery:** aspect ratios, codecs, loudness, filenames, and review artifacts.

Choose tools per layer. A typical local-first stack is Whisper for timestamps, FFmpeg for media operations, Remotion for content-driven animation, and an NLE for manual timeline refinement. An all-in-one editor is optional convenience, not a quality requirement.

## Complexity tiers

### Tier 1 — Single short clip

One source, one output, limited graphics. Work directly after inventory and transcription. Representative stills plus a full decode are normally sufficient.

### Tier 2 — Structured explainer

Several semantic beats, diagrams, UI mockups, B-roll, captions, music, and one or more aspect ratios. Create a manifest, preview at reduced resolution, and render from the source master.

### Tier 3 — Long-form or multi-source production

Many clips, speakers, camera angles, or derivative outputs. Use proxies, stable clip IDs, transcript provenance, explicit selects, a reusable timeline, and per-deliverable manifests. Do not encode all variants independently until the master edit is approved.

## Three-act information architecture

- **Hook:** show the problem, promise, or surprising outcome immediately.
- **Development:** alternate explanation and evidence. Every new claim receives a new visual state.
- **Payoff:** summarize what changed, show the result, and leave a clear next step.

For educational talking-head content, a useful rhythm is face → visual explanation → face → example → synthesis. Do not mechanically enforce shot durations when the speech cadence says otherwise.

## Iteration gates

1. **Paper edit:** transcript selections and structure.
2. **Rough cut:** timing and continuity; no expensive effects.
3. **Visual prototype:** representative motion and caption style.
4. **Fine cut:** final timing, graphics, B-roll, and sound design.
5. **Master:** color, mix, captions, and technical validation.
6. **Variants:** derive from the approved master and reframe intentionally.

At each gate, fix upstream problems before proceeding. Do not use motion graphics to disguise a weak structure or unclear transcript.
