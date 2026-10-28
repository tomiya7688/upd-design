# Practical UPD Examples

[日本語](../具体例.md)

UPD divides a feature into distinct kinds of work: **input, decisions, data access, and presentation**.

## Example 1: Search for products

A user enters a keyword and presses Search.

| Step | Layer | Responsibility |
| --- | --- | --- |
| 1 | UI | Read the search input |
| 2 | Process | Validate the search condition |
| 3 | Data | Fetch matching products |
| 4 | Process | Prepare the application-level result |
| 5 | UI | Display the product list |

If search ranking is an application rule, it belongs to Process. Choosing a card or table layout is a UI decision.

## Example 2: Save an order

UI sends the selected products and quantities to Process. Process checks the order conditions and performs relevant calculations.

After deciding what should be saved, Process asks Data to persist it. Data returns a save result. Process interprets the outcome for the application and UI displays it.

**Requesting a save is not proof that saving succeeded.** UI must distinguish an accepted request from a confirmed completed operation.

## Example 3: Show the winner of a game

UI accepts player actions. Process applies game rules to determine the winner. UI presents the result.

If the result must be stored, Process asks Data to save it. If nothing needs storage, Data does not need to participate.

## Examples of broken separation

- UI reads a database directly to fetch products.
- UI makes the final decision about purchase eligibility or discounts.
- Data decides who won the game.
- Process changes screen colors or layout.

In each case, one layer takes on another layer's responsibility.

## Remember

Even a single feature, such as Search or Purchase, may include multiple responsibilities. **Separate the work within features, not just the names of features.**

For project-size and workload guidance, see [Projects that benefit from UPD](suitable-projects.md).

For mandatory rules, see [Developer boundary rules](../../developers/en/boundaries.md).
