# Projects That Benefit from UPD

[日本語](../向いているプロジェクト.md)

UPD separates application responsibilities into **UI (input and presentation), Process (decisions and calculations), and Data (retrieval and persistence)**.

**The main consideration is not the number of lines of code or developers, but whether these responsibilities change for different reasons.** The small, medium, and large categories below are qualitative guidelines rather than fixed thresholds.

## Suitability by project size

| Size | Suitability | Example and rationale |
| --- | --- | --- |
| **Small** | **Useful in some cases** | A personal finance tracker or record-keeping app can benefit when presentation, calculation rules, and persistence need separate changes and tests. For a display-only utility, the cost of separation may outweigh the benefit. |
| **Medium** | **Often a particularly good fit** | Inventory, reservation, and order-management systems tend to have several screens, business rules, and data operations. Separating those responsibilities makes their interactions easier to reason about. |
| **Large** | **Useful, but insufficient on its own** | An e-commerce platform or organization-wide business system can apply UPD within features. It will still need additional decisions about feature boundaries, permissions, concurrency, deployment, and operations. |

**Medium-sized business applications are a particularly clear example of where UPD can help.** This does not exclude smaller projects with substantial rules or larger systems that need responsibility separation.

## Workloads that tend to fit UPD

### 1. Many application rules, decisions, and calculations

Examples include discounts, fees, inventory allocation, reservation eligibility, and game rules.

When a pricing rule changes, keeping that calculation in Process makes it easier to verify separately from UI formatting and data persistence.

### 2. The same rules are used from several interfaces

An application may have a customer-facing interface and an administration interface. Their layouts differ, but their eligibility checks or calculations may be shared.

Separating UI from Process makes it easier to reuse those application rules without tying them to one screen.

### 3. Multiple or changing data sources

Applications may read from a database, CSV files, and external APIs, or change their storage methods over time.

Data handles I/O and **normalizes source-specific representations** so Process can work with consistent values. Business defaults and other decisions that assign application meaning remain in Process.

### 4. Success, failure, and testing matter

Saving an order, confirming a reservation, or updating a record requires distinguishing an attempted operation from a completed one.

Data reports the I/O outcome, Process determines the application response, and UI presents it. Separate responsibilities make both focused tests and cross-layer tests easier to design.

## Concrete project examples

| Project | UI | Process | Data |
| --- | --- | --- | --- |
| **Personal finance tracker (small–medium)** | Expense entry, summary display | Category totals, budget-limit decisions | Record persistence, CSV format normalization |
| **Inventory and order management (medium)** | Product search, order entry, inventory view | Purchase eligibility, stock allocation, pricing | Retrieving and saving stock and orders |
| **Reservation management (medium–large)** | Date/time selection, availability display | Booking conditions, slot eligibility | Reading and writing reservations |
| **E-commerce platform (large)** | Product pages, cart, payment-result display | Coupon eligibility, price calculation, order decisions | Product, order, and customer data I/O |
| **Game with saving (any size)** | Player input, game screens and results | Scoring, rules, win/loss calculations | Save-file I/O |

These are **illustrative uses of UPD**, not claims that a project should adopt UPD based on industry or size alone.

## When UPD may have limited value

- **A mostly static website:** There is little application decision-making or persistence to separate.
- **A one-off conversion script:** The entire operation may be simple enough that separation introduces more work than benefit.
- **A very simple single-screen prototype:** If behavior is minimal and unlikely to evolve, the immediate benefit may be limited.

Even a seemingly small feature can benefit from UPD when rules, data sources, or change requirements grow.

**Choosing not to adopt UPD is different from adopting it and violating its boundaries.** Once a project adopts UPD, the [mandatory boundary rules](../../developers/en/boundaries.md) apply regardless of scale.

## Questions to ask before adopting UPD

- Are presentation, application rules, and data access likely to change independently?
- Do business calculations or decisions need tests independent of UI and storage?
- Will several interfaces reuse the same rules, or will several data sources be involved?
- Is the expected benefit worth the ongoing work of defining and enforcing boundaries?

**Projects with substantial rules and independently changing presentation and data access are especially good candidates for UPD.**

Related: [Benefits](benefits.md), [Practical examples](examples.md), and [Mandatory boundaries](../../developers/en/boundaries.md).
