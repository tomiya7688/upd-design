# UPD Developer Guide

[日本語](../README.md)

This guide is for people implementing and reviewing code using UPD.

**UPD separates the responsibilities of UI, Process, and Data, and these boundaries must be maintained.** Judge responsibilities by what the code actually does, not by a directory or class name.

## Responsibilities of each layer

| Layer | Responsible for | Must not own |
| --- | --- | --- |
| UI | Reading input, presentation formatting, rendering, view state | Final application rule decisions, retrieving or saving data |
| Process | Business and game rules, calculations, workflow decisions | Rendering and screen controls, direct database or file I/O |
| Data | Reading and writing data, storage-format conversion, detection of I/O errors | UI operations, business and game rule decisions |

The [mandatory boundaries](boundaries.md) are requirements, not suggestions.

## Direction of work

    Requests: UI → Process → Data
    Results:  Data → Process → UI

This describes responsibilities, not a particular function, messaging, or event mechanism. Not every operation must visit all three layers.

## Implementing a feature

First break the feature into input/presentation, rules/calculation, and retrieval/persistence. Then decide which values cross the boundaries and how results and errors are represented.

Finally check that each layer performs only its own work.

**Freedom to choose an implementation technique is not freedom to cross responsibility boundaries.**

## Boundary checking

Automated checks are developed in the [tools directory](../../../tools/en/README.md). Detected violations cause failures, but current coverage is limited; consult [checker guidance](checker.md) and continue reviewing the actual work performed.

## Detailed documentation

- [Mandatory boundaries](boundaries.md) — Prohibited responsibilities and bypasses
- [Implementation and flow](implementation.md) — Assigning responsibilities and passing results
- [Review checklist](review-checklist.md) — Verifying code changes
- [Boundary checker](checker.md) — CI integration and current limitations

For an introduction, see the [user guide](../../users/en/README.md).
