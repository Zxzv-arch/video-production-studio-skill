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

Projects start in a low-cost `draft` render mode. Promote only when the work is ready:

```powershell
python scripts/video_project.py render-mode --project-root C:\path\to\my-video-project --set review --note "Complete sequence ready"
python scripts/video_project.py render-mode --project-root C:\path\to\my-video-project --set master --note "Timing and motion approved"
```

`draft` favors stills, short ranges, proxies, and low-resolution previews; `review` validates the complete sequence economically; `master` performs requested-resolution rendering, final finishing, full decode, and delivery QA. This prevents disposable iterations from paying final-export costs.

Check executable capabilities without triggering dependency reminders:

```powershell
python scripts/video_project.py doctor --project-root C:\path\to\my-video-project --write
```

The report distinguishes planning, FFmpeg editing, local ASR, GPU acceleration, Remotion scaffolding, an installed Remotion runtime, browser capture, and disk capacity. It emits a degraded but honest fallback plan when components are absent.

Additional portable helpers cover three frequent handoff gaps:

```powershell
# Create a pinned Remotion project without Git/create-video
python scripts/bootstrap_remotion_project.py C:\path\to\my-video-project\remotion

# Convert source word timestamps through the approved edit manifest
python scripts/retime_captions.py words.json edit-manifest.json captions.karaoke.json --fps 30

# Register a supplemental artifact without changing the workflow stage
python scripts/video_project.py register --project-root C:\path\to\my-video-project --artifact exports\final-v2.mp4 --role final
```

## What to copy

Copy or clone the **entire repository folder**, not only `SKILL.md`. The entry file links to the bundled workflow references, templates, and project-control script.

| Path | Role |
| --- | --- |
| `SKILL.md` | Required portable Agent Skill entry point. |
| `references/` | Editing, karaoke captions, energetic short-form, B-roll, Remotion, render-budget, music/audio, and delivery guidance loaded on demand. |
| `scripts/` | Optional but recommended guided project interface and environment checks. |
| `agents/openai.yaml` | Optional OpenAI/Codex UI metadata. Other compatible agents can safely ignore it. |

Any agent that implements the open Agent Skills folder convention can load `SKILL.md` directly. `agents/openai.yaml` is not a runtime dependency.

## Install in Codex

Place the repository at `video-production-studio` inside the target Codex skills directory, then invoke it as `$video-production-studio` or describe a complex video-production task that matches its description.

Personal installation on Windows:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills" | Out-Null
git clone https://github.com/Zxzv-arch/video-production-studio-skill.git "$env:USERPROFILE\.codex\skills\video-production-studio"
```

## Install in OpenCode

OpenCode discovers the full skill directory—including scripts and references—from either location:

- project: `.opencode/skills/video-production-studio/`
- global: `~/.config/opencode/skills/video-production-studio/`

Clone or copy the entire folder, then ask OpenCode to load `video-production-studio` or start a complex video task. The lowercase directory name and `SKILL.md` frontmatter match OpenCode's portable Agent Skills convention.

Project-local installation on Windows:

```powershell
git clone https://github.com/Zxzv-arch/video-production-studio-skill.git .opencode/skills/video-production-studio
```

## Install in Claude Code

Claude Code supports the same folder-based Agent Skills format and discovers skills from either location:

- project: `.claude/skills/video-production-studio/`
- personal: `~/.claude/skills/video-production-studio/`

Project-local installation on Windows:

```powershell
New-Item -ItemType Directory -Force -Path .claude\skills | Out-Null
git clone https://github.com/Zxzv-arch/video-production-studio-skill.git .claude\skills\video-production-studio
```

Personal installation on Windows:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills" | Out-Null
git clone https://github.com/Zxzv-arch/video-production-studio-skill.git "$env:USERPROFILE\.claude\skills\video-production-studio"
```

Personal installation on macOS or Linux:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/Zxzv-arch/video-production-studio-skill.git ~/.claude/skills/video-production-studio
```

Claude can select the skill automatically from its description, or you can invoke it explicitly with `/video-production-studio`. If `.claude/skills` did not exist when the current Claude Code session started, restart that session once so the new top-level directory is watched. `agents/openai.yaml` is not required by Claude Code.

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
