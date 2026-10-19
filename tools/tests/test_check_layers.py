import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_layers import check, main

CONFIG = {
    "source_roots": ["src"],
    "layers": {
        "ui": ["src/ui"], "process": ["src/process"],
        "data": ["src/data"], "shared": ["src/shared"]
    },
}


class LayerCheckerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("ui", "process", "data", "shared"):
            (self.root / "src" / name).mkdir(parents=True)
            self.write(f"src/{name}/__init__.py", "")
        self.write("config.json", json.dumps(CONFIG))

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def codes(self):
        return [x.code for x in check(self.root, CONFIG)]

    def test_valid(self):
        self.write("src/ui/screen.py", "from process import logic\n")
        self.write("src/process/logic.py", "from data import db\nfrom shared import types\n")
        self.write("src/data/db.py", "from shared import types\n")
        self.write("src/shared/types.py", "VALUE=1\n")
        self.assertEqual(self.codes(), [])
        self.assertEqual(main(["--root", str(self.root), "--config", "config.json"]), 0)

    def test_ui_to_data(self):
        self.write("src/data/db.py", "")
        self.write("src/ui/screen.py", "from data import db\n")
        self.assertIn("UPD100", self.codes())
        self.assertEqual(main(["--root", str(self.root), "--config", "config.json"]), 1)

    def test_relative_import(self):
        self.write("src/data/db.py", "")
        self.write("src/ui/screen.py", "from ..data import db\n")
        self.assertIn("UPD100", self.codes())

    def test_process_to_ui(self):
        self.write("src/ui/screen.py", "")
        self.write("src/process/logic.py", "import ui.screen\n")
        self.assertIn("UPD100", self.codes())

    def test_data_to_process(self):
        self.write("src/process/logic.py", "")
        self.write("src/data/db.py", "from process import logic\n")
        self.assertIn("UPD100", self.codes())

    def test_shared_bypass(self):
        self.write("src/data/db.py", "")
        self.write("src/shared/helper.py", "from data import db\n")
        self.write("src/ui/screen.py", "from shared import helper\n")
        self.assertIn("UPD100", self.codes())

    def test_literal_dynamic_import(self):
        self.write("src/data/db.py", "")
        self.write("src/ui/screen.py", 'import importlib\ndb = importlib.import_module("data.db")\n')
        self.assertIn("UPD100", self.codes())

    def test_missing_module_name_does_not_bypass(self):
        self.write("src/ui/screen.py", "import data.unknown\n")
        self.assertIn("UPD100", self.codes())

    def test_unclassified_source(self):
        self.write("src/helper.py", "VALUE = 1\n")
        self.assertIn("UPD002", self.codes())

    def test_unsupported_language(self):
        self.write("src/ui/view.ts", "export const view = true;\n")
        self.assertIn("UPD003", self.codes())

    def test_syntax_error(self):
        self.write("src/ui/bad.py", "def broken(\n")
        self.assertIn("UPD004", self.codes())

    def test_bad_config(self):
        bad = json.loads(json.dumps(CONFIG))
        bad["layers"]["ui"] = ["src/missing"]
        with self.assertRaises(ValueError):
            check(self.root, bad)

    def test_external_standard_import(self):
        self.write("src/ui/screen.py", "import json\nfrom typing import Optional\n")
        self.assertEqual(self.codes(), [])


if __name__ == "__main__":
    unittest.main()
