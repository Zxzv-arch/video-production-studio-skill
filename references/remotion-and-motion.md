# Content-driven Remotion and motion design

Use when the edit needs diagrams, UI demonstrations, kinetic typography, branded explainers, data-driven scenes, or reusable video templates.

For a talking-head video in which the speaker must remain visible while real product, screen, process, or diagram evidence is demonstrated, also read `talking-head-demonstrations.md`. It defines the continuous-presenter architecture, picture-in-picture state changes, and semantic scene schedule.

This reference is self-contained for ordinary Remotion video production. Do not request a separate Remotion guidance skill. If an API is absent from the installed version or a current upgrade is explicitly requested, consult the installed package types or official Remotion documentation.

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

For a new blank project, use `npx create-video@latest --yes --blank --no-tailwind <project-name>` when its prerequisites and repository constraints are suitable. If scaffolding or Git integration is unavailable, use `python scripts/bootstrap_remotion_project.py <project-directory>` to write a pinned minimal project without Git. Add version-matched Remotion packages with `npx remotion add <package>` rather than manually mixing versions.

Put media in `public/` and resolve it with `staticFile()`. Import `<Video>` and `<Audio>` from `@remotion/media`. Use `<CanvasImage>` for still images when appropriate. Use `from`, `durationInFrames`, `trimBefore`, and `trimAfter` in frames; wrap components in `<Sequence>` when they do not expose the required timing props.

## Deterministic animation

- Drive animation from `useCurrentFrame()` and `useVideoConfig()` with `interpolate()`, `Easing.bezier()`, or `Easing.spring()`.
- Never use CSS transitions, CSS keyframes, Tailwind animation utilities, wall-clock timers, or unseeded runtime randomness for rendered motion.
- Clamp interpolation outside its intended range unless deliberate extrapolation is required.
- Prefer individual `scale`, `translate`, and `rotate` style properties. Keep editable interpolation calls and keyframes inline in the style prop when Studio editing matters.
- Use perceptual scale output when supported so linear numeric scaling appears visually even.

For a 1920×1080 composition, keep important text roughly 80 px from the sides and 100 px from the top and bottom. A main headline generally needs about 84 px or more and supporting text about 44 px or more; scale these guides with the output size and actual viewing distance.

## Editable timelines and scenes

Put each substantial scene in a separate component and source file. For independently positioned clips, author each `<Video>` as its own JSX node with explicit `from`, `durationInFrames`, and `trimBefore`. For ripple editing, use explicitly authored `<TransitionSeries.Sequence>` nodes so changing one duration shifts later clips.

Do not generate Studio-editable clips or scenes with `.map()`. Keep timings as literal frame values where editability matters, add useful names, and optionally register individual scenes as compositions so an editor can open them directly.

Use `TransitionSeries.Transition` for overlap transitions and `TransitionSeries.Overlay` for an effect placed over a cut. A transition shortens total duration by its overlap; an overlay does not. Calculate and register the master duration accordingly. Do not place two overlays together or directly beside a transition.

## Motion hierarchy

Each scene should have primary semantic motion, secondary connectors or reactions, and restrained ambient motion. Use decelerating entrances, accelerating exits, and springs only when the subject benefits from physical character. Limit simultaneous animation so the hero remains obvious.

Typical timing ranges are 100–250 ms for light feedback, 200–400 ms for cards and interface state changes, 400–700 ms for premium scene motion, and 600–1200 ms for a deliberate reveal. These are starting points. The spoken beat and emotional weight decide the final timing.

Define a project motion identity with one dominant personality, one signature easing family, and a small duration palette. Adapt density to the subject: financial, healthcare, and enterprise explanations generally need restrained motion; entertainment and gaming can carry greater amplitude and faster timing.

Provide a lower-motion treatment when large zooms, rapid direction changes, full-frame spins, multi-layer parallax, or persistent loops could cause discomfort. Replace spatial travel with shorter fades, remove spring bounce, reduce simultaneous motion, and never communicate essential meaning through movement alone. For render performance, favor opacity and transforms, stagger expensive layers, and keep filters, animated shadows, and large blur regions limited.

## Talking-head integration

