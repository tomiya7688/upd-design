# UPD Review Checklist

[日本語](../レビュー.md)

Use this checklist during implementation and review to verify that responsibilities remain separated. **Mandatory rules do not become optional when an item is skipped.** Refer to [Mandatory boundaries](boundaries.md).

## UI

- [ ] UI handles input and presentation.
- [ ] UI contains no final business or game rule decisions or calculations.
- [ ] UI does not retrieve or persist data directly.
- [ ] UI does not give widgets to Process to manipulate.

## Process

- [ ] Application rules and calculations are implemented in Process.
- [ ] Process does not manipulate widgets or render the screen.
- [ ] Process does not perform direct database or file I/O.
- [ ] Process requests Data work when retrieval or saving is necessary.

## Data

- [ ] Data handles retrieval, persistence, required storage conversions, and I/O error detection.
- [ ] Data does not make business or game rule decisions.
- [ ] Data does not display UI or send results directly to UI.

## Cross-layer communication

- [ ] UI and Data do not communicate directly.
- [ ] Shared helpers or events do not bypass the required boundaries.
- [ ] Exchanged values do not hand another layer internal objects needed to take over its work.
- [ ] Success and failure paths respect the same boundaries.
- [ ] Review considers the actual work, not just the file or type names.

## Check whether separation is useful

The following are design-review prompts rather than additional mandatory violation rules.

- [ ] Can UI-only changes usually avoid rewriting application rules?
- [ ] Can application rule changes be reasoned about independently from storage details?
- [ ] Can Data changes be assessed without coupling directly to screen rendering?
- [ ] Can layer-level and integration tests be written clearly?

Some features legitimately require changes in multiple layers. The key is being able to explain the change and each layer's responsibility.

[Back to developer guide](README.md).
