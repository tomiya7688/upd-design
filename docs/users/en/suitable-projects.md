# Projects Suited to UPD

[日本語](../向いているプロジェクト.md)

**UPD is intended for projects with an interface to the outside world.**

UI is not limited to a screen for human users. It also includes an interface that accepts requests and returns results to people, devices, or other systems. Data handles retrieval and storage.

**UPD is not suited to self-contained projects that operate autonomously without any external interface.**

## Suitability by size

| Size | Suitability | Example |
| --- | --- | --- |
| Small | Depends on the work involved | An expense tracker with input, calculations, and saving can benefit. A display-only app gains little. |
| Medium | Particularly suitable | Reservation or inventory management with distinct input, decision, and data responsibilities. |
| Large | Useful, but other design decisions are needed | E-commerce and business systems. UPD separates responsibilities; it does not define feature boundaries or operations. |

Size is only a guideline. First ask **whether the project has an external interface and responsibilities worth separating**.

## Workloads that fit well

- **Responding to external requests:** Reservation handling or commands received from a device.
- **Numerous rules and calculations:** Pricing, stock decisions, game outcomes.
- **Multiple data sources or stores:** Databases, CSV files, external APIs.
- **Shared rules behind several interfaces:** Customer and administration interfaces.

## Poor fits

- **Closed autonomous processes with no external interaction:** There is no UI role to separate.
- **Display-only pages or simple one-off operations:** Separation may offer little benefit.

A communication device can use UPD even when no human operates it. However, **having an external interface does not automatically make UPD the best fit**.

Related: [Benefits of UPD](benefits.md), [Examples](examples.md), and [Boundary rules](../../developers/en/boundaries.md).
