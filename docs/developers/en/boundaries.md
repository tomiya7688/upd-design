# Mandatory UPD Boundaries

[日本語](../境界.md)

**UI, Process, and Data must never take over each other's responsibilities.** These prohibitions apply even to temporary or very small implementations.

UPD does not mandate particular classes, internal components, or communication techniques. These rules state **which layer is responsible for which work**.

## Rule 1: UI must not decide application rules

UI handles input and presentation. Final decisions and calculations based on business or game rules belong to Process.

**Violation:** A purchase-button handler checks a membership tier, calculates a discount, and commits the order.

**Correct separation:** UI passes purchase data to Process. Process checks conditions and calculates the amount. UI displays the result.

UI may highlight an empty input field as a presentation behavior. That UI-level feedback is not a substitute for an application-level eligibility check.

## Rule 2: Process must not manipulate UI or storage directly

Process owns application rules and calculations, not screen elements or database/file operations.

**Violation:** Process changes the color of a label, executes SQL, or writes directly to a file.

**Correct separation:** Process returns state that UI may display. Process asks Data for retrieval or persistence.

Process decides **whether** data should be saved; Data handles **how** the data is saved.

## Rule 3: Data must not make application decisions or update UI

Data handles retrieval and persistence. It does not decide purchase eligibility or a game's winner, and it does not show dialogs.

**Violation:** A retrieval operation decides that a customer is allowed to purchase and presents a warning on screen.

**Correct separation:** Data returns relevant facts and I/O results. Process determines their application meaning; UI presents it.

Detecting connection failures or storage uniqueness constraints belongs to Data. Deciding how the application responds belongs to Process.

## Rule 4: UI and Data must not communicate directly

UI must not send retrieval or persistence requests straight to Data, and Data must not send results or direct updates straight to UI.

    Allowed: UI → Process → Data
    Allowed: Data → Process → UI
    Forbidden: UI → Data
    Forbidden: Data → UI

**Violation:** A screen handler accesses the database, or a Data module pushes a UI update directly.

**Correct separation:** Requests and results pass through Process, including failures.

Switching from calls to events or asynchronous messages does **not** make a boundary bypass acceptable.

## Rule 5: An intermediary does not excuse bypassing a boundary

A shared utility, object, or event mechanism cannot be used to disguise direct access to another layer's work.

**Violation:** UI calls a shared helper that directly invokes a Data save operation, bypassing Process.

**Correct separation:** Shared values and types may be used, but Process must make the relevant decision before Data handles saving.

Judge the actual execution and responsibility flow, not names or folder locations.

## Rule 6: Do not pass internal machinery to another layer to perform your job

Only the values and results required for work should cross layers.

**Violation:** UI hands a widget to Process so Process can manipulate it; Data hands a connection object to UI so UI can execute queries.

**Correct separation:** UI passes the search string; Data returns product values or a save result.

## Rule 7: Data normalizes representation; Process determines meaning

**Data may normalize retrieved data into a consistent representation that Process can use.** This is part of retrieval and data I/O.

**Examples that belong in Data:**

- Convert JSON or CSV into defined types.
- Map source-specific field names to common field names.
- Standardize number and date representations according to a defined schema.
- Normalize character encodings or text representations without changing their meaning.
- Detect parsing errors or missing values and return those facts to Process.

**Examples that belong in Process:**

- Apply membership-based discounts to a price.
- Supply a default for a missing value according to an application rule.
- Decide purchase eligibility or the winner of a game.
- Filter or prioritize results according to application rules.

**The boundary is whether an operation standardizes representation or determines application meaning.** Data must not silently reinterpret values, replace missing or invalid values based on business policy, or discard information in ways that alter its meaning.

For example, when an external service returns `price` as the string `"1200"`, converting it to a defined numeric type belongs to Data. Calculating a membership discount from that number belongs to Process.

Converting values to a storage format when saving also belongs to Data, while **deciding what may be saved belongs to Process**.

## Success and failure must obey the same boundaries

Data must not display a dialog only because storage failed. UI must not decide to retry business persistence directly. Data reports the failure; Process decides the application response; UI presents it.

## Boundaries are independent of implementation mechanisms

A project may use functions, interfaces, events, or asynchronous techniques. Whatever the mechanism, **the responsibilities and the UI–Data boundary are mandatory**.

Related: [Implementation and flow](implementation.md) and [Review checklist](review-checklist.md).
