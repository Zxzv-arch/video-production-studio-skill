import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "video_project.py"


class RenderModeTests(unittest.TestCase):
    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_new_project_defaults_to_draft_and_can_promote(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            source = Path(temporary) / "source.mp4"
            source.touch()

            initialized = self.run_cli(
                "init",
                "--non-interactive",
                "--project-root",
                str(root),
                "--source",
                str(source),
            )
            self.assertIn("Render mode: draft", initialized.stdout)
            data = json.loads((root / "project.json").read_text(encoding="utf-8"))
            self.assertEqual(data["renderPlan"]["activeMode"], "draft")

            promoted = self.run_cli(
                "render-mode",
                "--project-root",
                str(root),
                "--set",
                "review",
                "--note",
                "Complete sequence ready",
            )
            self.assertIn("Render mode: review", promoted.stdout)
            data = json.loads((root / "project.json").read_text(encoding="utf-8"))
            self.assertEqual(data["renderPlan"]["activeMode"], "review")
            self.assertEqual(data["workflow"]["history"][-1]["event"], "render-mode-changed")
            self.assertEqual(data["workflow"]["history"][-1]["from"], "draft")
            self.assertEqual(data["workflow"]["history"][-1]["to"], "review")

    def test_status_treats_missing_render_plan_as_legacy_draft(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            source = Path(temporary) / "source.mp4"
            source.touch()
            self.run_cli(
                "init",
                "--non-interactive",
                "--project-root",
                str(root),
                "--source",
                str(source),
            )
            path = root / "project.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            del data["renderPlan"]
            path.write_text(json.dumps(data), encoding="utf-8")

            status = self.run_cli("status", "--project-root", str(root))
            self.assertIn("Render mode: draft", status.stdout)


if __name__ == "__main__":
    unittest.main()
