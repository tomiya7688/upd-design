# Implementation and Data Flow

[日本語](../実装.md)

Before implementing a feature, ask: **What kind of work does this operation perform?** UPD separates work by responsibility, not by its function name or programming syntax.

## Decide where work belongs

1. **Does the task receive user input or change presentation?** Use UI.
2. **Does it make a business or game decision, or perform a calculation?** Use Process.
3. **Does it retrieve or persist data?** Use Data.
4. **Does it perform several types of work?** Split the work and assign the parts to their respective layers.

A name such as "conversion" is insufficient to determine a layer.

| Operation | Layer | Why |
| --- | --- | --- |
| Format an amount as a user-facing currency string | UI | Presentation |
| Calculate a discount based on membership level | Process | Application rule |
| Convert a date into a storage format | Data | Persistence |
| Show a loading indicator | UI | View state |
| Decide whether to save data | Process | Application decision |
| Detect a storage failure | Data | I/O result |

## Product search

    UI: Read search input
      ↓
    Process: Validate search conditions
      ↓
    Data: Retrieve products
      ↓
    Process: Prepare the application result
      ↓
    UI: Display the results

UI passes the search string rather than the search widget. Data returns product values rather than its storage connection.

When a search condition is invalid, Process can return an error to UI without calling Data.

## Saving data

    UI: Pass input values
      ↓
    Process: Decide whether the data is valid to save
      ↓
    Data: Save the data and return the outcome
      ↓
    Process: Interpret the outcome
      ↓
    UI: Present the result

"Saving should be attempted" and "Saving succeeded" are separate facts. UI must not announce success before completion has been confirmed.

## Returning failures

Data reports facts such as connection failures. Process determines whether to retry or return a failure at the application level. UI determines how the result is displayed.

The mechanism may be a return value, exception, or asynchronous notification. The **Data → Process → UI** responsibility flow must remain intact.

## What to decide after separation

UPD does not mandate folder names, class names, numbers of functions, or a communication style. For each boundary, clarify the input values, results, and failures exchanged.

Test each layer's behavior independently and also verify the entire exchange across boundaries.

See [Mandatory boundaries](boundaries.md) and [Review checklist](review-checklist.md).
