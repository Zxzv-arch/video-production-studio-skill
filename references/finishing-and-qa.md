# Finishing and quality assurance

Use for color, sound, subtitles, encoding, and final delivery.

## Audio order of priority

1. Dialogue intelligibility
2. Music supporting the intended energy
3. Sound effects punctuating real visual events
4. Ambience maintaining continuity

Use a consistent loudness target appropriate to the destination. For general online delivery, approximately -16 LUFS integrated and no more than -1.5 dB true peak is a practical starting point. Duck music beneath speech instead of merely lowering the entire mix. Listen for clicks at every cut.

For deterministic FFmpeg normalization, use the `loudnorm` filter in two passes: first analyze with video disabled and `print_format=json`; then supply the measured input integrated loudness, loudness range, true peak, and threshold to a second linear pass. Preserve the measurement JSON in the QA record. Re-run EBU R128 measurement on the encoded delivery because limiting, music, effects, and lossy encoding can change the result.

```text
# Pass 1; use NUL on Windows and /dev/null on macOS/Linux
ffmpeg -i <mix> -vn -af loudnorm=I=-16:LRA=11:TP=-1.5:print_format=json -f null <null-device>

# Pass 2; fill every measured_* value and offset from pass 1
ffmpeg -i <mix> -af loudnorm=I=-16:LRA=11:TP=-1.5:measured_I=<input_i>:measured_LRA=<input_lra>:measured_TP=<input_tp>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true:print_format=summary <output>
```

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

On Windows, libass subtitle filters require careful escaping of drive letters, backslashes, quotes, and filter separators. Pass an explicit `fontsdir` when the selected font is not guaranteed to be discoverable, and use `force_style` only for reviewed presentation overrides. If a particular FFmpeg build or shell still fails on non-ASCII filter paths, stage the SRT and required fonts in a short ASCII-only temporary directory, render to a new output, then preserve attribution and clean up only agent-created temporary files.

## FFmpeg assembly invariants

Before concatenating filtered segments, normalize the properties that the concat filter requires: dimensions, sample/display aspect ratio, frame rate/time base, pixel format, audio sample rate, channel layout, and starting timestamps. Apply `setsar=1` to every video branch when inputs have mismatched or non-square SAR and square-pixel output is intended; it is not a universal requirement for already-matching intentional anamorphic media. Normalize each branch symmetrically before `concat`, and test a short assembly before a long encode.

Keep trim and timestamp operations paired: video branches usually need `trim` plus `setpts=PTS-STARTPTS`, and audio branches `atrim` plus `asetpts=PTS-STARTPTS`. Add short audio fades or crossfades at discontinuities instead of relying on concat alone to prevent clicks.

## Export and validation

Choose resolution, frame rate, codec, profile, pixel format, color tags, bitrate or quality factor, audio sample rate, and fast-start behavior deliberately. Do not upscale unless the user needs a specific delivery raster and understands that detail is not recovered.

For each final file, confirm it exists, full-decode video and audio, check duration/resolution/frame rate/audio, inspect every major scene and transition, verify sync near the beginning and end, listen to the loudest transition, and confirm deliverable names. Use `scripts/validate_delivery.py` for technical checks; it does not replace editorial review.

Choose visual QA frames intentionally: the title card, middle of every scene, every return to a speaker, the longest/lowest caption, each picture-in-picture layout, aggressive punch-ins, and the frame around every major transition. For talking heads, explicitly verify that captions, progress indicators, and graphics do not cover the mouth, eyes, hands, or demonstrated object in any aspect-ratio variant.

Example technical acceptance command:

```text
python scripts/validate_delivery.py <final.mp4> --require-audio --expect-resolution 1080x1920 --measure-loudness --expect-lufs -16 --lufs-tolerance 1 --max-true-peak -1.5 --require-color-tags
```

Color tags are evidence, not proof that pixels are correct. Compare representative decoded frames or signal statistics against the approved reference. Retag/remux only when the pixel interpretation is known and the metadata alone is wrong; otherwise transcode through an explicit color conversion and validate again.
