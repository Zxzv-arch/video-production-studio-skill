# Render modes and performance budget

Use render modes to separate editorial iteration from delivery fidelity. A mode controls render scope, media fidelity, finishing, and validation effort; it must not silently change words, edit decisions, animation timing, safe areas, or the intended story.

## Select the narrowest sufficient mode

| Mode | Use when | Typical media and raster | Validation boundary |
| --- | --- | --- | --- |
| `draft` | Timing, layout, caption treatment, or motion language is still changing | Representative stills or short ranges first; then a low-resolution preview, commonly no more than 720p or about half scale; approved proxies are acceptable | Decode the rendered range, inspect its critical frames, and check sync around edited boundaries; defer final loudness and exhaustive delivery checks |
| `review` | A stakeholder or agent must judge the complete sequence | Complete timeline at an economical review resolution; use a stable proxy or mezzanine when original browser decoding is costly | Decode the complete preview, inspect every distinct scene and caption extreme, and review beginning-to-end continuity and sync; clearly label it non-final |
| `master` | The user requested a final candidate, or full fidelity is necessary to judge color, codec, fine texture, transparency, or a hardware-specific effect | Requested resolution, FPS, codec, color path, final captions, and original-quality media or an approved high-quality mezzanine | Run final audio finishing, full decode, metadata/color/loudness checks, representative visual inspection, and `validate_delivery.py` |

Default to `draft` when the approval state is unknown. Move to `review` after the edit structure and principal motion are coherent. Move to `master` after timing, captions, graphics, and music cues are approved. A user may explicitly request any mode; record why an early master was necessary.

For a guided project, set the mode with:

```text
python scripts/video_project.py render-mode --project-root <project-directory> --set draft --note "Testing caption placement"
python scripts/video_project.py render-mode --project-root <project-directory> --set review --note "Full sequence ready for approval"
python scripts/video_project.py render-mode --project-root <project-directory> --set master --note "Timing and motion approved"
```

The command records the transition in `project.json`. Render mode and workflow stage are related but independent: a short master-quality color test can occur before `finish`, and a `preview`-stage artifact is not automatically master quality.

## Preserve comparability across modes

- Keep composition FPS, edit points, animation frame timing, caption timing, fonts, and safe areas identical between draft and master unless the review is specifically testing an alternative.
- Prefer output scaling or a deliberate proxy switch over a separate simplified composition. If expensive effects must be approximated in draft, mark them visibly and list what the master restores.
- Burn a small `DRAFT` or `REVIEW` label into non-final stakeholder files when they could be mistaken for delivery media. Do not put that label into a master composition branch that could leak into final export.
- Never approve color, fine gradients, noise, text rasterization, or compression quality from a reduced-resolution draft.

## Cache and invalidation

Reuse work only when its inputs are still valid. Record or derive cache keys for:

- source path plus hash, size, and modification time;
- transcription model, language, VAD settings, and source audio hash;
- edit-manifest version or hash;
- caption corrections and retiming inputs;
- composition source, props, fonts, and referenced asset hashes;
- proxy/mezzanine codec, resolution, frame rate, and color transform.

A caption style change should not trigger transcription. A music gain change should not regenerate proxies. A timing change invalidates retimed captions and downstream renders, but not the raw word transcript. Never create a proxy from another proxy.

## Estimate before an expensive render

Before the first full `review` or any `master`:

1. Calculate total frames as duration multiplied by FPS and list every separately composited output.
2. Render a representative 5–10 second range containing video decode, captions, and the heaviest visual effect.
3. Record elapsed time, frames per second, peak memory if available, resolution, codec, and concurrency in `renderPlan.benchmarks` or the project decisions.
4. Extrapolate a range rather than promising an exact completion time. Include additional passes for encoding, loudness, validation, and platform variants.
5. If the estimate is unreasonable, reduce draft scale, optimize the expensive scene, render validated chunks, or ask about a deadline-versus-fidelity tradeoff before starting the master.

For repeated Remotion renders, use `npx remotion benchmark` on a representative range to compare concurrency values. More workers can be slower when they contend for RAM, video decoding, GPU resources, or storage. Preserve the fastest stable setting in the project rather than assuming all CPU threads are optimal.

## Avoid unnecessary rerenders

- Render stills and short frame ranges while debugging one scene.
- Bundle once and reuse the bundle or cache when inputs are unchanged.
- Use the performant current Remotion media component for embedded video; avoid multiplying simultaneous decoders without a visual reason.
- Limit large animated blur regions, filters, shadows, gradients, Canvas, WebGL, and motion blur in drafts. Precompute invariant heavy visuals when that preserves quality and transparency needs.
- Generate a single high-quality master, then derive codec-only, bitrate-only, audio-only, thumbnail, or simple scale variants with FFmpeg when no layout or timing changes. Recompose aspect-ratio variants whose framing or safe areas differ.
- Run exhaustive full-decode and loudness validation on final candidates, not on every disposable experiment. Still decode every rendered draft range before trusting its review result.

## Cold-start costs

Treat dependency installation, Remotion bundling, browser acquisition, model download, font download, and first proxy generation as setup work. Perform authorized setup once, preserve the caches, and report cold-start time separately from steady-state render time. Never hide a network download inside an unexplained render stall.
