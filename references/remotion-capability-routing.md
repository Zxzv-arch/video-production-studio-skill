# Remotion capability routing

Use this reference before implementing a substantial Remotion composition. Its purpose is to turn the editorial plan into the strongest appropriate set of Remotion capabilities, rather than defaulting to static cards, generic zooms, and ordinary subtitles.

If the user explicitly requires every spoken sentence to receive dynamic typography, PiP, and an animated presentation/demo, also apply `sentence-reactive-explainers.md` and validate sentence coverage before rendering.

Remotion is the deterministic composition and orchestration layer. It can coordinate edited media, a continuous presenter, evidence scenes, captions, audio, data, and reusable variants on one frame-accurate timeline. FFmpeg, an NLE, browser capture, or a specialist animation engine may prepare assets, but the final visual logic should remain explainable and reproducible.

## Run a capability design pass

For every important narrative beat, write down:

1. the spoken claim or viewer question;
2. the best proof or explanatory asset;
3. the visual state before, during, and after the beat;
4. the Remotion capability that makes the relationship clearest;
5. the exact transcript event that triggers it;
6. the lowest-cost faithful preview and the final-fidelity requirement.

Do not begin by choosing an effect. Begin with the information change. Select only capabilities that materially clarify, prove, compare, locate, demonstrate, or emotionally support it.

## Capability map

| Content need | Preferred Remotion treatment | Avoid |
| --- | --- | --- |
| Presenter explains real proof | one continuous presenter layer, animated PiP or split layout, evidence stage, global captions | restarting the presenter in every scene or hiding the face for an arbitrary slideshow |
| Product or process walkthrough | embedded demonstration video, focus crop, cursor/action event, state confirmation, step rail | fake interface actions or a highlight with no visible result |
| Important term or product name | kinetic keyword, grapheme-safe letter reveal, underline/highlight, settled readable state | animating every subtitle word or breaking multilingual text with `split('')` |
| Sequence or causal process | typed event schedule, nodes and connectors activated in spoken order | all nodes entering together or unrelated decorative arrows |
| Comparison | matched crops, shared baseline, animated divider, changed fields, persistent labels | unrelated card entrances that make visual comparison harder |
| Verified metric | counter, chart, progress, delta, unit and source label | an unreferenced number animation or misleading chart scale |
| Code or configuration | token assembly, typed command only when typing is meaningful, code diff, focused line, output/result | tiny full-screen code, decorative terminal noise, invented output |
| Timeline or history | frame-linked timeline with semantic milestones and controlled camera travel | using one generic title per date with no spatial relationship |
| Geography | static or animated map, route, marker, region highlight, evidence label | a map when location is not part of the explanation |
| Audio or speech analysis | waveform, spectrum, transcript emphasis, beat or phoneme-linked motion | audio-reactive decoration unrelated to the message |
| Brand illustration | SVG, Canvas, Lottie, or deterministic shape animation | rasterizing editable vector work too early |
| Spatial product or system | restrained Three.js/3D only when depth or assembly is the idea | adding 3D merely to look expensive |
| Scene change | hard cut by default; a short transition or overlay when the semantic relationship benefits | a different transition for every scene |
| Reusable versions | parameterized props, schema validation, calculated metadata, aspect-aware layout tokens | duplicating an entire composition for each copy or platform |
| Human-editable delivery | named scene components, explicit hero layers, inline keyframes, Studio-interactive elements | hiding edit-critical layers and timings inside opaque generators |

## Composition stack

A professional presenter-led master normally contains:

1. **Dialogue timeline:** the synchronization authority and edited source mapping.
2. **Presenter layer:** mounted continuously; crop and layout respond to scene state.
3. **Evidence layer:** screen, product, process, comparison, diagram, chart, map, code, or generated illustration.
4. **Semantic motion layer:** focus targets, connectors, counters, step states, highlights, and kinetic keywords.
5. **Caption and disclosure layer:** globally protected above changing layouts.
6. **Audio design layer:** dialogue, room tone, music, and restrained event sounds with ducking.
7. **Finishing layer:** global color treatment, vignette or texture when justified, progress, and delivery-safe overlays.

