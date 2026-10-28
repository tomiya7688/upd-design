# Benefits of UPD

[日本語](../メリット.md)

The goal of UPD is to **make different kinds of work distinct in the code**. Dividing responsibilities into UI, Process, and Data helps with changes, verification, and reuse.

The benefits below are **expected when responsibilities are actually separated**. Merely labeling a project "UPD" does not guarantee these outcomes.

## 1. Easier to understand the impact of a change

For display changes, start with UI. For business or game rules, start with Process. For storage and retrieval methods, start with Data.

For example, changing a product list from a table to cards should not normally require rewriting search rules or data retrieval.

**The reason for a change gives you a starting point for deciding which code to inspect.**

## 2. Easier to investigate defects

If a discount amount is incorrect, investigate Process first. If the displayed amount is formatted incorrectly, investigate UI. If a saved order cannot be read, start with Data.

The cause is not guaranteed to be in that layer, but separating responsibilities provides a useful investigation path.

## 3. More focused tests

Process rules and calculations can be tested without driving a screen. UI tests can focus on presentation, while Data tests focus on retrieval and persistence.

Separate integration tests can then verify that results and errors cross the boundaries correctly.

## 4. More flexible screens and storage

When application rules are kept in Process, the same behavior is easier to reuse from different screens.

Similarly, changing the database or storage technique can often be handled mainly inside Data. If the meaning or structure of values exchanged between layers changes, other layers may also require updates.

## 5. Clearer ownership during development

A shared vocabulary for display work, rule work, and data work makes implementation and review responsibilities easier to discuss.

This does not require a separate developer or team for each layer. It can help a solo developer too.

## Trade-offs

Separation requires designing the values passed between layers and deciding how success and failure are represented. On small features, this may add code and review work.

**If boundaries are not enforced, the benefits diminish.** A shortcut that accesses storage directly from a screen may be convenient today, but can increase the impact of later changes.

UPD is not a promise of speed or quality by itself. It is a design discipline for **continuing to keep unlike responsibilities separate**.

For guidance on project size and workload characteristics, see [Projects that benefit from UPD](suitable-projects.md).

Next: [Practical examples](examples.md).
