"""Semantic regression checks for the Feishu export cleanup.

Run with: python3 -m unittest discover -s tests -v
Fixtures retain the raw lines, so valid LaTeX subscripts are never repaired by
blindly replacing repeated letters in already-polished documents.
"""
import contextlib
import io
import json
from pathlib import Path
import runpy
import string
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "feishu_polish.py"
FIXTURES = json.loads((ROOT / "tests/fixtures/feishu_formula_regressions.json").read_text(encoding="utf-8"))


def load_cleanup():
    # The existing CLI intentionally runs at module scope; load it against an
    # empty temporary export, never against the real reference documents.
    with tempfile.TemporaryDirectory() as empty, patch.object(sys, "argv", [str(SCRIPT), empty]):
        with contextlib.redirect_stdout(io.StringIO()):
            return runpy.run_path(str(SCRIPT))["fix_math"]


fix_math = load_cleanup()


class FormulaCleanupTests(unittest.TestCase):
    def test_duplicate_variables_are_not_subscripts(self):
        for variable in string.ascii_letters + "αβγΔλπθϵϕ":
            with self.subTest(variable=variable):
                self.assertEqual(fix_math(f"{variable}*{variable}*"), f"${variable}$")

    def test_multicharacter_duplicates(self):
        for source, expected in [("dmodel*dmodel*", "$d_{model}$"), ("λU*λU*", "$λ_U$"), ("BA*BA*", "$BA$")]:
            with self.subTest(source=source):
                self.assertEqual(fix_math(source), expected)

    def test_distinct_subscripts_and_other_garbled_shapes(self):
        examples = {
            "W*K*": "$W_K$", "S*t*": "$S_t$", "L*D*": "$L_D$",
            "*W*0": "$W_0$", "*L*max": "$L_{max}$",
            "n=8*n*=8": "$n=8$", "B0*B*0": "$B_0$",
            "πref*π*ref": r"$\pi_{ref}$", "2*i*": "$2i$",
            "4*d*": "$4d$", "Δ*W*": r"$\Delta W$",
        }
        for source, expected in examples.items():
            with self.subTest(source=source):
                self.assertEqual(fix_math(source), expected)

    def test_existing_math_code_and_emphasis_are_preserved(self):
        for source in ["$W_W$", "$i_i$", "$$W*W* + i_i$$", "`W*W*`",
                       "```python\nW*W*\n```", "**中文强调**", "*中文强调*", "**W**", "*PPO*"]:
            with self.subTest(source=source):
                self.assertEqual(fix_math(source), source)

    def test_mixed_protected_and_raw_formula(self):
        self.assertEqual(fix_math("`W*W*` 与 W*W*，$i_i$ 与 i*i*"),
                         "`W*W*` 与 $W$，$i_i$ 与 $i$")

    def test_all_73_regression_source_lines(self):
        cases = FIXTURES["cases"]
        self.assertEqual(len(cases), 73)
        self.assertEqual(len({case["path"] for case in cases}), 38)
        for case in cases:
            with self.subTest(path=case["path"], raw=case["raw"]):
                self.assertEqual(fix_math(case["raw"]), case["expected"])

    def test_corrected_lines_are_checked_in(self):
        for case in FIXTURES["cases"]:
            with self.subTest(path=case["path"], expected=case["expected"]):
                text = (ROOT / case["path"]).read_text(encoding="utf-8")
                self.assertIn(case["expected"], text)

    def test_formula_cleanup_is_idempotent(self):
        for case in FIXTURES["cases"]:
            with self.subTest(path=case["path"]):
                once = fix_math(case["raw"])
                self.assertEqual(fix_math(once), once)

    def test_cli_preserves_ocr_pdf_and_is_repeatable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "_ocr").mkdir()
            (root / "_ocr/example.md").write_text("OCR formula: $W_W$", encoding="utf-8")
            (root / "manual.pdf.md").write_text("W*W*", encoding="utf-8")
            (root / "example.md").write_text("W*W*，W*K*\n\n![screenshot](media/example.png)\n", encoding="utf-8")
            run = lambda: subprocess.run([sys.executable, str(SCRIPT), str(root)], text=True,
                                         capture_output=True, check=True)
            first = run()
            result = (root / "example.md").read_text(encoding="utf-8")
            self.assertIn("$W$，$W_K$", result)
            self.assertIn("OCR formula: $W_W$", result)
            self.assertIn("![原图](media/example.png){.ocr-src}", result)
            self.assertEqual((root / "manual.pdf.md").read_text(encoding="utf-8"), "W*W*")
            self.assertEqual((root / "_ocr/example.md").read_text(encoding="utf-8"), "OCR formula: $W_W$")
            self.assertIn("polished 1 files", first.stdout)
            second = run()
            self.assertIn("polished 0 files", second.stdout)
            self.assertEqual((root / "example.md").read_text(encoding="utf-8"), result)


if __name__ == "__main__":
    unittest.main()
