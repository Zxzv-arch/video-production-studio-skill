# Focused Three.js and CAD demonstrations

Use this reference only when the explanation depends on shape, depth, rotation, assembly, internal structure, spatial hierarchy, or a physical mechanism. Three.js is an advanced Remotion scene type, not a decoration to apply to every sentence. Text-to-CAD is an optional upstream asset generator, not the renderer and not a default dependency.

## Activation gate

Use Three.js when at least one of these is true:

- the viewer must understand how parts fit, separate, rotate, fold, flow, or occupy space;
- a camera orbit, cutaway, exploded view, or depth cue communicates something a flat diagram cannot;
- an existing verified GLB/glTF model is important evidence;
- the product’s material, lighting, or spatial transformation is itself the subject;
- a data or system scene genuinely benefits from depth and occlusion.

Prefer Remotion SVG, Canvas, HTML, or recorded evidence when the same point is clearer in 2D. Do not use 3D for an ordinary definition, list, quote, software click, or decorative background.

## Pipeline

```text
spoken spatial claim
  → verified CAD/model or simple authored geometry
  → normalize scale, axes, origin, materials, and units
  → GLB/glTF or native Three.js primitives
  → @remotion/three scene driven by output frames
  → composite with presenter PiP, labels, captions, and sound
```

For a generated or converted model, retain the source prompt, generator, version, license, conversion settings, and validation notes in the project manifest.

## Remotion implementation contract

- Add `@remotion/three` with the same exact version as the project’s `remotion` packages.
- Use compatible exact versions of `three` and `@react-three/fiber`; do not mix arbitrary package versions.
- Wrap the 3D scene in `<ThreeCanvas width={width} height={height}>` and include intentional lighting.
- Drive rotation, camera, material, morph, and assembly state from `useCurrentFrame()` or values derived from it.
- Never use `useFrame()`, `requestAnimationFrame()`, wall-clock time, autonomous shader time, or unseeded randomness in a rendered scene.
- Any `<Sequence>` inside `<ThreeCanvas>` must use `layout="none"`.
- Keep captions and most explanatory text as ordinary 2D Remotion layers above the canvas for sharpness and layout control.
- Mount a 3D scene only for its relevant range. Premount enough frames to load assets, but do not keep an expensive invisible canvas alive across the whole composition.

For a model with built-in animation clips, sample the intended clip at deterministic composition time instead of letting an animation mixer advance from realtime delta values. Verify the same requested frame renders identically on repeated runs.

## Focused 3D visual grammar

Choose one spatial hero action per sentence:

- **Orbit:** move just enough to reveal an otherwise hidden relationship.
- **Explode:** separate components along meaningful axes, then hold with labels.
- **Assemble:** bring parts together in causal or procedural order.
- **Cutaway:** reveal internal structure with clipping, transparency, or a removed shell.
- **Highlight:** isolate one component through material, outline, light, or reduced opacity of other parts.
- **Flow:** trace a verified route through pipes, circuits, modules, or spatial nodes.
- **Compare:** keep camera, scale, and lighting matched between two models or states.
- **Measure:** show dimension lines, units, and a known reference; do not imply engineering precision from an unverified mesh.

Use the sequence `orient → spatial action → label/result → hold`. Avoid perpetual rotation, uncontrolled orbiting, excessive depth of field, and camera motion that competes with the presenter or captions.

## Presenter and sentence-reactive integration

In sentence-reactive mode, the required animated presentation for a spatial sentence may be a Three.js scene. The sentence still needs dynamic type and a presenter/PiP state, but those supporting tracks should reduce amplitude while the spatial action is the hero.

- Start with a short 2D label or keyword.
- Transfer the presenter to a stable PiP anchor.
- Run one spatial action synchronized to the relevant verb or noun.
- Add 2D anchored labels after the model settles.
- Hold the final camera and component state through the conclusion of the sentence.

Consecutive sentences about the same object should progressively update one mounted 3D scene rather than reload the model and reset the camera for every sentence.

## Text-to-CAD adapter

Text-to-CAD is justified only when the requested subject is mechanical, industrial, architectural, manufacturable, or dimensionally structured and no suitable verified model exists. Treat its output as a candidate asset.

Required checks before presenting generated CAD as evidence:

- units, overall dimensions, axes, origin, scale, and handedness;
- closed solids or intended open surfaces;
- part count, feature order, bores, fillets, clearances, and mating relationships;
- normals, self-intersections, non-manifold geometry, and conversion damage;
- whether the prompt actually specifies enough information for the claimed result;
- license and disclosure status.

If engineering correctness has not been independently verified, label the visual as a concept or illustrative reconstruction. Never claim manufacturability, tolerance, safety, performance, or exact fit based only on a generated model.

Prefer a generic adapter contract over coupling the Skill to one research repository:

```json
{
  "type": "generated-cad",
  "generator": "provider-or-local-tool",
  "prompt": "source prompt",
  "sourceFormat": "STEP",
  "renderFormat": "GLB",
  "units": "mm",
  "validation": {
    "geometry": "passed | failed | not-reviewed",
    "dimensions": "passed | failed | not-reviewed",
    "engineeringReview": "approved | illustrative-only"
  }
}
```

## Fallbacks

- No WebGL/GPU: render a turntable or key spatial states once and composite them as video or stills.
- No `@remotion/three`: use an SVG/isometric diagram with the same component relationships.
- No valid model: author simple primitives for an explicitly illustrative explanation.
- Text-to-CAD unavailable: use user-provided CAD, a licensed model, a verified technical drawing, or a labeled 2D reconstruction.
- Model too heavy: decimate a review proxy while preserving the original for the approved master path; document any topology or silhouette change.

Do not block the whole production because optional 3D is unavailable when a faithful 2D explanation remains possible.

## Performance budget

- Draft with simple materials, modest geometry, reduced raster scale, limited lights, and no expensive post-processing.
- Prefer GLB/glTF assets prepared once over parsing engineering CAD during every frame render.
- Reduce draw calls and texture sizes; avoid large transparent stacks and unnecessary realtime shadows.
- Keep camera and lighting deterministic. Cache converted models and browser/runtime setup.
- Benchmark one representative 3D sentence before committing the whole project to the treatment.

Promote to review only after the proxy proves camera, labels, PiP placement, and semantic timing. Use master-quality geometry and textures only when those details are visible and approved.

## QA

Render the orientation frame, peak spatial action, labeled result, and final hold. Check:

- deterministic repeat renders;
- no flicker, missing textures, clipping, z-fighting, or broken normals;
- correct camera framing at the delivery aspect ratio;
- legible component labels that do not intersect the model, presenter, or captions;
- physically and semantically correct assembly order;
- disclosed generated or reconstructed geometry;
- acceptable render time and a tested fallback.

The acceptance criterion is that 3D makes the relationship easier to understand than a flat scene. If it does not, remove it.
