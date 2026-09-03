#!/usr/bin/env python3
"""Portable guided project interface for multi-stage video production."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


STAGES = [
    "intake",
    "inventory",
    "transcript",
    "paper-edit",
    "rough-cut",
    "visual-plan",
    "preview",
    "fine-cut",
    "finish",
    "qa",
    "delivered",
]

GATES = {
    "intake": "Record source media, audience, outputs, privacy, and editorial constraints.",
    "inventory": "Inspect streams, duration, frame rate, dimensions, rotation, color, and audio.",
    "transcript": "Create raw transcript, word timestamps when needed, and uncertainty notes.",
    "paper-edit": "Create the narrative outline and keep/remove decisions or edit manifest.",
    "rough-cut": "Produce a playable proxy or rough editable timeline.",
    "visual-plan": "Map claims to purposeful B-roll, graphics, typography, and motion beats.",
    "preview": "Render a preview and representative review frames; collect revision notes.",
    "fine-cut": "Lock timing in the source composition or editable timeline.",
    "finish": "Complete color, audio, captions, and delivery candidates.",
    "qa": "Full-decode every final and record visual/audio review evidence.",
    "delivered": "Keep verified deliverables, editable source, and handoff notes together.",
}

PROJECT_DIRS = [
    "analysis",
    "transcripts",
    "proxies",
    "assets/broll",
    "assets/audio",
    "graphics",
    "remotion",
    "timeline",
    "review",
    "exports",
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def manifest_path(root: Path) -> Path:
    return root / "project.json"


def load(root: Path) -> dict[str, Any]:
    path = manifest_path(root)
    if not path.is_file():
        raise SystemExit(f"No guided project found: {path}\nRun the init command first.")
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    stage = data.get("workflow", {}).get("stage")
    if stage not in STAGES:
        raise SystemExit(f"Invalid workflow stage in {path}: {stage!r}")
    return data


def save(root: Path, data: dict[str, Any]) -> None:
    data["updatedAt"] = now()
    path = manifest_path(root)
    temporary = path.with_suffix(".json.tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.replace(temporary, path)


def rel_or_abs(path: str, root: Path) -> str:
    resolved = Path(path).expanduser().resolve()
    try:
        return resolved.relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(resolved)


def prompt(label: str, default: str) -> str:
    value = input(f"{label} [{default}]: ").strip()
    return value or default


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def command_init(args: argparse.Namespace) -> None:
    root = Path(args.project_root).expanduser().resolve()
    path = manifest_path(root)
    if path.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing project: {path}")

    interactive = not args.non_interactive and sys.stdin.isatty()
    name = args.name or root.name
    kind = args.kind
    audience = args.audience
    target_duration = args.target_duration
    language = args.caption_language
    timeline = args.timeline
    style = args.style
    if interactive:
        name = prompt("Project name", name)
        kind = prompt("Kind (interview/podcast/tutorial/explainer/social)", kind)
        audience = prompt("Audience", audience)
        target_duration = int(prompt("Target duration in seconds (0 = flexible)", str(target_duration)))
        language = prompt("Caption language", language)
        timeline = prompt("Timeline (programmatic/nle/both)", timeline)
        style = prompt("Visual style", style)

    root.mkdir(parents=True, exist_ok=True)
    for directory in PROJECT_DIRS:
        (root / directory).mkdir(parents=True, exist_ok=True)

    aspect_ratios = args.aspect_ratio or ["16:9"]
    sources = [
        {"id": f"source-{index + 1}", "path": rel_or_abs(source, root), "role": "primary" if index == 0 else "supporting"}
        for index, source in enumerate(args.source)
    ]
    created = now()
    data: dict[str, Any] = {
        "schema": "video-production-studio/project@1",
        "project": {"name": name, "kind": kind, "root": str(root)},
        "createdAt": created,
        "updatedAt": created,
        "agentContract": {
            "selfContained": True,
            "requiredAgentSkills": [],
            "entrypoint": "video-production-studio/SKILL.md",
            "stateSource": "project.json",
        },
        "sources": sources,
        "brief": {
            "audience": audience,
            "targetDurationSec": target_duration or None,
            "aspectRatios": aspect_ratios,
            "captionLanguage": language,
            "timelinePreference": timeline,
            "visualStyle": style,
            "mustKeep": args.must_keep,
        },
        "constraints": {
            "offlineOnly": args.offline_only,
            "allowUploads": False,
            "allowPaidServices": False,
            "notes": args.constraint,
        },
        "workflow": {
            "stage": "inventory",
            "stageIndex": 1,
            "gate": GATES["inventory"],
            "history": [
                {"at": created, "event": "initialized", "stage": "intake"},
                {"at": created, "event": "advanced", "from": "intake", "to": "inventory", "artifacts": ["project.json"], "note": "Guided intake captured"},
            ],
            "nextActions": [
                "Inspect every source and save analysis/media-inventory.json.",
                "Verify the brief and source paths while inventorying media.",
                "Advance with the inventory artifact after the inventory gate is satisfied.",
            ],
        },
        "artifacts": [],
        "decisions": [],
        "assumptions": [],
        "uncertainties": [],
        "blockers": [],
        "deliverables": [],
    }
    save(root, data)
    print(f"Initialized guided video project: {path}")
    print_summary(data)


def open_blockers(data: dict[str, Any]) -> list[dict[str, Any]]:
    return [item for item in data.get("blockers", []) if item.get("status") == "open"]


def progress_bar(index: int) -> str:
    width = 22
    filled = round((index / (len(STAGES) - 1)) * width)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def print_summary(data: dict[str, Any]) -> None:
    workflow = data["workflow"]
    stage = workflow["stage"]
    index = STAGES.index(stage)
    print(f"\n{data['project']['name']}")
    print(f"{progress_bar(index)} {index}/{len(STAGES) - 1}  {stage}")
    print(f"Gate: {GATES[stage]}")
    print(f"Sources: {len(data.get('sources', []))} | Artifacts: {len(data.get('artifacts', []))} | Open blockers: {len(open_blockers(data))}")
    actions = workflow.get("nextActions", [])
    if actions:
        print("Next:")
        for item in actions:
            print(f"  - {item}")
    if open_blockers(data):
        print("Blocked by:")
        for number, item in enumerate(open_blockers(data), start=1):
            print(f"  {number}. {item['reason']}")


def command_status(args: argparse.Namespace) -> None:
    print_summary(load(Path(args.project_root).expanduser().resolve()))


def resolve_executable(name: str, root: Path) -> str | None:
    env_key = f"VIDEO_{name.upper().replace('-', '_')}_BIN"
    configured = os.environ.get(env_key)
    if configured:
        candidate = Path(configured).expanduser()
        if candidate.is_file():
            return str(candidate.resolve())
    found = shutil.which(name)
    if found:
        return found
    suffixes = [".exe", ".cmd", ""] if os.name == "nt" else [""]
    bases = [root / ".video-tools", root / "tools" / name, root / "vendor" / name / "bin"]
    for base in bases:
        for suffix in suffixes:
            candidate = base / f"{name}{suffix}"
            if candidate.is_file():
                return str(candidate.resolve())
    return None


def module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def command_doctor(args: argparse.Namespace) -> None:
    root = Path(args.project_root).expanduser().resolve() if args.project_root else Path.cwd().resolve()
    executable_names = [
        "ffmpeg",
        "ffprobe",
        "node",
        "npm",
        "npx",
        "git",
        "nvidia-smi",
        "rocm-smi",
        "google-chrome",
        "chromium",
        "msedge",
    ]
    executables = {name: resolve_executable(name, root) for name in executable_names}
    local_remotion_candidates = [
        root / "node_modules" / ".bin" / "remotion.cmd",
        root / "node_modules" / ".bin" / "remotion",
        root / "node_modules" / "remotion" / "package.json",
    ]
    local_remotion = next((str(path.resolve()) for path in local_remotion_candidates if path.exists()), None)
    modules = {name: module_available(name) for name in ["faster_whisper", "whisper", "whisperx", "PIL"]}
    has_ffmpeg = bool(executables["ffmpeg"] and executables["ffprobe"])
    has_node = bool(executables["node"] and executables["npm"] and executables["npx"])
    has_asr = any(modules[name] for name in ["faster_whisper", "whisper", "whisperx"])
    has_gpu = bool(executables["nvidia-smi"] or executables["rocm-smi"])
    disk = shutil.disk_usage(root if root.exists() else root.parent)
    disk_free_gib = round(disk.free / (1024**3), 2)
    fallbacks: list[str] = []
    if not has_ffmpeg:
        if has_node and local_remotion:
            fallbacks.append("Probe the installed Remotion CLI for bundled ffmpeg/ffprobe commands; otherwise keep planning and timeline artifacts until a media backend is available.")
        else:
            fallbacks.append("Continue with brief, transcript supplied by the user, storyboard, shot plan, and EDL; encoded delivery and full-decode QA remain unavailable.")
    if not has_asr:
        fallbacks.append("Use supplied SRT/VTT/transcript or request timed text; never invent word timestamps.")
    if not has_node or not local_remotion:
        if has_ffmpeg:
            fallbacks.append("Use FFmpeg for cuts, captions, simple overlays, audio, and exports; preserve a Remotion-ready visual manifest for later enhancement.")
        else:
            fallbacks.append("Produce the Remotion source plan and asset manifest without claiming a preview or render.")
    if not has_gpu:
        fallbacks.append("Use CPU-safe ASR, smaller models, proxies, lower preview scale, low render concurrency, or chunked rendering.")
    if not any(executables[name] for name in ["google-chrome", "chromium", "msedge"]):
        fallbacks.append("Use supplied screenshots/recordings or extracted source frames instead of live browser capture.")
    if disk_free_gib < 10:
        fallbacks.append("Free space is limited: proxy first, reuse caches, estimate peak render storage, and render in validated chunks.")
    report = {
        "selfContainedAgentSkill": True,
        "requiredAgentSkills": [],
        "projectRoot": str(root),
        "platform": {"system": platform.system(), "release": platform.release(), "machine": platform.machine()},
        "python": sys.executable,
        "executables": executables,
        "pythonModules": modules,
        "localRemotion": local_remotion,
        "diskFreeGiB": disk_free_gib,
        "features": {
            "guidedProject": True,
            "timelineAndShotPlanning": True,
            "ffmpegEditing": has_ffmpeg,
            "localTranscription": bool(has_ffmpeg and has_asr),
            "gpuAcceleration": has_gpu,
            "remotionScaffoldPossible": has_node,
            "remotionRuntimePresent": bool(has_node and local_remotion),
        },
        "fallbacks": fallbacks,
    }
    if args.write:
        if not args.project_root:
            raise SystemExit("--write requires --project-root pointing to an initialized guided project.")
        data = load(root)
        data["environmentProfile"] = report
        data["workflow"]["history"].append({
            "at": now(),
            "event": "environment-probed",
            "readyFeatures": [name for name, ready in report["features"].items() if ready],
            "fallbackCount": len(fallbacks),
        })
        save(root, data)
        report["writtenTo"] = str(manifest_path(root))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    print("Video Production Studio environment")
    print("Agent skill dependencies: none")
    print(f"Project root: {root}")
    print(f"Python: {sys.executable}")
    for name, path in executables.items():
        print(f"{name}: {path or 'not found'}")
    for name, available in modules.items():
        print(f"{name}: {'available' if available else 'not found'}")
    print(f"local Remotion: {local_remotion or 'not found'}")
    print(f"free disk: {disk_free_gib} GiB")
    print("Features:")
    for name, available in report["features"].items():
        print(f"  - {name}: {'ready' if available else 'unavailable'}")
    if fallbacks:
        print("Fallback plan:")
        for item in fallbacks:
            print(f"  - {item}")


def command_advance(args: argparse.Namespace) -> None:
    root = Path(args.project_root).expanduser().resolve()
    data = load(root)
    if open_blockers(data):
        raise SystemExit("Cannot advance while open blockers exist. Resolve them first.")
    current = data["workflow"]["stage"]
    index = STAGES.index(current)
    if current == "delivered":
        raise SystemExit("Project is already delivered.")
    if not args.artifact:
        raise SystemExit("At least one --artifact is required as gate evidence.")
    missing = []
    artifacts = []
    for raw in args.artifact:
        candidate = Path(raw).expanduser()
        if not candidate.is_absolute():
            candidate = root / candidate
        if not candidate.exists():
            missing.append(str(candidate))
        artifacts.append(rel_or_abs(str(candidate), root))
    if missing:
        raise SystemExit("Artifact does not exist:\n" + "\n".join(missing))

    timestamp = now()
    for path in artifacts:
        data["artifacts"].append({"stage": current, "path": path, "registeredAt": timestamp})
    if args.note:
        data["decisions"].append({"at": timestamp, "stage": current, "note": args.note})
    next_stage = STAGES[index + 1]
    data["workflow"].update({
        "stage": next_stage,
        "stageIndex": index + 1,
        "gate": GATES[next_stage],
        "nextActions": [GATES[next_stage], "Register gate evidence, then advance one stage."],
    })
    data["workflow"]["history"].append({
        "at": timestamp,
        "event": "advanced",
        "from": current,
        "to": next_stage,
        "artifacts": artifacts,
        "note": args.note or "",
    })
    save(root, data)
    print_summary(data)


def command_block(args: argparse.Namespace) -> None:
    root = Path(args.project_root).expanduser().resolve()
    data = load(root)
    item = {"reason": args.reason, "status": "open", "openedAt": now()}
    data["blockers"].append(item)
    data["workflow"]["history"].append({"at": item["openedAt"], "event": "blocked", "reason": args.reason})
    save(root, data)
    print_summary(data)


def command_unblock(args: argparse.Namespace) -> None:
    root = Path(args.project_root).expanduser().resolve()
    data = load(root)
    blockers = open_blockers(data)
    if args.index < 1 or args.index > len(blockers):
        raise SystemExit(f"Open blocker index must be between 1 and {len(blockers)}.")
    item = blockers[args.index - 1]
    item.update({"status": "resolved", "resolvedAt": now(), "resolution": args.note})
    data["workflow"]["history"].append({"at": item["resolvedAt"], "event": "unblocked", "reason": item["reason"], "note": args.note})
    save(root, data)
    print_summary(data)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Guided, resumable video-production project interface")
    commands = parser.add_subparsers(dest="command", required=True)

    doctor = commands.add_parser("doctor", help="Report executable capabilities; no other agent skill is required")
    doctor.add_argument("--project-root", help="Inspect local tools and packages relative to this project")
    doctor.add_argument("--write", action="store_true", help="Persist the environment profile in an initialized project.json")
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(func=command_doctor)

    init = commands.add_parser("init", help="Create folders and a portable project.json")
    init.add_argument("--project-root", required=True)
    init.add_argument("--source", action="append", required=True, help="Source media path; repeat for multiple files")
    init.add_argument("--name")
    init.add_argument("--kind", default="talking-head")
    init.add_argument("--audience", default="general audience")
    init.add_argument("--target-duration", type=int, default=0)
    init.add_argument("--aspect-ratio", action="append")
    init.add_argument("--caption-language", default="auto")
    init.add_argument("--timeline", choices=["programmatic", "nle", "both"], default="both")
    init.add_argument("--style", default="content-driven, polished, restrained")
    init.add_argument("--must-keep", action="append", default=[])
    init.add_argument("--constraint", action="append", default=[])
    init.add_argument("--offline-only", action=argparse.BooleanOptionalAction, default=True)
    init.add_argument("--non-interactive", action="store_true")
    init.add_argument("--force", action="store_true", help="Replace project.json only; never deletes media or project folders")
    init.set_defaults(func=command_init)

    status = commands.add_parser("status", help="Show progress, gate, blockers, and next actions")
    status.add_argument("--project-root", required=True)
    status.set_defaults(func=command_status)

    advance = commands.add_parser("advance", help="Register gate evidence and advance exactly one stage")
    advance.add_argument("--project-root", required=True)
    advance.add_argument("--artifact", action="append", required=True)
    advance.add_argument("--note")
    advance.set_defaults(func=command_advance)

    block = commands.add_parser("block", help="Record a user or external blocker")
    block.add_argument("--project-root", required=True)
    block.add_argument("--reason", required=True)
    block.set_defaults(func=command_block)

    unblock = commands.add_parser("unblock", help="Resolve an open blocker by displayed index")
    unblock.add_argument("--project-root", required=True)
    unblock.add_argument("--index", type=int, required=True)
    unblock.add_argument("--note", required=True)
    unblock.set_defaults(func=command_unblock)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
