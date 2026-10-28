# Understanding UPD (User Guide)

[日本語](../README.md)

UPD is a design approach that divides application responsibilities into **UI, Process, and Data**. A *layer* means a group of related responsibilities.

UPD is not an application or library. It is a way to decide **which part of an application is responsible for which kind of work**.

**UPD is intended for projects with an external interface.** That interface can serve people, devices, or other systems.

## Why separate the work?

When screen updates, application decisions, and database operations are mixed into a single function, even a small change can require reviewing unrelated behavior.

UPD separates work that changes for different reasons.

| Type of work | Layer | Examples |
| --- | --- | --- |
| Interacting with the outside world | **UI** | Accept a button press or a request from another system and return a result |
| Application rules and calculations | **Process** | Check purchase eligibility and calculate discounts |
| Reading and writing data | **Data** | Search for products and save an order |

Calculating a discount and displaying the resulting price in red are different tasks. The calculation belongs to Process; the presentation belongs to UI.

## Respecting boundaries

**When using UPD, the boundaries between the three layers must not be violated.**

UI requests application work from Process instead of reading or writing data itself. Process makes decisions and requests data work from Data when needed. Data returns its results to Process, and UI decides how to display the application result.

    UI → Process → Data
    UI ← Process ← Data

This does not mean every operation must pass through all three layers. Opening an information panel may need UI alone; a calculation requiring no stored data may use only UI and Process.

**Do not move a layer's responsibility into another layer.** Three directories do not create real separation if the actual work remains mixed together.

## What are the benefits?

It becomes easier to reason about changes to screen presentation, application rules, or storage independently. Tests and investigations can focus on a narrower responsibility.

This does not guarantee that every change is limited to one layer. Changes to exchanged data or cross-cutting features may still require modifications in several places.

See [Benefits of UPD](benefits.md).

## Which projects are a good fit?

**UPD is not suited to closed autonomous projects without external interaction.** When an external interface exists, judge its suitability by the responsibilities that need separating, not project size alone. See [Projects that benefit from UPD](suitable-projects.md).

## Read next

- [Benefits of UPD](benefits.md) — Advantages and trade-offs
- [Projects that benefit from UPD](suitable-projects.md) — Suitability by size and workload
- [Practical examples](examples.md) — Search, saving an order, and game rules
- [Mandatory developer boundaries](../../developers/en/boundaries.md) — Detailed rules
