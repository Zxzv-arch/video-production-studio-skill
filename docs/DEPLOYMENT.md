# Installation and deployment

This repository is a skill package; it has no server deployment.

Project: Video Production Studio Skill. Repository: `Zxzv-arch/video-production-studio-skill`.

The public repository is distributed under Apache-2.0. Clones and redistributed packages must retain the license and applicable notice information.

For Codex, copy the repository directory to the local Codex skills folder and keep the directory name `video-production-studio`.

For OpenCode, copy or clone it to `.opencode/skills/video-production-studio/` in a project, or `~/.config/opencode/skills/video-production-studio/` for global discovery. Preserve the complete directory so references and scripts remain available.

For Claude Code, copy or clone it to `.claude/skills/video-production-studio/` in a project or `~/.claude/skills/video-production-studio/` for personal discovery, then invoke `/video-production-studio` or let the description trigger it.

Required for the guided interface: Python 3. Optional production dependencies are FFmpeg, Faster Whisper, Node.js, and Remotion. Cloud providers are not required.

Run `python scripts/video_project.py doctor --project-root <initialized-project> --write --json` on every new Agent environment. It reports platform-specific bootstrap hints but performs no installation. The project can continue through planning and handoff when optional components are absent; `references/environment-fallbacks.md` defines authorized setup and honest degraded routes.
