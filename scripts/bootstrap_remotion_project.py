#!/usr/bin/env python3
"""Create a pinned minimal Remotion project without invoking Git or create-video."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


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


def files_for(root: Path, versions: dict[str, str]) -> dict[Path, str]:
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
    return {
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
            "  <Composition id=\"Main\" component={Main} durationInFrames={150} fps={30} width={1920} height={1080} />\n"
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--remotion-version", default=DEFAULT_VERSIONS["remotion"])
    parser.add_argument("--force", action="store_true", help="Replace only generated files; never removes other files")
    args = parser.parse_args()
    versions = dict(DEFAULT_VERSIONS)
    versions["remotion"] = args.remotion_version
    root = args.output.expanduser().resolve()
    generated = files_for(root, versions)
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
                "next": ["npm install", "npm run browser:ensure", "npm run studio"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
