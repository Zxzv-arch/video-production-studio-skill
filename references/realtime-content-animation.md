# Realtime content animation for presenter-led video

Use this reference when spoken narration must continuously drive picture-in-picture, a product or process demonstration, kinetic words, diagrams, or visible result feedback. The goal is not constant movement. The goal is a precise chain: **the speaker names an idea, the relevant visual changes, and the result remains readable long enough to understand**.

## Build one semantic event track

Derive motion events from the approved word-timestamp transcript and edit manifest. Each event should identify:

- output-timeline `startMs` and `endMs`;
- source word indexes or caption token indexes that triggered it;
- semantic role: `keyword`, `step`, `ui-action`, `diagram-state`, `comparison`, `metric`, or `result`;
- visible target and evidence asset;
- presenter layout during the event;
- entrance, active state, readable hold, and exit;
- whether the event is factual evidence, an accurate reconstruction, or an illustration.

Run three synchronized visual tracks from that event data:

1. **Presenter track:** the same speaker layer moves between full frame, supporting frame, split view, and PiP.
2. **Evidence track:** the real screen, process, diagram, comparison, or result performs the action being described.
3. **Semantic typography track:** a small number of important words, letters, numbers, or labels reinforce the idea.

Captions are a fourth, global accessibility track. Do not turn every caption word into a second kinetic-title system.

When the user explicitly requests visual treatment for every sentence, use `sentence-reactive-explainers.md`. That mode requires a dynamic-text event, a presenter/PiP state, and an animated presentation or demonstration for every complete sentence while still sequencing the three tracks by attention priority.

## Convert speech time to frames once

Use the same output-timeline timestamps and rounding convention as captions:

`frame = round(milliseconds × fps / 1000)`

Do the conversion once when producing the scene or motion schedule. Do not independently subtract edit durations in React.

- Anticipate a major layout transfer by about 2–4 frames when it improves continuity without making the visual claim arrive before the spoken setup.
- Start a semantic emphasis at the spoken onset of its triggering word; let its visual peak land on that word or stressed syllable.
- After a UI action, reveal the changed state or result, then hold it. A click without a visible consequence is incomplete proof.
- Keep at least 4–8 stable frames between a PiP transfer and the first detailed evidence action at 30 fps, unless the cadence clearly requires overlap.
- Never cut or hide the evidence before the narration has finished referring to it.

## Dynamic words and letters

Use kinetic type selectively:

- **Keyword emphasis:** color, scale, underline, mask reveal, or a restrained spring on one important term.
- **Letter cascade:** a short title, acronym, product name, or transformation word assembles over 8–18 frames. The completed word must then hold.
- **Number motion:** count or roll toward a verified value; show the unit and basis.
- **Token assembly:** code, commands, formulas, or process labels join in the order being explained.
- **Type-on:** use only when typing, search, code entry, or composition is itself the meaning.
- **Before/after text:** keep both states aligned and animate the changed portion, not the whole frame.

Do not bounce every word, split ordinary subtitles into flying letters, or repeat the same reveal on every scene. A beat gets one hero motion and at most two supporting motions.

Segment text by grapheme cluster when possible. For CJK, emoji, combining marks, and multilingual copy, prefer `Intl.Segmenter(..., {granularity: 'grapheme'})`; `Array.from()` is an acceptable dependency-free fallback for Unicode code points. Never use `text.split('')`, which can break surrogate pairs. Preserve whitespace and punctuation in the settled state.

## Realtime demonstration vocabulary

Match the spoken intent to a visible action:

| Narration intent | Evidence action | Confirmation |
| --- | --- | --- |
| "Open" or "find" | cursor or focus moves to the real target | target gains a short focus ring or magnified crop |
| "Turn on" or "change" | toggle, selection, drag, form edit, or code diff | new state remains visible |
| "First / then / finally" | numbered steps activate sequentially | progress connector reaches the active step |
| "Compared with" | matched crops or aligned columns appear | changed field or delta is emphasized |
| "This causes" | diagram node activates and connector travels | dependent node changes state |
| numeric claim | chart bar, counter, or measured readout changes | final value, unit, and source remain readable |
| result or payoff | success state, output, before/after, or finished object appears | concise result label or checkmark resolves the beat |

Prefer real cursor and interface behavior captured in the source. Use synthetic cursors or reconstructed UI only when accurate, useful, and clearly labeled. Never animate a success state that the source does not establish.

## Remotion architecture

Keep the presenter mounted once outside per-scene sequences. Keep evidence media and scene graphics beneath a global caption layer. Store the schedule in typed data rather than scattering transcript timings through JSX.

An event shape may look like:

```ts
type MotionEvent = {
  id: string;
  at: number;
  durationInFrames: number;
  kind: 'keyword' | 'step' | 'ui-action' | 'diagram-state' | 'comparison' | 'metric' | 'result';
  label: string;
  target?: {x: number; y: number; width: number; height: number};
  sourceWordIndexes: readonly number[];
};
```

Drive every value with `useCurrentFrame()`, `interpolate()`, `Easing`, or a deterministic spring. Use `<Sequence premountFor={...}>` for media-bearing or delayed elements. Avoid CSS animation, timers, and unseeded randomness. Prefer opacity and individual `scale`, `translate`, and `rotate` properties; reserve expensive blur and filter animation for a short, meaningful beat.

The evidence scene should expose stable states—overview, target, action, result—so a reviewer can inspect them at exact frames. If the demonstration is an editable Studio deliverable, keep hero objects explicit and named rather than generating every edit-critical layer with `.map()`.

## Motion hierarchy and accessibility

- One hero action owns the eye at a time.
- The presenter transfer is the hero until it settles; the evidence action becomes hero next; the result state resolves the beat.
- Dynamic typography supports either the spoken concept or the evidence action, not both simultaneously at full amplitude.
- Keep captions in a protected bottom-safe region. Move PiP, labels, and step rails around the captions, never the reverse.
- Provide a lower-motion path: replace long travel with short fades, remove bounce, reduce scale range, and keep all meaning visible without motion.
- Preserve sufficient contrast and hold time at the actual delivery size.

## Review frames and acceptance

For each important beat, render and inspect:

1. the frame before the presenter begins moving;
2. the settled PiP/evidence layout;
3. the peak word or letter emphasis;
4. the evidence action;
5. the confirmed result;
6. the return to the presenter or next stable state.

Review the full sequence at normal speed. Reject the beat when the animation precedes the claim, the proof is too small, the speaker or label covers the action, typography duplicates captions, the result disappears too quickly, or an effect is unrelated to the spoken meaning.
