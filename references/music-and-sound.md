# Music and sound design

Use when music or effects materially support pace, emotion, transitions, or brand character. Silence and source sound remain valid choices; do not add music merely because the format is short.

## Decide before sourcing

Record the desired function: energy bed, emotional arc, rhythmic structure, comedic contrast, tension, release, or transition punctuation. Choose tempo, density, tonal brightness, lyric presence, and editability against the voice and story. Dense speech usually benefits from sparse instrumentation and fewer midrange elements.

Prefer sources in this order:

1. a user-provided track with known rights;
2. an existing licensed organizational library;
3. a track whose current license is verified per asset before download or use;
4. original or generated material only when the user authorizes the provider, terms, network use, and any cost.

Do not treat a library's general reputation as proof that a particular track is cleared. Record title, creator, source URL, retrieval date, license identifier/version, attribution text, territory/platform limits, modification rules, and proof file or screenshot. CC-BY material requires attribution; "royalty-free" does not necessarily mean free, attribution-free, or immune from content-ID claims.

## Build the cue map

Use a few motivated events instead of placing effects on every cut:

- riser or whoosh for an actual entrance or escalation;
- lift or light hit for a chapter/diagram state change;
- chime for a verified completion or confirmation;
- low impact for a genuine reveal, contrast, or result;
- tail or music release to shape the ending.

Attach every event to a visual cause or narrative beat in the manifest. Verify the transient lands on the intended frame. Avoid effects that imply UI confirmation, success, danger, or impact when the image does not support that meaning.

## Dialogue-first mix

- Repair and level dialogue before fitting music.
- Begin with music roughly 8–12 dB below its non-dialogue level during speech, then adjust by ear on headphones, phone speakers, and a small mono speaker.
- Use transparent attack/release so pumping does not call attention to itself. Restore energy in pauses only when the phrase and music both benefit.
- Keep room tone or ambience across dialogue cuts; effects must not mask consonants.
- For general online delivery, approximately -16 LUFS integrated and no more than -1.5 dBTP is a practical starting point, not a universal platform specification.
- Measure again after the final limiter/normalization pass; music and impacts can change both integrated loudness and true peak.

Use FFmpeg `sidechaincompress` when dialogue-driven automatic ducking is sufficient. Use Remotion `<Audio>` with a frame-relative volume callback when the cue map needs authored phrase-, scene-, or transient-level control. In either route, store the gain/duck envelope or reproducible command in the project.

## Delivery record

Include the music/SFX asset ledger, attribution text, mix method, loudness/true-peak report, and unresolved rights limitations in the handoff. Never publish or claim clearance when the recorded license does not cover the intended use.