Keep substantial scenes in named components and keep their editorial timing explicit. Use one master composition to synchronize them. Mount media early enough to avoid decode stalls, but do not keep invisible expensive scenes active without need.

## Use the broader Remotion surface deliberately

- Use frame-driven interpolation or deterministic springs for spatial motion; never depend on CSS animation, wall-clock time, or unseeded randomness.
- Use media components for video and audio, local asset resolution for project files, and explicit trims and sequence timing.
- Use transition series when an overlap transition changes scene duration; use an overlay when the effect should not change timing.
- Use caption JSON as data and keep active-word timing on the edited output timeline.
- Use annotations, SVG paths, masks, and rough/highlight treatments when they explain a target; keep finished text readable after the draw-on phase.
- Use Lottie, canvas, shaders, or 3D only when the intended look or subject needs them and the target renderer has been tested.
- Use audio visualization only when audio itself is evidence or structure.
- Use parameters and metadata calculation for variants whose copy, dimensions, duration, or data changes.
- Structure hero elements for Studio editing when the user needs a visual timeline or manual refinement.

An agent may consult an already available specialist Skill or authoritative package documentation for a complex capability. Do not make that external Skill a runtime requirement, ask the user to install it merely for guidance, or leave essential behavior undocumented. Incorporate the generalized decision and implementation constraints into the project and retain a self-contained fallback.

## Choose another engine when it is better

Remotion should orchestrate the video, not monopolize every operation.

- Use **FFmpeg** for probing, stream-safe trims, silence analysis, proxies/mezzanines, loudness work, codec conversion, and final validation.
- Use a **graphical NLE** when the requested deliverable depends on manual multitrack dragging, collaboration conventions, or a native project file.
- Use **Manim or a mathematical plotting system** for dense symbolic derivations that would be harder to verify in general React markup.
- Use **Blender or a dedicated 3D pipeline** for physically complex camera, lighting, simulation, or photoreal spatial work; render a controlled asset for Remotion to composite.
- Use **SVG/Lottie or an illustration tool** for authored vector character or brand animation, then preserve deterministic timing in the final composition.
- Use **browser capture** for real UI behavior when authentic interaction is stronger evidence than a reconstruction.

Record the choice and fallback in the manifest. If a specialist component is absent, degrade the treatment while preserving the same meaning—for example, use an SVG system diagram instead of 3D, a focus crop instead of a shader, or a verified screen recording instead of reconstructed UI.

## Motion budget

Each beat gets one hero action, up to two supporting reactions, and restrained ambient motion. A useful order is:

`anticipate → transfer focus → act → confirm → hold → resolve`

The presenter-to-PiP move is the hero until it settles. The proof action becomes hero next. Kinetic type supports the claim at lower amplitude. Event sound punctuates only a meaningful state change. Do not run several full-strength animation systems at once merely because Remotion can render them.

Establish one motion personality, one main easing family, a small duration palette, consistent radius/elevation rules, and an aspect-aware safe-area system. Provide a lower-motion treatment when large travel, parallax, rapid scale, or looping effects are used.

## Performance and verification

- Build a low-cost draft with the same frames, crops, layout geometry, and semantic events as the master.
- Cache transcription, proxies, browser downloads, bundles, and unchanged generated assets.
- Prefer transforms and opacity; limit large blur, filter, shadow, shader, particle, and 3D workloads.
- Render representative states before a full preview: scene entrance, PiP settled state, action, result, longest caption, and return to presenter.
- Type-check the project, render at least one still and one short transition/action range, then inspect the complete review at normal speed.
- Confirm that missing media, fonts, packages, or browser capabilities produce a clear fallback rather than a plausible-looking broken render.

The acceptance test is not “many effects are present.” It is that the viewer can follow the speaker, see the implementation or proof at the right moment, understand the result, and still edit or reproduce the composition.
