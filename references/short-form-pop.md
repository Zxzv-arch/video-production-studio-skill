# Energetic short-form visual language

Use when the user asks for an energetic, playful, high-retention, or "cool" social edit. This is a controlled style system, not permission to decorate every beat. Preserve comprehension, face visibility, caption safety, and brand tone.

## Establish a style contract

Choose one dominant motion personality and a small token set before rendering:

- one neutral caption color, one active color, and at most two semantic highlight colors;
- one primary typeface plus an optional display face;
- three motion durations: quick feedback around 100–180 ms, ordinary moves around 200–350 ms, and major reveals around 400–650 ms;
- one spring character for active words or punch-ins;
- one recurring transition motif and one sound family.

Do not mix random zooms, glitches, colors, and type treatments. High energy comes from precise timing and contrast between active and quiet moments.

## Karaoke captions

Drive state from word timestamps on the edited output timeline:

- **spoken:** full opacity in the neutral color;
- **active:** accent color plus a short scale or weight emphasis, typically 1.04–1.12× with a controlled spring;
- **future:** lower contrast but still readable, commonly 35–65% opacity;
- **semantic highlight:** reserve separate colors for categories such as product terms, measured numbers, warnings, or outcomes. Keep the category mapping stable.

Group words by syntax and breath, not only character count. Keep one or two lines, protect the face, and test the longest page on the smallest output. Active animation must settle quickly enough that the current word is readable rather than wobbling through its entire spoken interval.

Generate the output-timeline word JSON with:

```text
python scripts/retime_captions.py transcripts/source.words.json analysis/edit-manifest.json remotion/public/captions.karaoke.json --fps 30
```

The flat `captions` array follows the Remotion caption timing shape and includes frame boundaries, source word indexes, page breaks, cut clipping, and disclosed display corrections.

## Punch-ins and fast-cut camera language

- Use a punch-in to mark a new claim, hide a justified dialogue compression, or increase emphasis—not at a fixed interval.
- A normal talking-head change is often 1.00→1.04–1.08×. Reserve 1.10–1.15× for a rare impact after checking crop quality and face room.
- For an opening settle, a modest overscale can return to 1.00× over roughly 300–600 ms.
- Snap the main visual change to the cut or emphasized word. Let spring overshoot occur after the information boundary, not before it.
- Alternate scale, crop, composition, and graphics so repeated cuts do not create mechanical breathing or visible resolution loss.

## Title, progress, and edge treatment

- Keep the title card brief enough to preserve the hook, usually 0.5–1.5 seconds unless it carries necessary context.
- Scale typography to the output instead of hard-coding one raster. For 1080×1920, a main hook often begins around 72–120 px and supporting text around 36–56 px, then adjusts for font metrics and viewing distance.
- Keep essential text inside roughly 6–8% horizontal and 8–12% top safe margins. Reserve the lower interface/caption zone required by the target platform; do not assume every platform uses the same overlay footprint.
- Use a progress bar only when duration or chapter position helps orientation. Keep it thin, low contrast, and outside the caption/face regions.
- Vignette, grain, glow, and chromatic effects are finishing accents. Check skin, text edges, gradients, and compression after they are applied.

## Talking head → PiP → diagram scheduling

Map the information state before choosing the layout:

| Spoken purpose | Preferred visual state |
|---|---|
| personal claim, opinion, trust, setup | face prominent |
| mechanism, sequence, comparison | diagram or UI becomes hero; speaker may move to PiP |
| evidence, screenshot, example | evidence is readable; speaker supports rather than covers it |
| reaction, conclusion, call to action | return to face or a clean result frame |

Every transition needs an anchor in the transcript or edit manifest. Convert time with `frame = round(milliseconds × fps / 1000)` and use one convention throughout the composition. Align scene boundaries to `timelineInMs` edit boundaries or verified word starts. If a Remotion overlap transition shortens the master duration, account for the overlap once in the scene schedule; do not retime captions independently a second time.

Render stills at the title state, the middle of every distinct scene, each return to the speaker, and any aggressive punch-in. Then render a complete low-resolution preview to judge whether the energy pattern breathes.
