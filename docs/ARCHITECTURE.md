# Architecture

Video Production Studio Skill is a portable instruction and automation package.

Repository description: A portable Agent Skill with Python workflow guidance for transcript editing, multi-track timelines, Remotion motion graphics, and verified video delivery.

- `SKILL.md` routes an agent to the minimum relevant production guidance.
- `references/` contains editorial, transcript, timeline, Remotion, B-roll, finishing, and guided-workflow contracts.
- `scripts/video_project.py` supplies the cross-agent project state machine and terminal interface.
- `scripts/transcribe_local.py` creates local transcript artifacts when Faster Whisper is available.
- `scripts/build_edit_manifest.py` converts subtitle timing into a deterministic edit-manifest seed.
- `scripts/validate_delivery.py` probes and full-decodes final media with FFmpeg.
- `agents/openai.yaml` supplies optional Codex/OpenAI interface metadata.

Runtime media lives in a separate guided project directory. Its `project.json` records state while large media and generated artifacts remain outside this skill repository.
