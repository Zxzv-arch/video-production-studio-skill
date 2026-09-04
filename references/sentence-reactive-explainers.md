# Sentence-reactive talking-head explainers

Use this mode when the user explicitly wants every spoken sentence to receive dynamic typography, a corresponding presenter/PiP state, and a Remotion animated presentation or demonstration. This is a dense visual language. Preserve it as a deliberate project mode rather than silently imposing it on restrained interviews or documentary work.

“Animated PPT” here means a presentation-like Remotion scene: a title, visual argument, diagram, steps, comparison, evidence, or result animated directly on the video timeline. It does not require creating a `.pptx` file unless the user separately asks for an editable PowerPoint deliverable.

## Non-negotiable sentence contract

Segment the approved output transcript into complete semantic sentences. Every sentence cue must contain:

1. `startMs`, `endMs`, output frames, and source word indexes;
2. the complete sentence and one concise visual takeaway;
3. a dynamic text treatment for the sentence or its key phrase;
4. a presenter state: full, supporting, split, PiP, detail, or return;
5. a Remotion presentation/demo scene tied to the sentence meaning;
6. one hero action and a readable resolved state;
7. caption-safe regions and evidence provenance.

No sentence may be left as an unchanged talking-head shot merely because it is short. A brief connective sentence may use a restrained micro-slide, icon relationship, keyword transformation, or progress change, but it still changes visual state.

## Schedule shape

```ts
type SentenceCue = {
  id: string;
  startMs: number;
  endMs: number;
  from: number;
  durationInFrames: number;
  sourceWordIndexes: readonly number[];
  sentence: string;
  takeaway: string;
  presenterMode: 'speaker-full' | 'speaker-support' | 'demo-with-pip' | 'split' | 'demo-detail' | 'speaker-return';
  dynamicText: {
    phrase: string;
    treatment: 'letter-cascade' | 'keyword-pop' | 'underline' | 'counter' | 'token-assembly' | 'before-after';
  };
  slide: {
    kind: 'statement' | 'steps' | 'comparison' | 'diagram' | 'metric' | 'timeline' | 'real-demo';
    title: string;
    items: readonly string[];
    evidenceAsset?: string;
  };
  heroAction: string;
};
```

Use the output timeline from the edit manifest. Convert milliseconds to frames once with the project FPS. Do not rebuild sentence timing independently from phrase captions.

## Choreograph inside each sentence

The three tracks are required, but they should not all become heroes at once. Use this default internal order and adapt it to natural stress:

- **0–20%:** reveal or transform the important word or short phrase;
- **10–35%:** move the presenter toward the sentence’s PiP/split/supporting state;
- **25–75%:** animate the presentation, real demonstration, diagram, comparison, or metric;
- **65–90%:** reveal the visible result, conclusion, or causal connection;
- **final 10–25%:** hold the resolved state so it can be understood.

For a very short sentence, overlap supporting motions at lower amplitude rather than compressing three aggressive entrances. For a long compound sentence, split it into meaningful clauses only when the transcript and idea support separate visual events; do not invent punctuation that changes meaning.

## Map sentence meaning to animated presentation

| Sentence function | Dynamic type | Remotion PPT/demo scene |
| --- | --- | --- |
| Hook or promise | decisive letter cascade or keyword reveal | outcome card, visual thesis, or before/after preview |
| Definition | term builds and settles | term → attributes diagram with one active concept |
| Ordered instruction | action verb emphasis | numbered steps that activate with the spoken order |
| Cause and effect | cause/effect words highlighted | nodes and connector travel from cause to visible outcome |
| Comparison | changed word or delta emphasis | aligned before/after or two-column comparison |
| Numeric claim | verified number counter | chart, gauge, or measurement with unit and basis |
| Product action | command or control name reveal | real UI action, focused target, then changed state |
| Code/configuration | token or line emphasis | code diff, command assembly, output/result pane |
| Example | example label or proper noun | concrete scenario card, object, screenshot, or short clip |
| Timeline/history | date or milestone reveal | timeline travel to the relevant milestone |
| Spatial structure or assembly | component name or action verb | focused Three.js orbit, explode, assemble, cutaway, or flow scene governed by `threejs-and-cad.md` |
| Caveat/warning | restrained underline or color change | condition → risk → safe action diagram |
| Synthesis/CTA | key conclusion assembles | relationship recap, checklist, or next-step path |

If the sentence contains no verifiable external evidence, use an accurate diagram or presentation abstraction. Do not fabricate a product state, source, metric, or result to satisfy the “every sentence” rule.

## Dynamic text rules

- Animate the full short sentence only when it functions as a title or quotation. Otherwise animate the key phrase and leave captions readable.
- Keep punctuation and completed words stable after entrance.
- Rotate among a small approved family—letter cascade, mask reveal, underline, keyword scale, token assembly, or number change—based on meaning, not random variety.
- Preserve multilingual grapheme clusters and whole-word wrapping.
- Captions remain a separate global layer. Dynamic type may paraphrase the takeaway but must not obscure, replace, or contradict the verbatim caption.

## PiP rules for every sentence

Every sentence records a presenter layout, even when the box remains in the same position. Change crop, emphasis, anchor, or relative dominance only when it supports the sentence.

- Use `speaker-support` for trust, interpretation, warnings, and connective sentences with a quiet slide.
- Use `demo-with-pip` for procedures and proof.
- Use `split` for comparisons and interpretation beside evidence.
- Use `demo-detail` for dense interface, code, or exact measurements.
- Use `speaker-full` or `speaker-return` sparingly for emotional emphasis; pair it with an animated supporting presentation state when this dense mode is active.

Keep one continuous presenter media clock. Never restart the audible speaker for each sentence.

## Presentation component rules

Build each sentence presentation as a named scene or a typed scene record with stable states:

`intro → active element → result → hold`

Use slide kinds as reusable visual grammars, not repetitive templates. A steps slide should animate progress; a comparison should reveal aligned differences; a diagram should move causality; a metric should show a justified value; a real-demo slide should expose the action and changed state. A title plus three static bullets is not sufficient merely because the card moved onto the screen.

Use `<Sequence premountFor={...}>` for delayed or media-bearing scenes. Drive all states from frames. When Studio editability is required, keep sentence hero objects explicit and named, and register important scenes individually when useful.

## Density control

The project may satisfy every sentence without becoming visually exhausting:

- one hero action per sentence;
- alternate large and small visual changes;
- reuse spatial anchors and easing so the viewer learns the grammar;
- allow some sentences to update an existing slide instead of replacing the entire stage;
- use hard cuts or shared-element continuity more often than full decorative transitions;
- lower the amplitude of dynamic text while a real UI action or chart is the hero;
- keep at least one readable resolved state before moving on.

“Every sentence changes” does not mean “every sentence resets the entire composition.” Consecutive sentences about one idea should progressively update one coherent scene.

Three.js is never a per-sentence quota. Only spatial sentences use it; neighboring sentences should reuse the mounted model and update camera, emphasis, or assembly state instead of rebuilding the scene.

## QA

Validate the schedule before rendering: every sentence must have non-empty dynamic text, presenter mode, slide/demo kind, hero action, and source timing. Then render the beginning, hero action, and resolved state of every sentence plus a low-resolution complete review.

Reject a sentence when its animation is generic, unrelated to the words, smaller than legible delivery size, covered by PiP or captions, missing a visible result, or so busy that the viewer cannot tell which element is primary.
