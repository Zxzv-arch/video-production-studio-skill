#!/usr/bin/env python3
"""Create a pinned Remotion starter without invoking Git or create-video."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from textwrap import dedent


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


DEFAULT_VERSIONS = {
    "remotion": "4.0.520",
    "react": "19.2.8",
    "react_types": "19.2.18",
    "react_dom_types": "19.2.7",
    "typescript": "5.9.3",
}


def safe_package_name(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9._-]+", "-", value.lower()).strip("-.")
    return normalized or "remotion-video"


def talking_head_template_files(root: Path) -> dict[Path, str]:
    return {
        root / "src" / "Composition.tsx": dedent(
            """
            import React from 'react';
            import {TalkingHeadDemo} from './talk-demo/TalkingHeadDemo';

            export const Main: React.FC = () => (
              <TalkingHeadDemo speakerSrc="" demoSrc="" />
            );
            """
        ).lstrip(),
        root / "src" / "talk-demo" / "scene-schedule.ts": dedent(
            """
            export type StageMode =
              | 'speaker-full'
              | 'speaker-support'
              | 'demo-with-pip'
              | 'split'
              | 'demo-detail'
              | 'speaker-return';

            export type SceneCue = {
              id: string;
              from: number;
              durationInFrames: number;
              mode: StageMode;
              eyebrow: string;
              headline: string;
              callout?: string;
              focusTarget?: {x: number; y: number; width: number; height: number};
            };

            // Replace these example cues with transcript-linked output-timeline beats.
            export const sceneSchedule: readonly SceneCue[] = [
              {id: 'hook', from: 0, durationInFrames: 90, mode: 'speaker-full', eyebrow: 'THE PROMISE', headline: 'Start with the person and the outcome'},
              {id: 'proof', from: 90, durationInFrames: 120, mode: 'demo-with-pip', eyebrow: 'REAL DEMO', headline: 'Let the implementation take the main stage', callout: 'Show the action, then the changed state', focusTarget: {x: 0.50, y: 0.48, width: 0.24, height: 0.18}},
              {id: 'compare', from: 210, durationInFrames: 75, mode: 'split', eyebrow: 'WHY IT WORKS', headline: 'Keep the explanation beside the evidence', callout: 'One hero action per beat', focusTarget: {x: 0.12, y: 0.45, width: 0.44, height: 0.20}},
              {id: 'return', from: 285, durationInFrames: 75, mode: 'speaker-return', eyebrow: 'SYNTHESIS', headline: 'Return to the speaker for meaning and next steps'},
            ];
            """
        ).lstrip(),
        root / "src" / "talk-demo" / "TalkingHeadDemo.tsx": dedent(
            """
            import React from 'react';
            import {Video} from '@remotion/media';
            import {
              AbsoluteFill,
              Easing,
              Sequence,
              interpolate,
              staticFile,
              useCurrentFrame,
              useVideoConfig,
            } from 'remotion';
            import {sceneSchedule, type StageMode} from './scene-schedule';

            type Box = {left: number; top: number; width: number; height: number; radius: number};
            type TalkingHeadDemoProps = {speakerSrc?: string; demoSrc?: string};

            const mix = (a: number, b: number, progress: number) => a + (b - a) * progress;

            const presenterBox = (mode: StageMode, width: number, height: number): Box => {
              if (mode === 'speaker-full' || mode === 'speaker-return') {
                return {left: 0, top: 0, width, height, radius: 0};
              }
              if (mode === 'speaker-support') {
                return {left: width * 0.06, top: height * 0.08, width: width * 0.52, height: height * 0.84, radius: 28};
              }
              if (mode === 'split') {
                return {left: width * 0.05, top: height * 0.12, width: width * 0.40, height: height * 0.72, radius: 28};
              }
              if (mode === 'demo-detail') {
                return {left: width * 0.74, top: height * 0.07, width: width * 0.21, height: height * 0.28, radius: 24};
              }
              return {left: width * 0.69, top: height * 0.07, width: width * 0.26, height: height * 0.30, radius: 28};
            };

            const evidenceBox = (mode: StageMode, width: number, height: number): Box => {
              if (mode === 'split') {
                return {left: width * 0.49, top: height * 0.12, width: width * 0.46, height: height * 0.72, radius: 28};
              }
              return {left: width * 0.035, top: height * 0.045, width: width * 0.93, height: height * 0.91, radius: 32};
            };

            const cueIndexAt = (frame: number) => {
              let index = 0;
              for (let i = 1; i < sceneSchedule.length; i++) {
                if (frame >= sceneSchedule[i].from) index = i;
              }
              return index;
            };

            const Surface: React.FC<{src?: string; label: string; muted?: boolean}> = ({src, label, muted}) => (
              <AbsoluteFill style={{backgroundColor: '#11182b', overflow: 'hidden'}}>
                {src ? (
                  <Video src={staticFile(src)} muted={muted} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
                ) : (
                  <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', color: '#8fa7cf', fontFamily: 'Arial, sans-serif', fontSize: 42, fontWeight: 700}}>
                    {label}
                  </AbsoluteFill>
                )}
              </AbsoluteFill>
            );

            const BeatCopy: React.FC<{from: number; durationInFrames: number; mode: StageMode; eyebrow: string; headline: string; callout?: string}> = ({from, durationInFrames, mode, eyebrow, headline, callout}) => (
              <Sequence from={from} durationInFrames={durationInFrames} premountFor={30}>
                <BeatCopyLocal mode={mode} eyebrow={eyebrow} headline={headline} callout={callout} />
              </Sequence>
            );

            const BeatCopyLocal: React.FC<{mode: StageMode; eyebrow: string; headline: string; callout?: string}> = ({mode, eyebrow, headline, callout}) => {
              const frame = useCurrentFrame();
              const demonstrationIsPrimary = mode === 'demo-with-pip' || mode === 'demo-detail' || mode === 'split';
              const opacity = interpolate(frame, [0, 12], [0, 1], {easing: Easing.bezier(0.16, 1, 0.3, 1), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
              const y = interpolate(frame, [0, 16], [24, 0], {easing: Easing.bezier(0.16, 1, 0.3, 1), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
              return (
                <div style={{position: 'absolute', left: 72, top: 62, width: demonstrationIsPrimary ? 560 : 760, color: 'white', fontFamily: 'Arial, sans-serif', opacity, translate: `0px ${y}px`, zIndex: 5}}>
                  <div style={{fontSize: 22, fontWeight: 800, letterSpacing: 3, color: '#67e8f9'}}>{eyebrow}</div>
                  <div style={{fontSize: demonstrationIsPrimary ? 38 : 50, lineHeight: 1.06, fontWeight: 800, marginTop: 12, textShadow: '0 3px 20px rgba(0,0,0,0.55)'}}>{headline}</div>
                  {callout ? <div style={{display: 'inline-block', marginTop: 18, padding: '10px 16px', borderRadius: 999, backgroundColor: 'rgba(5,12,25,0.82)', border: '1px solid rgba(103,232,249,0.6)', fontSize: 22}}>{callout}</div> : null}
                </div>
              );
            };

            export const TalkingHeadDemo: React.FC<TalkingHeadDemoProps> = ({speakerSrc, demoSrc}) => {
              const frame = useCurrentFrame();
              const {fps, width, height, durationInFrames} = useVideoConfig();
              const index = cueIndexAt(frame);
              const cue = sceneSchedule[index];
              const previous = sceneSchedule[Math.max(0, index - 1)];
              const transferFrames = Math.max(1, Math.round(0.5 * fps));
              const progress = index === 0 ? 1 : interpolate(frame, [cue.from, cue.from + transferFrames], [0, 1], {easing: Easing.bezier(0.16, 1, 0.3, 1), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
              const previousPresenter = presenterBox(previous.mode, width, height);
              const currentPresenter = presenterBox(cue.mode, width, height);
              const previousEvidence = evidenceBox(previous.mode, width, height);
              const currentEvidence = evidenceBox(cue.mode, width, height);
              const previousEvidenceVisible = previous.mode === 'speaker-full' || previous.mode === 'speaker-return' ? 0 : 1;
              const currentEvidenceVisible = cue.mode === 'speaker-full' || cue.mode === 'speaker-return' ? 0 : 1;
              const focusProgress = cue.focusTarget ? interpolate(frame, [cue.from + transferFrames + 4, cue.from + transferFrames + 14], [0, 1], {easing: Easing.bezier(0.16, 1, 0.3, 1), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;

              return (
                <AbsoluteFill style={{backgroundColor: '#060b18'}}>
                  <div style={{position: 'absolute', left: mix(previousEvidence.left, currentEvidence.left, progress), top: mix(previousEvidence.top, currentEvidence.top, progress), width: mix(previousEvidence.width, currentEvidence.width, progress), height: mix(previousEvidence.height, currentEvidence.height, progress), borderRadius: mix(previousEvidence.radius, currentEvidence.radius, progress), overflow: 'hidden', opacity: mix(previousEvidenceVisible, currentEvidenceVisible, progress), boxShadow: '0 24px 80px rgba(0,0,0,0.45)', zIndex: 1}}>
                    <Surface src={demoSrc} label="DEMONSTRATION / EVIDENCE" muted />
                  </div>

                  {cue.focusTarget ? (
                    <div style={{position: 'absolute', left: currentEvidence.left + currentEvidence.width * cue.focusTarget.x, top: currentEvidence.top + currentEvidence.height * cue.focusTarget.y, width: currentEvidence.width * cue.focusTarget.width, height: currentEvidence.height * cue.focusTarget.height, borderRadius: 18, border: '4px solid #67e8f9', boxShadow: '0 0 0 8px rgba(103,232,249,0.13), 0 10px 36px rgba(0,0,0,0.4)', opacity: focusProgress, scale: 0.94 + 0.06 * focusProgress, transformOrigin: 'center', zIndex: 2}}>
                      <div style={{position: 'absolute', right: -11, bottom: -11, width: 22, height: 22, borderRadius: 999, backgroundColor: '#f8fafc', border: '5px solid #06b6d4'}} />
                    </div>
                  ) : null}

                  <div style={{position: 'absolute', left: mix(previousPresenter.left, currentPresenter.left, progress), top: mix(previousPresenter.top, currentPresenter.top, progress), width: mix(previousPresenter.width, currentPresenter.width, progress), height: mix(previousPresenter.height, currentPresenter.height, progress), borderRadius: mix(previousPresenter.radius, currentPresenter.radius, progress), overflow: 'hidden', border: cue.mode === 'speaker-full' || cue.mode === 'speaker-return' ? '0 solid transparent' : '2px solid rgba(255,255,255,0.72)', boxShadow: cue.mode === 'speaker-full' || cue.mode === 'speaker-return' ? 'none' : '0 18px 60px rgba(0,0,0,0.48)', zIndex: 3}}>
                    <Surface src={speakerSrc} label="PRESENTER VIDEO" />
                  </div>

                  {sceneSchedule.map((item) => <BeatCopy key={item.id} {...item} />)}

                  <div style={{position: 'absolute', left: 0, bottom: 0, width: `${(frame / Math.max(1, durationInFrames - 1)) * 100}%`, height: 7, backgroundColor: '#67e8f9', zIndex: 8}} />
                </AbsoluteFill>
              );
            };
            """
        ).lstrip(),
    }


def files_for(root: Path, versions: dict[str, str], template: str) -> dict[Path, str]:
    package = {
        "name": safe_package_name(root.name),
        "version": "1.0.0",
        "private": True,
        "scripts": {
            "studio": "remotion studio",
            "browser:ensure": "remotion browser ensure",
            "render": "remotion render Main out/video.mp4",
            "still": "remotion still Main out/review.png --frame=30",
        },
        "dependencies": {
            "@remotion/cli": versions["remotion"],
            "@remotion/media": versions["remotion"],
            "react": versions["react"],
            "react-dom": versions["react"],
            "remotion": versions["remotion"],
        },
        "devDependencies": {
            "@types/react": versions["react_types"],
            "@types/react-dom": versions["react_dom_types"],
            "typescript": versions["typescript"],
        },
    }
    duration = 360 if template == "talking-head-demo" else 150
    generated = {
        root / "package.json": json.dumps(package, indent=2) + "\n",
        root / "tsconfig.json": json.dumps(
            {
                "compilerOptions": {
                    "target": "ES2022",
                    "lib": ["DOM", "ES2022"],
                    "module": "ESNext",
                    "moduleResolution": "Bundler",
                    "jsx": "react-jsx",
                    "strict": True,
                    "noEmit": True,
                    "skipLibCheck": True,
                },
                "include": ["src", "remotion.config.ts"],
            },
            indent=2,
        )
        + "\n",
        root / "remotion.config.ts": (
            "import {Config} from '@remotion/cli/config';\n\n"
            "Config.setEntryPoint('./src/index.ts');\n"
            "Config.setOverwriteOutput(true);\n"
        ),
        root / "src" / "index.ts": (
            "import {registerRoot} from 'remotion';\n"
            "import {RemotionRoot} from './Root';\n\n"
            "registerRoot(RemotionRoot);\n"
        ),
        root / "src" / "Root.tsx": (
            "import React from 'react';\n"
            "import {Composition} from 'remotion';\n"
            "import {Main} from './Composition';\n\n"
            "export const RemotionRoot: React.FC = () => (\n"
            f"  <Composition id=\"Main\" component={{Main}} durationInFrames={{{duration}}} fps={{30}} width={{1920}} height={{1080}} />\n"
            ");\n"
        ),
        root / "src" / "Composition.tsx": (
            "import React from 'react';\n"
            "import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';\n\n"
            "export const Main: React.FC = () => {\n"
            "  const frame = useCurrentFrame();\n"
            "  const opacity = interpolate(frame, [0, 20], [0, 1], {extrapolateRight: 'clamp'});\n"
            "  return (\n"
            "    <AbsoluteFill style={{backgroundColor: '#0b1020', color: 'white', alignItems: 'center', justifyContent: 'center'}}>\n"
            "      <div style={{fontFamily: 'sans-serif', fontSize: 96, fontWeight: 800, opacity}}>Video Production Studio</div>\n"
            "    </AbsoluteFill>\n"
            "  );\n"
            "};\n"
        ),
        root / "public" / ".gitkeep": "",
        root / "out" / ".gitkeep": "",
    }
    if template == "talking-head-demo":
        generated.update(talking_head_template_files(root))
    return generated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--remotion-version", default=DEFAULT_VERSIONS["remotion"])
    parser.add_argument("--template", choices=["minimal", "talking-head-demo"], default="minimal")
    parser.add_argument("--force", action="store_true", help="Replace only generated files; never removes other files")
    args = parser.parse_args()
    versions = dict(DEFAULT_VERSIONS)
    versions["remotion"] = args.remotion_version
    root = args.output.expanduser().resolve()
    generated = files_for(root, versions, args.template)
    collisions = [path for path in generated if path.exists()]
    if collisions and not args.force:
        parser.error("Refusing to replace existing files:\n" + "\n".join(str(path) for path in collisions))
    for path, content in generated.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "project": str(root),
                "files": [str(path.relative_to(root)) for path in generated],
                "remotionVersion": versions["remotion"],
                "template": args.template,
                "next": ["npm install", "npm run browser:ensure", "npm run studio"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
