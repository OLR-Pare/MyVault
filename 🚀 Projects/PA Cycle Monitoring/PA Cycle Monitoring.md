---
type: project
date: 2026-06-12
description: Automated consolidation of PA Cycle data from 138 Lark bases into a master base with Anycross, plus monitoring dashboard.
tags: [project, lark, automation, anycross, pa-cycle]
status: active
quarter: Q2 2026
deadline:
---
# PA Cycle Monitoring

## Goal
> Consolidate Self Review, Manager Review, and Final Verdict (PA Cycle) data from 138 Lark bases into a single master Lark Base, synced hourly via Anycross, with a monitoring dashboard to track submission and review progress.

## Current State
- ✅ Master Base created: [PA Master - Self Review Consolidated](https://fcn.sg.larksuite.com/base/BigabYUZCaNLTHsKKNilSUUagWh)
- ✅ Source Registry table populated (138 bases, all with Self Review + Manager Review table IDs, Category, Base Link)
- ✅ Self Review Master table — Anycross flow live (truncate & reload hourly)
- ✅ Manager Review Master table — Anycross flow built, field mapping resolved
- ✅ PA Cycle (Creative only) Master table — Anycross flow in progress
- 🔄 Dashboard monitoring — wireframe designed, pending implementation

## Tech Stack
- **Lark Base** — master data store
- **Anycross** — hourly sync automation (truncate & reload)
- **lark-cli** — CLI for bulk operations (registry population, permission grants)

## Master Base
- URL: https://fcn.sg.larksuite.com/base/BigabYUZCaNLTHsKKNilSUUagWh
- Base Token: `BigabYUZCaNLTHsKKNilSUUagWh`

### Tables
| Table | Table ID | Description |
|-------|----------|-------------|
| Source Registry | `tblldadUWDnBQlJt` | 138 base references with tokens, table IDs, category, link |
| Self Review Master | `tbldqTZB8ZhFbYtt` | Merged self review from all 138 bases |
| Manager Review Master | *(see base)* | Merged manager review — Non Creative (Manager Review) + Creative (Final Verdict - PA Cycle) |

### Source Registry Columns
`Base Name` · `Base Token` · `Self Review Table ID` · `Self Review Table Name` · `Manager Review Table ID` · `Manager Review Table Name` · `Category` (Creative / Non Creative) · `Base Link`

## Anycross Flows

### Self Review Flow
- **Method:** Truncate & reload (delete all → insert all)
- **Schedule:** Every 1 hour
- **Logic:** Loop 138 bases → loop records → skip if Employee's Full Name empty → Create Record
- **Key fields:** SelfID, Employee's Full Name, Company ID, Email, Job Position, Department, Business Unit, Manager Name/Email, Appraisal Cycle, Evaluation Period, Unique Code

### Manager Review Flow
- **Method:** Truncate & reload
- **Schedule:** Every 1 hour
- **Source:** Non Creative → `Manager Review - {Position}` | Creative → `Final Verdict - PA Cycle`
- **JS normalize node (script-3):** Handles field name differences between Creative/Non Creative, extracts scores as numbers
- **Key fields:** Unique Code, scores (Competency/Habit/Future Proof/Final), Final Verdict, Salary Increment, Promotion fields, Other Title

### PA Cycle Flow (Creative only)
- **Method:** Truncate & reload
- **Schedule:** Every 1 hour
- **Source:** Only 14 Creative bases — filter Source Registry by `Category = Creative`
- **Branch in loop-1:** Skip if `Final Verdict - PA Cycle Table ID` is empty

## Field Path Reference

### Self Review source field types
| Field | Structure | Path |
|-------|-----------|------|
| Formula fields (SelfID, Job Position, Department, Unique Code) | `{type:1, value:[{text:"..."}]}` | `.value[0].text` |
| Text fields (Full Name, Email, Manager Name/Email) | `[{text:"..."}]` | `[0].text` |
| Select/string fields (Business Unit, Appraisal Cycle, Evaluation Period) | plain string | direct |
| Number fields (Company ID) | plain number | direct |

### Manager Review source field types
| Field | Structure | Path |
|-------|-----------|------|
| Formula fields (scores, verdict, eligibility) | `{type:1, value:[{text:"..."}]}` or plain number | `.value[0].text` or direct |
| Select fields (Proceed, Reason, Title) | plain string | direct |
| Business Unit | `{type:3, value:["..."]}` | `.value[0]` |

## Dashboard Plan

### Widgets
1. **Summary cards** — Total Self Review, Total Manager Review, Total PA Cycle, Completion Rate %
2. **Bar chart** — Self Review vs Manager Review by Business Unit
3. **Pie chart** — Final Verdict distribution (Exceed / Meet / Below)
4. **Pie chart** — Promotion Eligibility distribution
5. **Bar chart** — Salary Increment Eligibility
6. **Bar chart** — Proceed for Promotion
7. **Bar chart** — Manager progress per Direct Manager

### Pending
- [ ] Add `Manager Review Status` formula field in Self Review Master (Completed / Pending) to enable completion rate tracking
- [ ] Build dashboard in Lark Base using above widgets

## Key Decisions
- **Truncate & reload** over upsert — simpler, no update logic needed, max ~400 records per cycle
- **Anycross** for automation — serial loops work, but command substitution hangs in background shell; solved with file redirect + Python for batch ops
- **Source Registry** as single source of truth for base tokens + table IDs — avoids hardcoding in Anycross
- **Unified Manager Review flow** for Creative + Non Creative — JS normalize node handles field name differences with fallback logic
- **Category field** (single select) added to Source Registry to filter Creative/Non Creative in flows

## Log

| Date | Update |
|------|--------|
| 2026-06-15 | Source Registry: added Category (Creative/Non Creative) + Base Link columns, all 138 populated |
| 2026-06-15 | Manager Review Anycross flow: resolved TextFieldConvFail, JS normalize adjusted for plain number + text array handling |
| 2026-06-12 | Manager Review table IDs populated in Source Registry (138/138), all matched correctly |
| 2026-06-12 | JavaScript `has_data` check fixed: `$.loop-2.item` is object (not array), `Employee's Full Name` is formula wrapper in Manager Review |
| 2026-06-12 | Self Review flow: branch node fixed (boolean vs string mismatch — JS now returns string "true"/"false") |
| 2026-06-12 | App permissions granted to all 138 bases (App ID: cli_a670ef189ce2902f) |
| 2026-06-12 | Master Base created, Source Registry + Self Review Master tables set up |

## Related
- [[ALVA]]
- Source Registry: https://fcn.sg.larksuite.com/base/BigabYUZCaNLTHsKKNilSUUagWh?table=tblldadUWDnBQlJt
