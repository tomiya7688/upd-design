# UPD Boundary Checker

[日本語](../README.md)

These tools aim to **fail checks when a supported UPD boundary violation is detected**. The authoritative rules are documented in [Mandatory UPD Boundaries](../../docs/developers/en/boundaries.md).

## Initial language support

| Language | File extensions | Static reference forms currently examined |
| --- | --- | --- |
| Python | `.py` | `import`, `from`, and selected constant-string dynamic imports (Python AST) |
| C# | `.cs` | Namespace declarations and `using`, including aliases and `global using` |
| Rust | `.rs` | Explicit references using `crate::` and `super::` |
| Go | `.go` | Local package imports resolved using `go.mod` |
| Kotlin | `.kt`, `.kts` | Package declarations and `import` |
| C++ | `.cpp`, `.cc`, `.cxx`, `.h`, `.hpp`, `.hh`, `.hxx` | Quoted local `#include` directives |
| Nadesiko 3 | `.nako3` | Local file inclusion using the language's literal inclusion directive |

**This is not complete parsing or full language support.** Only representative forms of static dependencies are examined. Nadesiko 1 files (`.nako` and `.nako2`) are explicitly unsupported.

## Permitted and prohibited dependencies

| Source layer | Permitted target layers | Prohibited targets |
| --- | --- | --- |
| UI | UI, Process, Shared | Data |
| Process | Process, Data, Shared | UI |
| Data | Data, Shared | UI, Process |
| Shared (optional) | Shared | UI, Process, Data |

Shared is not a fourth processing layer. It must not be used to bypass the boundaries. A return value flowing from Data to Process does not mean Data needs to import Process implementation details.

## Configuration

Place an `upd-check.json` file in the consuming project. The directory names below are examples, not prescribed UPD names.

```json
{
  "source_roots": ["src"],
  "layers": {
    "ui": ["src/ui"],
    "process": ["src/process"],
    "data": ["src/data"],
    "shared": ["src/shared"]
  }
}
```

Configured directories must exist. Omit `shared` if the project does not have a shared directory. Include all relevant source files under the configured source roots.

## Running the checker

The checker runs using Python 3.11 or later and requires only the Python standard library.

```sh
python /path/to/upd-design/tools/check_layers.py --root /path/to/project --config upd-check.json
```

C# and Kotlin match imports against namespaces and packages found in the inspected source. Go resolves local packages via `go.mod`. Rust infers module positions from paths. C++ and Nadesiko 3 match references to local files.

## Exit codes and diagnostics

| Exit code | Meaning |
| --- | --- |
| 0 | No violation was found **within the supported static-reference forms** |
| 1 | A boundary violation, unclassified source, recognized unsupported extension, resolution error, or empty inspection target |
| 2 | Inspection could not start because of an invalid configuration or other setup error |

A diagnostic reports the path, line, rule code, and forbidden source/target layers. For example, a report for `src/ui/View.cs` might indicate an `ui → data` reference to `Demo.Data` with rule code `UPD100`. The current CLI's diagnostic messages are in Japanese.

Configure the checker as a required CI job in each consuming project. A nonzero result must fail that job.

## Limitations

**A passing result is not a certification of compliance with all UPD rules.** Business calculations written directly inside UI, for example, may not trigger a dependency checker.

Current unsupported areas include:

- **C#:** Fully qualified references without `using`, semantic analysis of conditional compilation and generated code.
- **Rust:** Macros, grouped `use` declarations, path attributes, and complex module layouts.
- **Go:** Local layouts without `go.mod`, build tags, generated files, and runtime behavior.
- **Kotlin:** Fully qualified references without `import` and runtime behavior.
- **C++:** Angle-bracket includes, macro-based includes, build-system include paths, and call graphs.
- **Nadesiko 3:** External plugins, repository or URL imports, runtime references, and calls that do not use literal file inclusion.
- **Across languages:** Cross-language runtime call graphs, full lexical interpretation of comments and strings, semantic analysis of application responsibilities, files outside configured source roots, and unknown source extensions.

Do not claim unimplemented syntax has been validated. Proper parsers, build metadata integration, and semantic responsibility checks are future work.

## Tests and CI

```sh
python -m unittest discover -s tools/tests -v
```

The GitHub Actions workflow in this repository tests **the checker itself**. Each consuming project must separately integrate the checker to enforce its own boundaries.

For Nadesiko 3 syntax, see the [official Nadesiko 3 repository](https://github.com/kujirahand/nadesiko3) and the [language author's article](https://qiita.com/kujirahand/items/bdbf611fc1f448e63bf9).
