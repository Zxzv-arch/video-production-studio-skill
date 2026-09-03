# Video Production Studio Skill

Portable Agent Skill for complex, local-first video production. It combines transcript editing, editable timelines, content-driven Remotion motion, semantic B-roll, finishing, and verified multi-platform delivery.

It is self-contained at the Agent Skill level: no additional video-editing or Remotion guidance skill is required. Runtime programs such as FFmpeg, Python transcription packages, Node.js, and Remotion are only needed when the selected production path uses them.

Repository: `Zxzv-arch/video-production-studio-skill` (Public)

## Guided interface

Start a resumable project with the terminal wizard:

```powershell
python scripts/video_project.py init --project-root C:\path\to\my-video-project --source C:\path\to\footage.mp4
```

Resume from any AI or terminal without relying on chat history:

```powershell
python scripts/video_project.py status --project-root C:\path\to\my-video-project
```

The interface creates a portable `project.json`, production folders, stage gates, artifact history, blockers, and concrete next actions. It does not copy or upload the source footage.

Check executable capabilities without triggering dependency reminders:

```powershell
python scripts/video_project.py doctor --project-root C:\path\to\my-video-project --write
```

The report distinguishes planning, FFmpeg editing, local ASR, GPU acceleration, Remotion scaffolding, an installed Remotion runtime, browser capture, and disk capacity. It emits a degraded but honest fallback plan when components are absent.

## Install in Codex

Copy the entire `video-production-studio` folder into the target agent's skills directory, then invoke it as `$video-production-studio`. Agents that implement the open Agent Skills folder convention can read `SKILL.md` directly; `agents/openai.yaml` is optional UI metadata.

## Install in OpenCode

OpenCode discovers the full skill directory—including scripts and references—from either location:

- project: `.opencode/skills/video-production-studio/`
- global: `~/.config/opencode/skills/video-production-studio/`

Clone or copy the entire folder, then ask OpenCode to load `video-production-studio` or start a complex video task. The lowercase directory name and `SKILL.md` frontmatter match OpenCode's portable Agent Skills convention.

Project-local installation on Windows:

```powershell
git clone https://github.com/Zxzv-arch/video-production-studio-skill.git .opencode/skills/video-production-studio
```

## Agent entry point

All compatible agents should read `SKILL.md` first. For complex, multi-session, or cross-agent work, they then read `references/guided-workflow.md` and use `scripts/video_project.py` as the stateful control surface.

Core instructions have no service dependency. Optional execution features require:

- Python 3 and Faster Whisper for local transcription;
- FFmpeg for media inspection, editing, finishing, and validation;
- Node.js and Remotion for programmatic motion graphics.

Cloud editors, generative video providers, logins, uploads, and paid credits are optional and require explicit user authorization.

## License

Licensed under the Apache License 2.0. This permits commercial and private use, modification, and redistribution subject to the license terms, and includes an explicit patent grant. Keep the `LICENSE` and applicable `NOTICE` information with redistributed copies.

This repository vendors no third-party Skill or media assets. Design-research sources and their licenses are recorded in `docs/RESEARCH_SOURCES.md`.
