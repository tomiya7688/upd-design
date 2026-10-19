import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_layers import check, main


class LanguageDependenciesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for layer in ("ui", "process", "data", "shared"):
            (self.root / "src" / layer).mkdir(parents=True)
        self.conf = {
            "source_roots": ["src"],
            "layers": {layer: [f"src/{layer}"] for layer in ("ui", "process", "data", "shared")},
        }
        self.write("upd-check.json", json.dumps(self.conf))

    def write(self, path, value):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(value, encoding="utf-8")

    def findings(self):
        return check(self.root, self.conf)

    def assert_violation(self):
        self.assertIn("UPD100", [f.code for f in self.findings()])

    def assert_ok(self):
        self.assertEqual(self.findings(), [])

    def test_csharp_forbidden_using(self):
        self.write("src/data/Store.cs", "namespace Demo.Data;\npublic class Store {}\n")
        self.write("src/ui/View.cs", "using Demo.Data;\nnamespace Demo.Ui;\npublic class View {}\n")
        self.assert_violation()

    def test_csharp_allowed_using(self):
        self.write("src/data/Store.cs", "namespace Demo.Data;\npublic class Store {}\n")
        self.write("src/process/Logic.cs", "using Demo.Data;\nnamespace Demo.Process;\npublic class Logic {}\n")
        self.assert_ok()

    def test_csharp_alias_using(self):
        self.write("src/data/Store.cs", "namespace Demo.Data;\n")
        self.write("src/ui/View.cs", "using DB = Demo.Data.Store;\n")
        self.assert_violation()

    def test_kotlin_forbidden_import(self):
        self.write("src/data/Store.kt", "package demo.data\nclass Store\n")
        self.write("src/ui/View.kt", "package demo.ui\nimport demo.data.Store\n")
        self.assert_violation()

    def test_kotlin_allowed_import(self):
        self.write("src/data/Store.kt", "package demo.data\nclass Store\n")
        self.write("src/process/Logic.kt", "package demo.process\nimport demo.data.Store\n")
        self.assert_ok()

    def test_go_forbidden_import(self):
        self.write("go.mod", "module example.com/updtest\n\ngo 1.22\n")
        self.write("src/data/store.go", "package data\nfunc Read() {}\n")
        self.write("src/ui/view.go", 'package ui\nimport "example.com/updtest/src/data"\n')
        self.assert_violation()

    def test_go_allowed_import(self):
        self.write("go.mod", "module example.com/updtest\n\ngo 1.22\n")
        self.write("src/data/store.go", "package data\n")
        self.write("src/process/logic.go", 'package process\nimport (\n "fmt"\n db "example.com/updtest/src/data"\n)\n')
        self.assert_ok()

    def test_go_requires_go_mod(self):
        self.write("src/ui/view.go", "package ui\n")
        self.assertIn("UPD004", [f.code for f in self.findings()])

    def test_rust_forbidden_crate_path(self):
        self.write("src/data/store.rs", "pub fn read() {}\n")
        self.write("src/ui/view.rs", "use crate::data::store;\n")
        self.assert_violation()

    def test_rust_allowed_crate_path(self):
        self.write("src/data/store.rs", "")
        self.write("src/process/logic.rs", "use crate::data::store;\n")
        self.assert_ok()

    def test_rust_super_path(self):
        self.write("src/data/store.rs", "")
        self.write("src/ui/mod.rs", "use super::data::store;\n")
        self.assert_violation()

    def test_cpp_forbidden_include(self):
        self.write("src/data/store.hpp", "#pragma once\n")
        self.write("src/ui/view.cpp", '#include "../data/store.hpp"\n')
        self.assert_violation()

    def test_cpp_allowed_include(self):
        self.write("src/data/store.hpp", "#pragma once\n")
        self.write("src/process/logic.cpp", '#include "../data/store.hpp"\n#include <vector>\n')
        self.assert_ok()

    def test_cpp_include_source_root_path(self):
        self.write("src/data/store.h", "")
        self.write("src/ui/view.cc", '#include "data/store.h"\n')
        self.assert_violation()

    def test_cpp_relative_unknown_fails(self):
        self.write("src/ui/view.cpp", '#include "../data/missing.hpp"\n')
        self.assertIn("UPD004", [f.code for f in self.findings()])

    def test_nadesiko3_forbidden_import(self):
        self.write("src/data/読込.nako3", "「ok」と表示。\n")
        self.write("src/ui/画面.nako3", "!「../data/読込.nako3」を取り込む\n")
        self.assert_violation()

    def test_nadesiko3_allowed_import(self):
        self.write("src/data/読込.nako3", "「ok」と表示。\n")
        self.write("src/process/処理.nako3", "!『../data/読込.nako3』を取り込む\n")
        self.assert_ok()

    def test_nadesiko3_dynamic_import_fails(self):
        self.write("src/ui/画面.nako3", "!何かを取り込む\n")
        self.assertIn("UPD004", [f.code for f in self.findings()])

    def test_unclassified_multi_language_fails(self):
        self.write("src/misc.kt", "package demo\n")
        self.assertIn("UPD002", [f.code for f in self.findings()])

    def test_nadesiko1_not_falsely_supported(self):
        self.write("src/ui/script.nako", "「こんにちは」と表示\n")
        self.assertIn("UPD003", [f.code for f in self.findings()])

    def test_multilanguage_in_one_project(self):
        self.write("go.mod", "module example.com/mixed\n")
        self.write("src/ui/view.py", "import json\n")
        self.write("src/process/logic.kt", "package demo.process\n")
        self.write("src/data/store.go", "package data\n")
        self.assert_ok()

    def test_cli_returns_failure_on_violation(self):
        self.write("src/data/Store.cs", "namespace Demo.Data;\n")
        self.write("src/ui/View.cs", "using Demo.Data;\n")
        self.assertEqual(main(["--root", str(self.root), "--config", "upd-check.json"]), 1)


if __name__ == "__main__":
    unittest.main()
