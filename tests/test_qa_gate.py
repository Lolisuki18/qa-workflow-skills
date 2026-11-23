"""Tests for scripts/qa-gate.py (stdlib unittest)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GATE = Path(__file__).resolve().parent.parent / "scripts" / "qa-gate.py"


class QaGateTests(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.root = Path(self._td.name)
        (self.root / "qa-artifacts").mkdir()

    def tearDown(self):
        self._td.cleanup()

    def write(self, name, status):
        (self.root / "qa-artifacts" / name).write_text(f"# x\n- **Status:** {status}\n", encoding="utf-8")

    def run_gate(self, target, env=None, raw=None):
        payload = raw if raw is not None else json.dumps(
            {"cwd": str(self.root), "tool_input": {"file_path": str(self.root / target)}})
        e = {**os.environ, **(env or {})}
        return subprocess.run([sys.executable, str(GATE)], input=payload, capture_output=True, text=True, env=e)

    def test_blocks_matrix_while_plan_is_draft(self):
        self.write("01-test-plan.md", "Draft")
        r = self.run_gate("qa-artifacts/02-test-matrix.md")
        self.assertEqual(r.returncode, 2)
        self.assertIn("still 'Status: Draft'", r.stderr)

    def test_allows_matrix_when_plan_approved(self):
        self.write("01-test-plan.md", "Approved (approved on: 2026-11-23)")
        self.assertEqual(self.run_gate("qa-artifacts/02-test-matrix.md").returncode, 0)

    def test_blocks_execution_while_matrix_is_draft(self):
        self.write("01-test-plan.md", "Approved")
        self.write("02-test-matrix.md", "Draft")
        self.assertEqual(self.run_gate("qa-artifacts/03-execution-notes.md").returncode, 2)

    def test_nonfunctional_design_needs_approved_plan(self):
        self.write("01-test-plan.md", "Draft")
        self.assertEqual(self.run_gate("qa-artifacts/02b-nonfunctional.md").returncode, 2)

    def test_editing_the_prerequisite_itself_is_allowed(self):
        self.write("01-test-plan.md", "Draft")
        self.assertEqual(self.run_gate("qa-artifacts/01-test-plan.md").returncode, 0)

    def test_defects_and_summary_are_never_blocked(self):
        self.write("01-test-plan.md", "Draft")
        self.write("02-test-matrix.md", "Draft")
        self.assertEqual(self.run_gate("qa-artifacts/04-defects.md").returncode, 0)
        self.assertEqual(self.run_gate("qa-artifacts/05-summary-report.md").returncode, 0)

    def test_missing_prerequisite_is_allowed(self):
        self.assertEqual(self.run_gate("qa-artifacts/02-test-matrix.md").returncode, 0)

    def test_files_outside_qa_artifacts_are_ignored(self):
        self.write("01-test-plan.md", "Draft")
        self.assertEqual(self.run_gate("src/app.py").returncode, 0)

    def test_bypass_env_and_marker_file(self):
        self.write("01-test-plan.md", "Draft")
        self.assertEqual(self.run_gate("qa-artifacts/02-test-matrix.md", env={"QA_GATE": "off"}).returncode, 0)
        (self.root / "qa-artifacts" / ".no-gate").write_text("", encoding="utf-8")
        self.assertEqual(self.run_gate("qa-artifacts/02-test-matrix.md").returncode, 0)

    def test_fails_open_on_bad_input(self):
        self.assertEqual(self.run_gate("x", raw="not json").returncode, 0)


if __name__ == "__main__":
    unittest.main()
