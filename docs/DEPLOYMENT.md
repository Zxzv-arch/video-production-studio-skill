# Installation and deployment

This repository is a skill package; it has no server deployment.

Project: Video Production Studio Skill. Repository: `Zxzv-arch/video-production-studio-skill`.

For Codex, copy the repository directory to the local Codex skills folder and keep the directory name `video-production-studio`.

For OpenCode, copy or clone it to `.opencode/skills/video-production-studio/` in a project, or `~/.config/opencode/skills/video-production-studio/` for global discovery. Preserve the complete directory so references and scripts remain available.

Required for the guided interface: Python 3. Optional production dependencies are FFmpeg, Faster Whisper, Node.js, and Remotion. Cloud providers are not required.

Run `python scripts/video_project.py doctor --project-root <initialized-project> --write --json` on every new Agent environment. The project can continue through planning and handoff when optional components are absent; `references/environment-fallbacks.md` defines honest degraded routes.
