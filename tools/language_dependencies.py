"""Limited static cross-layer reference scanners for six additional languages.

This module does NOT claim to parse or semantically validate the full languages.
Unresolved implicit/runtime references and duty violations need further analyzers.
"""
from __future__ import annotations

import re
from pathlib import Path

LANGUAGE_SUFFIXES = {
    ".cs": "csharp",
    ".rs": "rust",
    ".go": "go",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".hpp": "cpp",
    ".hh": "cpp",
    ".hxx": "cpp",
    ".h": "cpp",
    ".nako3": "nadesiko3",
}

NAMESPACE = {
    "csharp": re.compile(r"^\s*namespace\s+([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\b", re.M),
    "kotlin": re.compile(r"^\s*package\s+([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\b", re.M),
}
CS_USING = re.compile(
    r"^\s*(?:global\s+)?using\s+(?:static\s+)?(?:[A-Za-z_]\w*\s*=\s*)?"
    r"([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\s*;", re.M
)
KT_IMPORT = re.compile(r"^\s*import\s+([A-Za-z_]\w*(?:\.[A-Za-z_]\w*|\.\*)*)", re.M)
RUST_REF = re.compile(r"\b(crate|super(?:::\s*super)*)\s*::\s*([A-Za-z_]\w*(?:::\w+)*)")
CPP_INCLUDE = re.compile(r'^\s*#\s*include\s*"([^"\n]+)"', re.M)
NAKO_IMPORT = re.compile(r"^\s*!\s*[「『]([^」』]+)[」』]\s*を取り込む")


