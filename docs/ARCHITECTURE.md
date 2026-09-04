# Architecture

Video Production Studio Skill is a portable instruction and automation package.

Repository description: A portable Agent Skill with Python workflow guidance for transcript editing, multi-track timelines, Remotion motion graphics, and verified video delivery.

- `SKILL.md` routes an agent to the minimum relevant production guidance.
- `references/` contains editorial, transcript, timeline, Remotion, B-roll, shot-direction, short-form selection and energetic styling, music/sound, environment bootstrap/fallback, finishing, and guided-workflow contracts.
- `scripts/video_project.py` supplies the cross-agent project state machine and terminal interface.
- `scripts/transcribe_local.py` creates local transcript artifacts when Faster Whisper is available.
- `scripts/build_edit_manifest.py` converts subtitle timing into a deterministic edit-manifest seed.
- `scripts/retime_captions.py` maps immutable source words and reviewed corrections through an EDL into karaoke-ready output timing.
- `scripts/bootstrap_remotion_project.py` writes a pinned minimal Remotion project when Git or `create-video` cannot be used.
- `scripts/validate_delivery.py` probes, full-decodes, checks color metadata, and optionally measures EBU R128 loudness.
- `agents/openai.yaml` supplies optional Codex/OpenAI interface metadata.

Runtime media lives in a separate guided project directory. Its `project.json` records state while large media and generated artifacts remain outside this skill repository.

The skill has no Agent Skill dependency. Its references contain the required editorial and Remotion decision rules; external executables are detected separately by the guided interface.
