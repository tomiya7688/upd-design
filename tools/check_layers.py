#!/usr/bin/env python3
"""UPD: Python import-based layer boundary checker (standard library only)."""
from __future__ import annotations

import argparse
import ast
import json
import sys
from dataclasses import dataclass
from pathlib import Path

UNSUPPORTED = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".cs", ".java", ".go", ".rs", ".kt", ".swift", ".rb", ".php", ".dart", ".cpp", ".cc", ".c", ".h", ".hpp"}
ALLOWED = {
    "ui": {"ui", "process", "shared"},
    "process": {"process", "data", "shared"},
    "data": {"data", "shared"},
    "shared": {"shared"},
}


@dataclass(frozen=True, order=True)
class Finding:
    path: str
    line: int
    code: str
    message: str

    def __str__(self):
        return f"{self.path}:{self.line}: {self.code} {self.message}"


def within(path, parent):
    return path == parent or parent in path.parents


def resolve_config(root, config):
    if not isinstance(config, dict):
        raise ValueError("設定はJSONオブジェクトにしてください")
    roots = config.get("source_roots")
    layers = config.get("layers")
    if not isinstance(roots, list) or not roots or not all(isinstance(x, str) and x.strip() for x in roots):
        raise ValueError("source_roots を指定してください")
    if not isinstance(layers, dict) or set(layers) - set(ALLOWED) or not {"ui", "process", "data"} <= set(layers):
        raise ValueError("layers に ui、process、data が必要です（shared は任意）")

    def paths(values, key):
        if not isinstance(values, list) or not values or not all(isinstance(x, str) and x.strip() for x in values):
            raise ValueError(f"{key} はパスの配列にしてください")
        result = []
        for value in values:
            path = (root / value).resolve()
            if not within(path, root) or not path.is_dir():
                raise ValueError(f"{key} の指定先が不正です: {value}")
            result.append(path)
        return result

    source_roots = paths(roots, "source_roots")
    mapping = {name: paths(values, name) for name, values in layers.items()}
    dirs = [(name, path) for name, paths_ in mapping.items() for path in paths_]
    for i, (name, path) in enumerate(dirs):
        if not any(within(path, src) for src in source_roots):
            raise ValueError(f"層のディレクトリは source_roots の中に置いてください: {path}")
        for other, peer in dirs[i + 1:]:
            if within(path, peer) or within(peer, path):
                raise ValueError(f"層のディレクトリが重複しています: {name} と {other}")
    for i, src in enumerate(source_roots):
        if any(within(src, peer) or within(peer, src) for peer in source_roots[i + 1:]):
            raise ValueError("source_roots が重複しています")
    return source_roots, mapping


def layer_of(path, mapping):
    for name, dirs in mapping.items():
        if any(within(path, directory) for directory in dirs):
            return name
    return None


def module_name(path, source_root):
    parts = list(path.relative_to(source_root).with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def imported_modules(tree, package):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield node.lineno, alias.name
        elif isinstance(node, ast.Call) and node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
            fn = node.func
            if (isinstance(fn, ast.Name) and fn.id == "__import__") or (
                isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name)
                and fn.value.id == "importlib" and fn.attr == "import_module"
            ):
                yield node.lineno, node.args[0].value
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                parts = package.split(".") if package else []
                if node.level > len(parts) + 1:
                    yield node.lineno, "<invalid relative import>"
                    continue
                prefix = parts[:max(0, len(parts) - node.level + 1)]
                base = ".".join(prefix + ([node.module] if node.module else []))
            else:
                base = node.module or ""
            for alias in node.names:
                if alias.name == "*":
                    if base:
                        yield node.lineno, base
                else:
                    yield node.lineno, f"{base}.{alias.name}" if base else alias.name


def check(root, config):
    roots, mapping = resolve_config(root, config)
    findings, sources, namespaces = [], [], []
    for src in roots:
        for layer, paths in mapping.items():
            for path in paths:
                if within(path, src):
                    name = ".".join(path.relative_to(src).parts)
                    if name:
                        namespaces.append((name, layer))
                        if src.name.isidentifier():
                            namespaces.append((f"{src.name}.{name}", layer))
        for path in sorted(src.rglob("*")):
            if not path.is_file() or any(part in {"__pycache__", ".git", "node_modules"} for part in path.parts):
                continue
            label = path.relative_to(root).as_posix()
            if path.suffix in UNSUPPORTED:
                findings.append(Finding(label, 1, "UPD003", f"未対応言語: {path.suffix}"))
            elif path.suffix == ".py":
                layer = layer_of(path.resolve(), mapping)
                if layer is None:
                    findings.append(Finding(label, 1, "UPD002", "未分類のPythonソース"))
                else:
                    sources.append((path, src, layer))
    if not sources:
        findings.append(Finding("<source_roots>", 1, "UPD005", "検査可能なPythonソースがありません"))

    modules = {}
    for path, src, layer in sources:
        name = module_name(path, src)
        if name:
            modules[name] = layer
            if src.name.isidentifier():
                modules[f"{src.name}.{name}"] = layer

    for path, src, layer in sources:
        label = path.relative_to(root).as_posix()
        try:
            tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=label)
        except (SyntaxError, UnicodeError) as exc:
            findings.append(Finding(label, getattr(exc, "lineno", 1) or 1, "UPD004", f"解析不能: {exc}"))
            continue
        name = module_name(path, src)
        package = name if path.name == "__init__.py" else ".".join(name.split(".")[:-1])
        for line, imported in imported_modules(tree, package):
            if imported == "<invalid relative import>":
                findings.append(Finding(label, line, "UPD004", "相対importの階層が不正です"))
                continue
            parts = imported.split(".")
            prefixes = [".".join(parts[:i]) for i in range(len(parts), 0, -1)]
            target = next((modules[p] for p in prefixes if p in modules), None)
            if target is None:
                matches = [(len(n), owner) for n, owner in namespaces if imported == n or imported.startswith(n + ".")]
                if matches:
                    target = max(matches)[1]
            if target and target not in ALLOWED[layer]:
                findings.append(Finding(label, line, "UPD100", f"禁止された層間依存: {layer} → {target} ({imported})"))
    return sorted(set(findings))


def main(argv=None):
    parser = argparse.ArgumentParser(description="UPD Python層間importチェッカー")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    config_path = args.config if args.config.is_absolute() else root / args.config
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        findings = check(root, config)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"UPD001 検査開始失敗: {exc}", file=sys.stderr)
        return 2
    for finding in findings:
        print(finding)
    if findings:
        print(f"UPD: {len(findings)} 件の違反・未検査項目", file=sys.stderr)
        return 1
    print("UPD: Python静的importの対応範囲で違反なし（責務の意味は未検証）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