- Keep the face prominent during introductions, opinions, and trust-building statements.
- Keep one continuous presenter/media clock across layout changes when possible. Shift, dim, crop, or place that same layer in picture-in-picture while demonstrations carry technical explanations; do not restart the presenter clip merely because the visual scene changed.
- Reintroduce the face after dense graphics to reset attention.
- Place captions in a protected layer above all graphics and verify the longest line.
- Author a frame-based scene schedule with explicit `speaker-full`, `demo-with-pip`, `split`, `demo-detail`, and `speaker-return` states. Scene changes follow claims and demonstration events, not a decorative timer.

## Caption implementation

Keep rendering captions in JSON records compatible with this shape:

```ts
type Caption = {
  text: string;
  startMs: number;
  endMs: number;
  timestampMs: number | null;
  confidence: number | null;
  pageBreakAfter?: boolean;
};
```

Use `@remotion/captions` to parse SRT or group word captions into readable pages. Load caption JSON or SRT with `staticFile()` and hold rendering with `useDelayRender()` until parsing completes. Convert page milliseconds to frames with the composition FPS, render each page in a `<Sequence>`, preserve intentional whitespace, and compute the active word from absolute caption time. Keep caption rendering in its own component above the visual content.

After dialogue edits are locked, generate the caption data from source words plus the EDL:

```text
python scripts/retime_captions.py <words.json> <edit-manifest.json> <captions.karaoke.json> --fps <composition-fps>
```

Use its output-timeline milliseconds and frames directly. Do not subtract removed durations again inside React. Align scene boundaries with the same `round(milliseconds × fps / 1000)` convention. Applied display corrections retain source word indexes and must remain in the delivery disclosure chain.

## Audio and embedded video

Layer audio with explicit `<Audio>` nodes. Delay with `<Sequence>`, trim in frames, and use a frame-relative `volume` callback for fades or ducking. Use `playbackRate` only within the media component's supported range. Pitch processing may differ between Studio preview and server render, so verify the rendered output when pitch is changed.

For embedded footage, set sizing and `objectFit` deliberately. Use proxies when the browser cannot decode the camera codec reliably; keep source in/out decisions in the edit manifest so the final can return to original-quality media.

For HEVC, 10-bit, HDR, variable-frame-rate, or camera formats that preview unreliably, choose the intermediate deliberately:

- Use a CFR H.264/AAC mezzanine for SDR browser compatibility when one high-quality extra generation is acceptable. A slow `libx264` encode around CRF 14–18 is a practical starting range, not a lossless guarantee; preserve resolution, timing, and intended color conversion explicitly.
- Do not collapse HDR or critical 10-bit material to ordinary 8-bit H.264 without an approved tone-map or quality tradeoff. Prefer a compatible 10-bit or intraframe mezzanine, or return to the source for finishing.
- A final may derive from the H.264 mezzanine only when original decoding is unreliable, the mezzanine was created once at high quality, color was verified, and the quality cost is recorded. Avoid proxy-of-proxy generations.

## Rendering workflow

1. Confirm media compatibility; create an appropriate proxy or mezzanine when browser decoding cannot handle the camera codec.
2. Run `npx remotion browser ensure` before the first unattended render. It verifies a usable browser and may download Chrome Headless Shell; record this network/storage side effect and use `--browser-executable` when an approved existing browser is required.
3. Render representative stills at the title state, the middle of every scene, aggressive crops/punch-ins, caption extremes, and every return to a talking head.
4. Render a low-resolution complete preview to inspect transitions and audio sync.
5. Correct warnings before the master render.
6. Render the master once, then derive delivery variants without unnecessary repeated compositing.
7. Probe pixel format and color range/space/transfer/primaries, and compare representative pixels against the approved preview. Chromium/Remotion does not guarantee one universal tag combination. Remux or retag only when the pixels are already correct and the existing metadata is demonstrably wrong; otherwise perform an explicit color conversion.

Use `npx remotion studio --no-open` for interactive preview, `npx remotion still <composition-id> --frame <n>` for representative frame checks, and `npx remotion render <composition-id> <output>` for requested output. Rendering authorization follows the user's requested deliverable; opening Studio alone is not proof that the composition renders.

For a new presenter-led project, the bundled no-Git scaffold can generate a working layout starter:

```text
python scripts/bootstrap_remotion_project.py <project-directory> --template talking-head-demo
```
