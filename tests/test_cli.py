import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

from game_polish.cli import create_run, cycle_warnings, default_config, load_config, main, write_json


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "game-polish.json"
        self.config = default_config("Test")
        self.config["checks"] = {"test": {"argv": [sys.executable, "-c", "print('verified')"], "timeout_seconds": 2}}
        self.save()

    def save(self):
        write_json(self.path, self.config)

    def test_config(self):
        self.assertEqual(load_config(self.path)[1], self.root)

    def test_init_does_not_overwrite(self):
        before = self.path.read_text()
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["init", str(self.root)]), 2)
        self.assertEqual(self.path.read_text(), before)

    def test_plan_does_not_execute(self):
        self.config["checks"]["test"]["argv"] = ["nonexistent-program-game-polish"]
        self.save()
        directory, manifest = create_run(self.path, "baseline", False, None, None)
        self.assertEqual(manifest["status"], "planned")
        self.assertEqual(manifest["checks"]["test"]["status"], "not_run")
        self.assertFalse((directory / "test.log").exists())

    def test_execute_and_baseline(self):
        directory, manifest = create_run(self.path, "baseline", True, None, None)
        self.assertEqual(manifest["status"], "passed")
        self.assertEqual((directory / "test.log").read_text().strip(), "verified")
        after, result = create_run(self.path, "run", True, None, str(directory))
        self.assertNotEqual(directory, after)
        self.assertEqual(result["baseline"], str(directory))
        self.assertEqual(result["regression"]["status"], "no_check_regression")
        self.assertIsNone(result["budget"]["tokens_used"])
        self.assertIn("source_after", result)
        self.assertEqual(json.loads((after / "observations.json").read_text())["decision"], "pending")
        self.assertIn("not proof of visual quality", (after / "report.md").read_text())

    def test_failed_check(self):
        self.config["checks"]["test"]["argv"] = [sys.executable, "-c", "raise SystemExit(7)"]
        self.save()
        _, manifest = create_run(self.path, "run", True, None, None)
        self.assertEqual(manifest["status"], "failed")
        self.assertEqual(manifest["checks"]["test"]["exit_code"], 7)

    def test_recorded_gdx_output_compatibility(self):
        fixtures = Path(__file__).parent / "fixtures"
        for fixture in ("gdx-capture-success.json", "gdx-start-success.json"):
            self.config["checks"]["test"].update(expect_json_ok=True, argv=[sys.executable, "-c", "import pathlib,sys; print(pathlib.Path(sys.argv[1]).read_text())", str(fixtures / fixture)])
            self.save()
            _, result = create_run(self.path, "run", True, None, None)
            self.assertEqual(result["status"], "passed")
            self.assertTrue(result["checks"]["test"]["json_ok"])

    def test_json_success_contract(self):
        self.config["checks"]["test"]["expect_json_ok"] = True
        for output, expected in (("{\"ok\":true}", "passed"), ("{\"ok\":false}", "failed"), ("no JSON", "failed")):
            self.config["checks"]["test"]["argv"] = [sys.executable, "-c", f"print({output!r})"]
            self.save()
            _, result = create_run(self.path, "run", True, None, None)
            self.assertEqual(result["status"], expected)

    def test_missing_executable(self):
        self.config["checks"]["test"]["argv"] = ["nonexistent-program-game-polish"]
        self.save()
        _, manifest = create_run(self.path, "run", True, None, None)
        self.assertEqual(manifest["checks"]["test"]["status"], "error")
        self.assertEqual(manifest["status"], "failed")

    def test_timeout(self):
        self.config["checks"]["test"] = {"argv": [sys.executable, "-c", "import time; time.sleep(10)"], "timeout_seconds": 1}
        self.save()
        _, manifest = create_run(self.path, "run", True, None, None)
        self.assertEqual(manifest["checks"]["test"]["status"], "timed_out")

    def test_unsafe_check_name(self):
        self.config["checks"]["../escape"] = self.config["checks"].pop("test")
        self.save()
        with self.assertRaises(ValueError):
            load_config(self.path)

    def test_cycle_capability_feedback(self):
        self.config["cycle"] = {"interval_minutes": 60, "max_tokens": 20000}
        self.save()
        warnings = cycle_warnings(self.config)
        self.assertEqual(len(warnings), 2)
        self.assertIn("UNSUPPORTED", warnings[1])
        output = io.StringIO()
        with contextlib.redirect_stderr(output), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(["validate", "--config", str(self.path)]), 0)
        self.assertIn("no schedule has been created", output.getvalue())
        self.assertIn("tokens_used remains null", output.getvalue())

    def test_invalid_cycle_budget(self):
        self.config["cycle"] = {"max_tokens": -1}
        self.save()
        with self.assertRaises(ValueError):
            load_config(self.path)

    def test_invalid_timeout(self):
        for value in (True, 0, -1, 3601, "60"):
            self.config["checks"]["test"]["timeout_seconds"] = value
            self.save()
            with self.assertRaises(ValueError):
                load_config(self.path)

    def test_invalid_selection_and_baseline(self):
        with self.assertRaises(ValueError):
            create_run(self.path, "run", False, ["unknown"], None)
        directory, _ = create_run(self.path, "baseline", False, None, None)
        with self.assertRaises(ValueError):
            create_run(self.path, "run", True, None, str(directory))

    def test_baseline_comparison_flags_changed_commands(self):
        directory, _ = create_run(self.path, "baseline", True, None, None)
        self.config["checks"]["test"]["argv"][-1] = "print('changed')"
        self.save()
        _, manifest = create_run(self.path, "run", True, None, str(directory))
        self.assertEqual(manifest["comparison"]["status"], "different_checks")

    def test_evidence_symlink_escape(self):
        with tempfile.TemporaryDirectory() as external:
            (self.root / ".game-polish").symlink_to(external, target_is_directory=True)
            with self.assertRaises(ValueError):
                create_run(self.path, "run", False, None, None)

    def test_evidence_placeholder(self):
        self.config["checks"]["test"]["argv"] = [sys.executable, "-c", "import pathlib,sys; pathlib.Path(sys.argv[1]).write_text('evidence')", "{evidence_dir}/result.txt"]
        self.save()
        directory, manifest = create_run(self.path, "run", True, None, None)
        self.assertEqual(manifest["status"], "passed")
        self.assertEqual((directory / "evidence/result.txt").read_text(), "evidence")


if __name__ == "__main__":
    unittest.main()
