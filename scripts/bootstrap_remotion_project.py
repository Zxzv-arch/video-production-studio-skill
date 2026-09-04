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

            export type SlideCue = {
              kind: 'statement' | 'steps' | 'comparison' | 'diagram';
              title: string;
              items: readonly string[];
            };

            export type SceneCue = {
              id: string;
              from: number;
              durationInFrames: number;
              mode: StageMode;
              eyebrow: string;
              headline: string;
              accentWords?: readonly string[];
              callout?: string;
              focusTarget?: {x: number; y: number; width: number; height: number};
              demoSteps?: readonly string[];
              resultLabel?: string;
              slide: SlideCue;
            };

            // Sentence-reactive mode: every transcript sentence gets dynamic type,
            // a presenter/PiP state, and a content-specific animated slide or demo.
            export const sceneSchedule: readonly SceneCue[] = [
              {id: 'hook', from: 0, durationInFrames: 90, mode: 'speaker-support', eyebrow: 'SENTENCE 01', headline: 'Every sentence changes the visual state', accentWords: ['changes'], slide: {kind: 'statement', title: 'THE VISUAL PROMISE', items: ['SEE THE PERSON', 'SEE THE PROOF', 'UNDERSTAND WHY']}},
              {id: 'proof', from: 90, durationInFrames: 120, mode: 'demo-with-pip', eyebrow: 'SENTENCE 02', headline: 'Watch the workflow happen live', accentWords: ['live'], callout: 'Speech drives every visible state', focusTarget: {x: 0.07, y: 0.49, width: 0.58, height: 0.14}, demoSteps: ['Open', 'Change', 'Confirm'], resultLabel: 'RESULT VERIFIED', slide: {kind: 'steps', title: 'LIVE IMPLEMENTATION', items: ['Open the target', 'Perform the action', 'Confirm the result']}},
              {id: 'compare', from: 210, durationInFrames: 75, mode: 'split', eyebrow: 'SENTENCE 03', headline: 'Keep the explanation beside the evidence', accentWords: ['evidence'], callout: 'One hero action per beat', focusTarget: {x: 0.06, y: 0.36, width: 0.42, height: 0.24}, slide: {kind: 'comparison', title: 'EXPLANATION + EVIDENCE', items: ['What the speaker says', 'What the viewer can verify']}},
              {id: 'return', from: 285, durationInFrames: 75, mode: 'speaker-support', eyebrow: 'SENTENCE 04', headline: 'Resolve with meaning and next steps', accentWords: ['meaning'], slide: {kind: 'diagram', title: 'THE RESOLUTION', items: ['Meaning', 'Decision', 'Next step']}},
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
            import {sceneSchedule, type SceneCue, type StageMode} from './scene-schedule';

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

            const AnimatedSlide: React.FC<{cue: SceneCue; globalFrame: number}> = ({cue, globalFrame}) => {
              const localFrame = Math.max(0, globalFrame - cue.from);
              const supportingSpeaker = cue.mode === 'speaker-support';
              const split = cue.mode === 'split';
              const panelLeft = supportingSpeaker ? '61%' : split ? '6%' : '6%';
              const panelTop = supportingSpeaker ? '24%' : split ? '22%' : '25%';
              const panelWidth = supportingSpeaker ? '34%' : split ? '88%' : '61%';
              const columns = cue.slide.kind === 'comparison' ? 'repeat(2, minmax(0, 1fr))' : cue.slide.kind === 'statement' ? 'repeat(3, minmax(0, 1fr))' : '1fr';
              return (
                <div style={{position: 'absolute', left: panelLeft, top: panelTop, width: panelWidth, padding: split ? 24 : 34, borderRadius: 28, backgroundColor: 'rgba(7, 14, 30, 0.92)', border: '1px solid rgba(103,232,249,0.38)', boxShadow: '0 22px 70px rgba(0,0,0,0.36)', color: 'white', fontFamily: 'Arial, sans-serif', opacity: interpolate(localFrame, [8, 18], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}), translate: interpolate(localFrame, [8, 22], ['0px 24px', '0px 0px'], {easing: Easing.bezier(0.16, 1, 0.3, 1), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>
                  <div style={{fontSize: 15, fontWeight: 900, letterSpacing: 2.4, color: '#67e8f9'}}>{cue.slide.kind.toUpperCase()} / REMOTION</div>
                  <div style={{marginTop: 10, fontSize: split ? 28 : 36, lineHeight: 1.05, fontWeight: 900}}>{cue.slide.title}</div>
                  <div style={{display: 'grid', gridTemplateColumns: columns, gap: 12, marginTop: 24}}>
                    {cue.slide.items.map((item, itemIndex) => {
                      const start = 22 + itemIndex * 10;
                      const active = interpolate(localFrame, [start, start + 8], [0, 1], {easing: Easing.bezier(0.16, 1, 0.3, 1), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
                      return (
                        <div key={item} style={{position: 'relative', minHeight: split ? 82 : 92, padding: '18px 18px 16px', borderRadius: 18, backgroundColor: `rgba(15, 31, 54, ${0.72 + active * 0.22})`, border: `2px solid rgba(103, 232, 249, ${0.16 + active * 0.72})`, opacity: 0.25 + active * 0.75, scale: 0.92 + active * 0.08}}>
                          <div style={{fontSize: 14, fontWeight: 900, color: '#67e8f9'}}>0{itemIndex + 1}</div>
                          <div style={{marginTop: 8, fontSize: split ? 19 : 22, lineHeight: 1.18, fontWeight: 800}}>{item}</div>
                          <div style={{position: 'absolute', left: 0, bottom: 0, height: 4, width: `${active * 100}%`, borderRadius: 999, backgroundColor: itemIndex === cue.slide.items.length - 1 ? '#a3e635' : '#22d3ee'}} />
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            };

            const AnimatedHeadline: React.FC<{text: string; compact: boolean; accentWords?: readonly string[]}> = ({text, compact, accentWords}) => {
              const frame = useCurrentFrame();
              const tokens = text.match(/\\S+\\s*/gu) ?? [text];
              let glyphOffset = 0;
              return (
                <div aria-label={text} style={{display: 'flex', flexWrap: 'wrap', whiteSpace: 'pre-wrap', fontSize: compact ? 38 : 50, lineHeight: 1.06, fontWeight: 800, marginTop: 12, textShadow: '0 3px 20px rgba(0,0,0,0.55)'}}>
                  {tokens.map((token, tokenIndex) => {
                    const tokenGlyphs = Array.from(token);
                    const tokenOffset = glyphOffset;
                    glyphOffset += tokenGlyphs.length;
                    const normalizedToken = token.trim().replace(/[^\\p{L}\\p{N}]+/gu, '').toLocaleLowerCase();
                    const accented = accentWords?.some((word) => word.toLocaleLowerCase() === normalizedToken) ?? false;
                    return (
                      <span key={`${token}-${tokenIndex}`} style={{display: 'inline-block', whiteSpace: 'pre'}}>
                        {tokenGlyphs.map((glyph, glyphIndex) => {
                          const start = Math.min(18, (tokenOffset + glyphIndex) * 1.15);
                          return (
                            <span
                              aria-hidden
                              key={`${glyph}-${glyphIndex}`}
                              style={{
                                display: 'inline-block',
                                color: accented ? '#67e8f9' : 'white',
                                opacity: interpolate(frame, [start, start + 8], [0, 1], {easing: Easing.bezier(0.16, 1, 0.3, 1), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
                                scale: interpolate(frame, [start, start + 10], [0.82, 1], {easing: Easing.spring({damping: 20, stiffness: 260}), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
                                translate: interpolate(frame, [start, start + 9], ['0px 18px', '0px 0px'], {easing: Easing.bezier(0.16, 1, 0.3, 1), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
                              }}
                            >
                              {glyph}
                            </span>
                          );
                        })}
                      </span>
                    );
                  })}
                </div>
              );
            };

            const BeatCopy: React.FC<{from: number; durationInFrames: number; mode: StageMode; eyebrow: string; headline: string; accentWords?: readonly string[]; callout?: string}> = ({from, durationInFrames, mode, eyebrow, headline, accentWords, callout}) => (
              <Sequence from={from} durationInFrames={durationInFrames} premountFor={30}>
                <BeatCopyLocal mode={mode} eyebrow={eyebrow} headline={headline} accentWords={accentWords} callout={callout} />
              </Sequence>
            );

            const BeatCopyLocal: React.FC<{mode: StageMode; eyebrow: string; headline: string; accentWords?: readonly string[]; callout?: string}> = ({mode, eyebrow, headline, accentWords, callout}) => {
              const frame = useCurrentFrame();
              const demonstrationIsPrimary = mode === 'demo-with-pip' || mode === 'demo-detail' || mode === 'split';
              const opacity = interpolate(frame, [0, 12], [0, 1], {easing: Easing.bezier(0.16, 1, 0.3, 1), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
              const y = interpolate(frame, [0, 16], [24, 0], {easing: Easing.bezier(0.16, 1, 0.3, 1), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
              return (
                <div style={{position: 'absolute', left: 72, top: 62, width: demonstrationIsPrimary ? 560 : 760, color: 'white', fontFamily: 'Arial, sans-serif', opacity, translate: `0px ${y}px`, zIndex: 5}}>
                  <div style={{fontSize: 22, fontWeight: 800, letterSpacing: 3, color: '#67e8f9'}}>{eyebrow}</div>
                  <AnimatedHeadline text={headline} compact={demonstrationIsPrimary} accentWords={accentWords} />
                  {callout ? <div style={{display: 'inline-block', marginTop: 18, padding: '10px 16px', borderRadius: 999, backgroundColor: 'rgba(5,12,25,0.82)', border: '1px solid rgba(103,232,249,0.6)', fontSize: 22}}>{callout}</div> : null}
                </div>
              );
            };

            const LiveDemoSteps: React.FC<{from: number; durationInFrames: number; steps: readonly string[]; resultLabel?: string}> = ({from, durationInFrames, steps, resultLabel}) => (
              <Sequence from={from} durationInFrames={durationInFrames} premountFor={30}>
                <LiveDemoStepsLocal steps={steps} resultLabel={resultLabel} />
              </Sequence>
            );

            const LiveDemoStepsLocal: React.FC<{steps: readonly string[]; resultLabel?: string}> = ({steps, resultLabel}) => {
              const frame = useCurrentFrame();
              const railStart = 28;
              const resultStart = railStart + steps.length * 12 + 4;
              return (
                <div style={{position: 'absolute', left: 92, top: 770, display: 'flex', alignItems: 'center', gap: 12, zIndex: 2, fontFamily: 'Arial, sans-serif'}}>
                  {steps.map((step, stepIndex) => {
                    const start = railStart + stepIndex * 12;
                    const active = interpolate(frame, [start, start + 8], [0, 1], {easing: Easing.bezier(0.16, 1, 0.3, 1), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
                    return (
                      <React.Fragment key={step}>
                        {stepIndex > 0 ? <div style={{width: 42, height: 3, borderRadius: 999, backgroundColor: '#67e8f9', transformOrigin: 'left', scale: `${interpolate(frame, [start - 8, start], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} 1`, opacity: 0.85}} /> : null}
                        <div style={{display: 'flex', alignItems: 'center', gap: 10, padding: '11px 16px', borderRadius: 16, backgroundColor: `rgba(5, 12, 25, ${0.72 + active * 0.18})`, border: `2px solid rgba(103, 232, 249, ${0.28 + active * 0.72})`, color: 'white', opacity: 0.38 + active * 0.62, scale: 0.9 + active * 0.1, boxShadow: active > 0.98 ? '0 10px 30px rgba(6,182,212,0.2)' : 'none'}}>
                          <span style={{display: 'grid', placeItems: 'center', width: 26, height: 26, borderRadius: 999, backgroundColor: active > 0.98 ? '#22d3ee' : '#334155', color: '#06101c', fontSize: 16, fontWeight: 900}}>{stepIndex + 1}</span>
                          <span style={{fontSize: 20, fontWeight: 800}}>{step}</span>
                        </div>
                      </React.Fragment>
                    );
                  })}
                  {resultLabel ? (
                    <div style={{marginLeft: 14, padding: '12px 18px', borderRadius: 999, backgroundColor: '#a3e635', color: '#122006', fontSize: 19, fontWeight: 900, letterSpacing: 1.2, opacity: interpolate(frame, [resultStart, resultStart + 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}), scale: interpolate(frame, [resultStart, resultStart + 10], [0.78, 1], {easing: Easing.spring({damping: 18, stiffness: 280}), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>
                      {resultLabel}
                    </div>
                  ) : null}
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
                    <Surface src={demoSrc} label="" muted />
                    <AnimatedSlide cue={cue} globalFrame={frame} />
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
                  {sceneSchedule.map((item) => item.demoSteps ? <LiveDemoSteps key={`${item.id}-demo-steps`} from={item.from} durationInFrames={item.durationInFrames} steps={item.demoSteps} resultLabel={item.resultLabel} /> : null)}

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
