# UPD Design

[日本語](../README.md)

**UPD is a design approach that separates an application's work into UI, Process, and Data.**

The important part is not the names of directories or classes. It is **keeping different responsibilities separate**.

| Layer | Responsibility |
| --- | --- |
| **UI** | Accept user input and present results |
| **Process** | Apply application rules, make decisions, perform calculations, and coordinate work |
| **Data** | Retrieve and store data |

## Boundaries are mandatory

Each UPD layer must stay within its responsibility. In particular, **UI and Data must not communicate directly**.

    Requests: UI → Process → Data
    Results:  Data → Process → UI

This shows the flow of responsibilities, not a mandated class structure or communication mechanism. Not every action needs all three layers.

## Documentation

### [For users](../docs/users/en/README.md)

- [Understanding UPD](../docs/users/en/README.md) — What is separated and why
- [Benefits of UPD](../docs/users/en/benefits.md) — Benefits and trade-offs
- [Practical examples](../docs/users/en/examples.md) — Search, saving, and game logic

### [For developers](../docs/developers/en/README.md)

- [Developer guide](../docs/developers/en/README.md) — Responsibilities and implementation approach
- [Mandatory boundaries](../docs/developers/en/boundaries.md) — Prohibitions and violation examples
- [Implementation and data flow](../docs/developers/en/implementation.md) — Assigning responsibilities and passing results
- [Review checklist](../docs/developers/en/review-checklist.md) — What to verify in code reviews
- [Boundary checker](../docs/developers/en/checker.md) — CI integration and current limitations

## Tools

The [tools directory](../tools/en/README.md) contains work on automated checks that fail when supported boundary violations are detected.

The initial static-reference checker covers representative syntax in **Python, C#, Rust, Go, Kotlin, C++, and Nadesiko 3**. It does not detect every responsibility violation. Consult the [tool documentation](../tools/en/README.md) for the exact scope.

## Documentation languages

Japanese is the default language for the root `README.md`. Other Japanese documents use Japanese filenames; English documents use English filenames. A language-switch link appears at the top of every document.

## License

[MIT License](../LICENSE)
