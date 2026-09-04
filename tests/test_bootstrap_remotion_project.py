import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "bootstrap_remotion_project.py"


class BootstrapRemotionProjectTests(unittest.TestCase):
    def test_talking_head_demo_template_has_continuous_stage_and_schedule(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "remotion"
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "--template", "talking-head-demo"],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            report = json.loads(completed.stdout)
            self.assertEqual(report["template"], "talking-head-demo")
            schedule = (root / "src" / "talk-demo" / "scene-schedule.ts").read_text(encoding="utf-8")
            composition = (root / "src" / "talk-demo" / "TalkingHeadDemo.tsx").read_text(encoding="utf-8")
            package = json.loads((root / "package.json").read_text(encoding="utf-8"))
            self.assertIn("demo-with-pip", schedule)
            self.assertIn("speaker-return", schedule)
            self.assertIn("focusTarget", schedule)
            self.assertIn("demoSteps", schedule)
            self.assertIn("resultLabel", schedule)
            self.assertEqual(composition.count("<Surface src={speakerSrc}"), 1)
            self.assertIn("sceneSchedule.map", composition)
            self.assertIn("const AnimatedHeadline", composition)
            self.assertIn("Array.from(token)", composition)
            self.assertIn("accentWords", schedule)
            self.assertIn("const LiveDemoSteps", composition)
            self.assertIn("RESULT VERIFIED", schedule)
            self.assertEqual(package["dependencies"]["@remotion/media"], package["dependencies"]["remotion"])

    def test_minimal_template_remains_default(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "remotion"
            subprocess.run([sys.executable, str(SCRIPT), str(root)], check=True, capture_output=True, text=True)
            self.assertTrue((root / "src" / "Composition.tsx").is_file())
            self.assertFalse((root / "src" / "talk-demo").exists())

    def test_cli_reports_unicode_project_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "视频项目"
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(root)],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            report = json.loads(completed.stdout)
            self.assertEqual(Path(report["project"]), root.resolve())


if __name__ == "__main__":
    unittest.main()
