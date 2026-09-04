# AI handoff

Project: Video Production Studio Skill

Description: A portable Agent Skill with Python workflow guidance for transcript editing, multi-track timelines, Remotion motion graphics, and verified video delivery.

Start with `SKILL.md`. For a complex video, read `references/guided-workflow.md`, run `scripts/video_project.py status`, and treat the guided project's `project.json` as the source of truth. Check `renderPlan.activeMode` before rendering and read `references/render-modes.md` when changing the render budget. Do not rely on prior chat history.

For presenter-led work, also read `references/talking-head-demonstrations.md`. Preserve the continuous dialogue clock and presenter layer, then schedule evidence scenes and PiP layout states from output-timeline transcript beats.

Preserve originals and existing edits. Do not upload private footage, create accounts, spend credits, or publish media without explicit authorization. Register artifacts and decisions before handing work to another agent.

The repository contains instructions and utilities, not user footage, transcripts, credentials, or generated client media.

License: Apache-2.0. Preserve the repository's `LICENSE` and applicable `NOTICE` information when redistributing it.

This is a self-contained Agent Skill. Do not request another editing or Remotion guidance skill. Check actual executable availability with `python scripts/video_project.py doctor --project-root <dir> --write --json`; use the recorded fallback plan and report only software that the chosen deliverable requires.