def inside(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def strip_comments(text: str) -> str:
    """Leave lines in place; remove // and /* */ comments (not a full lexer)."""
    return re.sub(
        r"/\*.*?\*/|//[^\n]*",
        lambda m: "\n" * m.group(0).count("\n"),
        text,
        flags=re.S,
    )


def line_at(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def module_prefixes(value: str):
    parts = value.split(".")
    return [".".join(parts[:n]) for n in range(len(parts), 0, -1)]


def collect_namespaces(sources):
    """Map namespaces declared by project source files to layers."""
    index = {"csharp": {}, "kotlin": {}}
    for path, _src, layer in sources:
        lang = LANGUAGE_SUFFIXES.get(path.suffix.lower())
        if lang not in index:
            continue
        text = strip_comments(path.read_text(encoding="utf-8-sig"))
        for match in NAMESPACE[lang].finditer(text):
            index[lang].setdefault(match.group(1), set()).add(layer)
    return index


def go_module(file: Path, root: Path):
    for directory in (file.parent, *file.parents):
        if not inside(directory, root):
            break
        go_mod = directory / "go.mod"
        if go_mod.is_file():
            contents = go_mod.read_text(encoding="utf-8")
            match = re.search(r'^\s*module\s+"?([^"\s]+)"?', contents, re.M)
            if match:
                return match.group(1).strip(), directory
            return None
    return None


def collect_go_packages(root, sources):
    namespaces = {}
    missing = []
    for path, _src, layer in sources:
        if path.suffix != ".go":
            continue
        module = go_module(path, root)
        if module is None:
            missing.append(path)
            continue
        name, module_dir = module
        suffix = path.parent.relative_to(module_dir).as_posix()
        pkg = name + ("/" + suffix if suffix != "." else "")
        namespaces.setdefault(pkg, set()).add(layer)
    return namespaces, missing


def go_imports(text):
    in_block = False
    for i, line in enumerate(text.splitlines(), 1):
        line = line.split("//", 1)[0].strip()
        if in_block:
            if line.startswith(")"):
                in_block = False
            elif match := re.match(r'(?:\w+|_|\.)?\s*"([^"]+)"', line):
                yield i, match.group(1)
        elif re.match(r"^import\s*\(", line):
            in_block = True
        elif match := re.match(r'^import\s+(?:\w+\s+|_\s+|\.\s+)?"([^"]+)"', line):
            yield i, match.group(1)


def rust_target(path, src, match):
    keyword, symbol = match.group(1), match.group(2)
    parts = symbol.split("::")
    if keyword == "crate":
        location = src
    else:
        rel = list(path.relative_to(src).parts)
        if rel[-1] in ("mod.rs", "lib.rs", "main.rs"):
            rel.pop()
        else:
            rel[-1] = rel[-1].removesuffix(".rs")
        levels = keyword.count("super")
        if levels > len(rel):
            return None
        location = src.joinpath(*rel[:-levels])
    return location.joinpath(*parts).resolve()


def resolve_cpp(path, src, symbol):
    for candidate in ((path.parent / symbol), (src / symbol)):
        candidate = candidate.resolve()
        if inside(candidate, src) and candidate.is_file():
            return candidate
    return None


def check_other(root, sources, mapping, allowed):
    """Yield (relative_path, line, diagnostic_code, message)."""
    namespaces = collect_namespaces(sources)
    go_packages, no_go_mod = collect_go_packages(root, sources)
    for path, src, layer in sources:
        lang = LANGUAGE_SUFFIXES[path.suffix.lower()]
        label = path.relative_to(root).as_posix()
        if path in no_go_mod:
            yield label, 1, "UPD004", "Go の go.mod が見つかりません（import先を解決できません）"
            continue
        try:
            original = path.read_text(encoding="utf-8-sig")
        except UnicodeError as exc:
            yield label, 1, "UPD004", f"UTF-8 を解析できません: {exc}"
            continue
        content = strip_comments(original) if lang != "nadesiko3" else original

        def emit(line, targets, ref):
            for target in sorted(targets):
                if target not in allowed[layer]:
                    yield label, line, "UPD100", f"禁止された層間依存: {layer} → {target} ({ref})"

        if lang in ("csharp", "kotlin"):
            expression = CS_USING if lang == "csharp" else KT_IMPORT
            for match in expression.finditer(content):
                value = match.group(1).removesuffix(".*")
                targets = set()
                for prefix in module_prefixes(value):
                    targets = namespaces[lang].get(prefix, set())
                    if targets:
                        break
                yield from emit(line_at(content, match.start()), targets, value)

        elif lang == "go":
            for line, imp in go_imports(content):
                yield from emit(line, go_packages.get(imp, set()), imp)

        elif lang == "rust":
            for match in RUST_REF.finditer(content):
                target_path = rust_target(path, src, match)
                if target_path:
                    for target, dirs in mapping.items():
                        if any(inside(target_path, d) for d in dirs):
                            yield from emit(line_at(content, match.start()), {target}, match.group(0))
                            break

        elif lang == "cpp":
            for match in CPP_INCLUDE.finditer(content):
                name = match.group(1)
                target_path = resolve_cpp(path, src, name)
                if target_path:
                    for target, dirs in mapping.items():
                        if any(inside(target_path, d) for d in dirs):
                            yield from emit(line_at(content, match.start()), {target}, name)
                            break
                elif name.startswith(("./", "../")):
                    yield label, line_at(content, match.start()), "UPD004", f"相対 include を解決できません: {name}"

        elif lang == "nadesiko3":
            for line, value in enumerate(content.splitlines(), 1):
                trimmed = value.strip()
                if trimmed.startswith("#"):
                    continue
                match = NAKO_IMPORT.match(value)
                if not match:
                    if trimmed.startswith("!") and ("取り込む" in trimmed):
                        yield label, line, "UPD004", "取り込み先を静的に解決できません"
                    continue
                name = match.group(1)
                if name.startswith(("http://", "https://", "拡張プラグイン:", "貯蔵庫:")):
                    continue
                candidates = [(path.parent / name).resolve(), (src / name).resolve()]
                target_path = next((p for p in candidates if inside(p, root) and p.is_file()), None)
                if target_path:
                    for target, dirs in mapping.items():
                        if any(inside(target_path, d) for d in dirs):
                            yield from emit(line, {target}, name)
                            break
                elif name.startswith(("./", "../")):
                    yield label, line, "UPD004", f"取り込み先のファイルが見つかりません: {name}"
