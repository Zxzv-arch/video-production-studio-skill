# Content-driven Remotion and motion design

Use when the edit needs diagrams, UI demonstrations, kinetic typography, branded explainers, data-driven scenes, or reusable video templates.

## Map meaning to motion

For each transcript beat, record the claim, viewer takeaway, visual metaphor or evidence, hero element, timing, and whether the speaker remains visible.

Examples:

- A technology stack assembles from modules into a central system.
- A historical statement becomes a timeline, not a generic title.
- A commerce workflow becomes user → product → cart → payment.
- A numeric claim becomes a counter, comparison, or chart with its basis visible.
- A product feature becomes a UI state change or before/after demonstration.

## Composition structure

- Put each substantial scene in its own component.
- Keep one master composition for audio, global captions, progress, and scene sequencing.
- Drive every animation from the current frame. Do not use CSS keyframe animations, timers, or runtime randomness.
- Use deterministic seeded randomness for particles or ambient variation.
- Keep editable scene timing explicit and named.
- Premount media-bearing sequences when the framework supports it.
- Reference local assets through the project asset mechanism instead of absolute development-machine paths.

## Motion hierarchy

Each scene should have primary semantic motion, secondary connectors or reactions, and restrained ambient motion. Use decelerating entrances, accelerating exits, and springs only when the subject benefits from physical character. Limit simultaneous animation so the hero remains obvious.

## Talking-head integration

- Keep the face prominent during introductions, opinions, and trust-building statements.
- Shift, dim, crop, or place the speaker in picture-in-picture while diagrams carry technical explanations.
- Reintroduce the face after dense graphics to reset attention.
- Place captions in a protected layer above all graphics and verify the longest line.

## Rendering workflow

1. Confirm media compatibility; create H.264 proxies when browser decoding cannot handle the camera codec.
2. Render representative stills from every scene.
3. Render a low-resolution complete preview to inspect transitions and audio sync.
4. Correct warnings before the master render.
5. Render the master once, then derive delivery variants without unnecessary repeated compositing.

If an official Remotion skill is available, follow its current API guidance for project scaffolding, media components, captions, and rendering.
