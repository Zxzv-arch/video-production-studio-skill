# Finishing and quality assurance

Use for color, sound, subtitles, encoding, and final delivery.

## Audio order of priority

1. Dialogue intelligibility
2. Music supporting the intended energy
3. Sound effects punctuating real visual events
4. Ambience maintaining continuity

Use a consistent loudness target appropriate to the destination. For general online delivery, approximately -16 LUFS integrated and no more than -1.5 dB true peak is a practical starting point. Duck music beneath speech instead of merely lowering the entire mix. Listen for clicks at every cut.

## Color

- Correct exposure and white balance before applying a look.
- Match shots within a scene before stylizing the sequence.
- Preserve skin tones unless the intended genre clearly justifies deviation.
- Keep color range and transfer tags consistent with the rendered pixels.
- Inspect gradients, shadows, and saturated graphics for banding or clipping.

## Captions

- Apply captions last and keep them in the title-safe region.
- Prefer no more than two lines and phrase breaks that follow speech.
- Verify product names, acronyms, numbers, and proper nouns.
- Check the longest line and the smallest delivery format.
- Provide a sidecar caption file when accessibility or future editing matters, even when captions are burned in.

## Export and validation

Choose resolution, frame rate, codec, profile, pixel format, color tags, bitrate or quality factor, audio sample rate, and fast-start behavior deliberately. Do not upscale unless the user needs a specific delivery raster and understands that detail is not recovered.

For each final file, confirm it exists, full-decode video and audio, check duration/resolution/frame rate/audio, inspect every major scene and transition, verify sync near the beginning and end, listen to the loudest transition, and confirm deliverable names. Use `scripts/validate_delivery.py` for technical checks; it does not replace editorial review.
