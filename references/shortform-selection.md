# Long-form to short-form selection

Use for turning interviews, podcasts, courses, screen recordings, or long videos into Shorts, Reels, TikTok clips, teasers, or several candidate versions.

## Candidate generation

Read the full transcript before selecting. Generate overlapping candidates rather than locking the first plausible excerpt. A candidate should normally contain a hook, enough setup to stand alone, a development or proof beat, and a payoff.

Score each candidate from 0–100 using weighted dimensions:

- hook strength: 30%;
- standalone coherence: 25%;
- emotional intensity or curiosity: 20%;
- value density: 15%;
- payoff quality: 10%.

Also record context risk, factual sensitivity, available visuals, clean boundary confidence, duration, and whether the excerpt misrepresents the speaker. Reject misleading fragments regardless of score.

Present a ranked shortlist with source time, duration, hook, score, rationale, and proposed crop. If the user requested autonomous batch generation, record selection criteria and continue; otherwise obtain selection before expensive renders.

## Boundary snapping

1. Start at a sentence or clause boundary near the chosen hook.
2. End at a complete payoff; extend to the next sentence boundary when the extension is small and useful.
3. Snap to word timestamps, then check nearby silence or low-energy audio.
4. Add a small post-word tail and short audio fades; preserve natural room tone.
5. Inspect face and gesture continuity. Hide unavoidable jump cuts with a motivated reframe or insert.
6. Report the delta between proposed and snapped boundaries.

Do not rely on stream-copy extraction for frame-accurate boundaries: keyframe placement can shift the actual cut. Use it only for quick proxies when the offset is measured and acceptable; re-encode exact delivery cuts or use a frame-accurate composition.

## Content-aware reframing

- **Talking head:** track or keyframe the face within a protected center region; leave caption space and avoid nervous micro-panning.
- **Screen recording:** use a framed layout or authored camera moves toward the active UI area; preserve enough context to understand location.
- **Podcast/multispeaker:** switch or compose speakers according to the active voice; verify diarization around overlap and laughter.
- **Demonstration/action:** follow the hands, object, cursor, or result rather than a fixed center crop.

Automatic center crop is only a draft. Store reframe keyframes per candidate so all platform exports remain reproducible.

## Captions and variants

Generate output-timeline captions from the approved EDL. Keep raw transcript timing immutable and display corrections separate. Create a small, intentional style set—such as restrained, energetic, and minimal—rather than random styling per clip.

Bundle shared analysis once, then render candidates and platform variants from the same source manifest. Validate every output independently for crop, caption safe area, audio, codec, duration, and meaning.
