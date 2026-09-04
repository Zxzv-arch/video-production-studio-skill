# Transcript-driven editing

Use for interviews, podcasts, courses, talking heads, and any edit where speech determines structure.

## Required transcript data

Prefer word-level entries containing `text`, `start`, `end`, `confidence`, and optional `speaker`. Keep the raw transcript immutable and store editorial corrections separately.

Assign stable zero-based source word indexes before editing. A correction record must point back to those indexes and preserve raw text, display text, confidence, basis, review status, and whether it must appear in delivery disclosure. Display captions may use approved corrections; edit decisions and factual audit trails continue to reference the immutable raw words.

Names, product terms, acronyms, measurements, and version numbers deserve manual or contextual verification. Low-confidence terms must not silently become authoritative captions.

## Silence and filler policy

- Treat pause removal as editorial judgment, not a global threshold.
- Candidate dead air: usually 0.8 seconds or longer.
- Preserve shorter breaths around emotional, technical, or comedic beats.
- When tightening adjacent sentences, retain 120–350 ms of natural room unless the intended style is deliberately rapid.
- Remove filler words only when the sentence remains grammatical and the edit does not create a visible mouth jump that needs a cutaway.
- Remove false starts and duplicated takes only after confirming the later take carries the intended meaning.

## Cut construction

1. Snap video cuts to verified word boundaries.
2. Add 30–120 ms boundary padding where ASR timing may drift.
3. Apply 20–50 ms audio fades at every discontinuity.
4. Use room tone across tightened gaps; do not leave digital silence.
5. Hide unavoidable talking-head jumps with a motivated punch-in, alternate angle, diagram, screenshot, or B-roll.
6. Preserve sync by deriving video and audio cuts from the same edit decision list.
7. Generate output captions from that decision list with `scripts/retime_captions.py`; never shift source timestamps by hand after each removal.

## Multiple speakers

Use diarization when speaker identity affects the story or captions. Verify speaker turns near overlap, laughter, crosstalk, and telephone-quality audio. Keep a speaker map separate from ASR text so identities can be corrected without retranscription.

## Outputs

Keep:

- raw word transcript;
- corrected display captions;
- selects/rejects list with reasons;
- edit decision list with source time ranges;
- optional clean transcript for publication.

The clean transcript may improve punctuation and readability. It must not be reused as frame-accurate evidence unless its timing remains linked to the raw words.
