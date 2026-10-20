# Using the Boundary Checker

[日本語](../検査ツール.md)

UPD boundary violations must be fixed before changes are accepted.

Consult [the checker documentation](../../../tools/en/README.md) and run the tool as a required step in the consuming project's CI.

## Supported languages

The initial scanner checks representative static-reference syntax in **Python, C#, Rust, Go, Kotlin, C++, and Nadesiko 3**.

It does not fully understand every language, syntax form, or responsibility. The precise supported forms and limitations are listed in [the tools guide](../../../tools/en/README.md).

## Handling violations

Detected forbidden references, unclassified sources, unsupported recognized file extensions, resolution errors, and configuration failures cause non-zero exit status.

Do not hide problematic files by removing them from the declared scanning roots.

This repository's GitHub Actions workflow tests **the checker itself**. To enforce boundaries in a consuming project, integrate the checker into that project's CI and configure it as a required check.

## Limitations

If UI directly calculates a business discount without importing another layer, the current dependency-based checker may miss it. Fully qualified references, macros, and dynamic references also have language-specific gaps.

**A passing check does not certify compliance with every UPD rule.** Continue using the [mandatory boundaries](boundaries.md) and [review checklist](review-checklist.md).

Improve analysis coverage rather than allowing exceptions that would conceal actual violations.
