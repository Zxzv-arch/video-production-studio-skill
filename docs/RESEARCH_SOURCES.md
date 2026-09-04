# Research sources and adopted ideas

This project does not require the repositories below at runtime and does not vendor their code. They were reviewed as design research; the local references express original, compact guidance suited to this skill.

- [Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) — Apache-2.0. Informed shot-function planning, product-derived visual language, beat-aware timing, and still-frame review gates.
- [FireRedTeam/FireRed-OpenStoryline](https://github.com/FireRedTeam/FireRed-OpenStoryline) — Apache-2.0. Informed intent-driven media understanding, grouping, timeline planning, and speech rough-cut review.
- [luoluoluo22/jianying-editor-skill](https://github.com/luoluoluo22/jianying-editor-skill) — MIT. Informed native-draft adapters, inspect-before-write behavior, and cross-platform editor handoff.
- [LottieFiles/motion-design-skill](https://github.com/LottieFiles/motion-design-skill) — MIT. Informed motion personality, choreography consistency, accessibility alternatives, and performance budgets.
- [Jaycheng1103/chatgpt-video-editing-skills](https://github.com/Jaycheng1103/chatgpt-video-editing-skills) — MIT. Informed immutable-source workspaces, staged preview approval, and full-delivery QA.
- [AgriciDaniel/claude-shorts](https://github.com/AgriciDaniel/claude-shorts) — MIT. Informed candidate scoring, audio-aware boundaries, content-type reframing, and per-platform validation.
- [xuliang2024/cutcli-cookbook](https://github.com/xuliang2024/cutcli-cookbook) and [yihui-dev/yh-chatcut-skills](https://github.com/yihui-dev/yh-chatcut-skills) — MIT. Informed editable draft interchange and timestamp-conscious caption handoff.

Repository popularity and activity were considered during research, but quality, license clarity, portability, and complementarity determined what was adopted.

Current tool behavior was checked against primary documentation on 2026-09-03:

- [Remotion `create-video` CLI](https://www.remotion.dev/docs/cli/create-video) — non-interactive flags and repository constraints.
- [Remotion browser ensure CLI](https://www.remotion.dev/docs/cli/browser/ensure) — browser preflight, download behavior, and browser override.
- [Remotion configuration](https://www.remotion.dev/docs/config) — current `remotion.config.ts` entry-point convention.
- [npm install-script policy](https://docs.npmjs.com/cli/v11/commands/npm-install-scripts/) — version-dependent lifecycle-script review and narrow approval workflow.
