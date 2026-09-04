# Environment capability and fallback matrix

Use this reference after `scripts/video_project.py doctor --project-root <dir> --write --json`. Agent instructions are bundled; this matrix concerns executable capabilities only. `--write` stores the observed profile and fallback plan in the initialized project's `project.json` for the next agent.

## Rules

1. Detect before installing. Do not assume a binary, package, GPU, font, browser, codec, editor, login, network connection, or paid credit exists.
2. Do not install software, upload footage, sign in, or spend money without authority.
3. Select the narrowest engine that satisfies the output. Record the chosen route and degraded features in `project.json`.
4. If a fallback changes the visual result, editability, privacy, cost, or final format materially, tell the user. Otherwise continue and document it.
5. Never fabricate a render, transcript, media probe, GUI project, or validation result.

## Authorized environment bootstrap

`doctor` reports capabilities and never installs them. Only run installation commands after the user has authorized local software changes. Re-run `doctor --write --json` afterward and record the executable paths actually selected.

| Capability | Windows (`winget`) | macOS (Homebrew) | Debian/Ubuntu (`apt`) |
|---|---|---|---|
| FFmpeg | `winget install --id Gyan.FFmpeg --exact` | `brew install ffmpeg` | `sudo apt update && sudo apt install ffmpeg` |
| Python | `winget search Python.Python` then install an approved maintained 3.x package by exact ID | `brew install python` | `sudo apt install python3 python3-venv python3-pip` |
| Node.js/npm | `winget install --id OpenJS.NodeJS.LTS --exact` | `brew install node` | use a maintained Node LTS source appropriate to the host; distro `nodejs` may be too old |
| Git | `winget install --id Git.Git --exact` | `brew install git` | `sudo apt install git` |

Package IDs and supported versions can change. Search first, capture the selected version, and verify with `ffmpeg -version`, `python --version`, `node --version`, `npm --version`, and `git --version`. Do not silently elevate privileges or work around UAC/sudo denial.

On Windows, `python.exe` may resolve to a Microsoft Store application-execution alias under `WindowsApps` instead of a usable interpreter. Check `Get-Command python` and `py -0p`; use the verified interpreter's absolute path or disable the alias rather than assuming `python` is functional. Keep that path in the project's reproduction commands.

### Remotion without Git or `create-video`

Git is not required to author or render a Remotion project. When `create-video` is unavailable, inappropriate for the current repository, or blocked during scaffolding, generate the bundled pinned minimal project without invoking Git:

```text
python scripts/bootstrap_remotion_project.py <project-root>/remotion
cd <project-root>/remotion
npm install
npm run browser:ensure
npm run studio
```

For presenter-led explainers, add `--template talking-head-demo` to generate the animated continuous-presenter, evidence-stage, and scene-schedule starter instead of the minimal title card.

The generator writes exact dependency versions plus `package.json`, `tsconfig.json`, `remotion.config.ts`, and explicit source entry files. Before intentionally upgrading, query the current compatible Remotion version, pass it with `--remotion-version`, keep every `remotion` and `@remotion/*` package on exactly that version, and validate a still plus a short render.

Newer npm releases may report or block unreviewed dependency lifecycle scripts. Do not assume a skipped script is harmless, and do not globally enable all scripts. Inspect the exact npm message and package; use the review command exposed by that installed npm (`npm approve-scripts --allow-scripts-pending` or `npm install-scripts ls`, depending on version), review the pinned dependency, then approve only the required package/version. A blocked native or bundler install script such as esbuild's platform validation can leave an apparently installed dependency unusable.

## Capability matrix

| Missing capability | Continue with | Lost or changed | Stop only when |
|---|---|---|---|
| FFmpeg/FFprobe | inspect with an available media library; build transcript, storyboard, EDL, Remotion source, or NLE plan without final media operations | no trustworthy probe/full decode; simple trim/export unavailable | the requested deliverable is an encoded or technically verified media file and no equivalent exists |
| Node.js/Remotion | FFmpeg for cuts, scaling, captions, simple overlays, audio, and export; static cards from an image library | reduced interactive motion and programmatic scene complexity | the approved design specifically requires React/Remotion rendering |
| Remotion package in an existing Node project | inspect `package.json`; if installs are authorized, use the project's package manager and version-matched packages; otherwise produce source plan and assets | no preview/render until installed | rendered Remotion output is required now |
| Local ASR | use a supplied transcript/SRT/VTT; extract audio for manual transcription; produce a visual-only plan | no automatic word timing | dialogue-driven cuts or captions are required and no timed text exists |
| GPU | use CPU ASR with a smaller model, proxies, lower preview scale, fewer render workers, or chunked rendering | longer processing and sometimes lower ASR confidence | deadline or media size makes CPU completion impractical |
| Browser or screen-capture automation | use user screenshots/recordings, extract frames from supplied video, or create diagrammatic UI explanations | no live product-state capture | truthful demonstration of an uncaptured state is essential |
| GUI NLE | keep `project.json`, EDL/OTIO/FCPXML/CSV where supported, plus a Remotion or FFmpeg reconstruction | no manual drag timeline on this machine | the user explicitly requires a native editor project that cannot be generated safely |
| Target NLE adapter | deliver a portable timeline package and adapter-ready track map; test a small interchange file | native effects and caption styles may not round-trip | a verified native draft is the required deliverable |
| Exact font | use a metrically suitable local fallback only for a preview and record substitution | line wraps and brand appearance may differ | final brand typography is mandatory |
| Network/cloud generation | use local/user assets, diagrams, crops, typography, and camera moves | no stock search or generated B-roll | the story requires an unavailable asset and no honest substitute exists |
| Music/SFX library | use room tone, source sound, silence, or clearly licensed local assets | less designed soundscape | music is contractually required |
| Disk space | generate low-resolution proxies, render by scene/chunk, reuse caches, remove only agent-created intermediates after approval | slower pipeline and extra concat step | safe free space remains below estimated peak usage |

## Command fallbacks

- If system FFmpeg is absent but a local Remotion CLI exists, probe whether that installed version exposes `npx remotion ffmpeg` and `npx remotion ffprobe`. Do not assume support without running `--help` or a harmless version command.
- If hardware encoding fails, retry a short sample with CPU H.264 before the full render.
- If a camera codec fails in browser preview, create an H.264/AAC proxy while keeping source timecodes and returning to originals for the master when possible.
- If a long render runs out of memory, lower preview scale, reduce concurrency, render scene ranges, and concatenate validated chunks.

## Handoff record

Record `environmentProfile`, `selectedEngine`, `fallbacks`, `unavailableFeatures`, and `reproductionCommands` in the guided project. Commands must contain no tokens or credentials. A later agent can rerun `doctor` and upgrade the route when more components become available.
