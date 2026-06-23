---
type: meeting
date: 2026-06-22
description: Working session to revise PO, SO, and payment flows in AgencyOS — job number logic, budget visibility, vendor validation, and approver configuration.
attendees: [Ayya, Jeff, Rayva]
attendees_source: transcript
source: https://fcn.sg.larksuite.com/minutes/obsgd297dr3xm6bcl663h3a5
tags: [meeting, agencyos, po-flow, so-flow, payment, vendor-registration]
project: AgencyOS
quarter: Q2 2026
---
# Runthrough Flow Revision

**Date:** 2026-06-22 (Sun), 16:20 WIB — 1h 38m
**Attendees:** [[Ayya]], [[Jeff]], Rayva *(speakers unnamed in transcript — attributed by context)*
**Context:** Working session to run through and revise the PO, SO, and payment flows before the next stakeholder meeting — fixing logic gaps, agreeing on source of truth for job numbers, and aligning on what's in scope for this month.

---

## Summary

The session focused on three areas: **(1)** tightening the PO form logic for project vs non-project requests (including pitching), **(2)** resolving the SO revision flow and ensuring sales values are locked to SO figures, and **(3)** scoping the payment request module. Several open questions were surfaced around NetSuite behavior (PO showing as minus, SO revision handling) that need to be resolved with Finance. Priorities for this month: finish Vendor Registration + Sales Tracker first, then move to Payment flow.

---

## Key Decisions

- **Job number in PO (non-project):** optional — user can type it manually, but not required; if empty = fine, just needs a description
- **Pitching cost:** treated as **non-project** in PO — add disclaimer copy: *"If this is for pitching purposes, select Non-Project"*
- **Single source of truth for job numbers:** all data pulled from **Project** table (not Pitches table)
- **SO revision:** edit the existing SO (not create a new one); Finance handles in NetSuite manually
- **Sales value lock:** need a column in project tracker to verify that Sales = SO value — prevents account from editing sales without a proper SO
- **Type of Cost in PO:** "Under Cost" confirmed removed; remaining options: **Third Party, Freelance, Interco** only
- **Maleo approver selection:** add disclaimer — *"Select Account Lead according to the brand being worked on"*
- **Vendor beneficiary name:** add formula in base to validate if beneficiary name matches KTP/NPWP — helps Peter's screening, allows prioritising clean submissions
- **Budget remaining:** feature needed — currently no cap/remaining view; users can spend without knowing limits; to be designed
- **Payment request module:** deferred until Vendor Registration + Sales Tracker are stable; payment will reference PO number and can be submitted in partial amounts
- **Non-registered vendor payments** (restaurant, rental, etc.): use PO as non-project with description — no vendor registration required
- **Scope for this month:** Vendor Registration → Sales Tracker → then Payment

---

## 🎯 My Action Items

- [ ] **PO form — non-project job number:** change to optional text input (not required from base dropdown); add placeholder hint *"If any"*
- [ ] **PO form — non-project disclaimer:** add helper text explaining that description is mandatory to explain the purpose
- [ ] **PO form — pitching disclaimer:** add copy *"For pitching purposes, select Non-Project and describe accordingly"*
- [ ] **PO form — Maleo approver:** add disclaimer *"Select Account Lead based on the brand being worked on"*
- [ ] **Vendor registration — beneficiary name validation:** build formula in base to flag mismatch vs KTP/NPWP name; use as a pre-screening signal for Peter Novianto (not a hard block)
- [ ] **PO form — Type of Cost:** confirm only Third Party / Freelance / Interco remain (under cost removed ✓)
- [ ] **Project tracker — Sales lock column:** add column to verify Sales value = SO value; lock sales input so it must come from SO
- [ ] **Coordinate with Finance:** clarify how SO/PO revisions work in NetSuite — edit existing or create new? Affects sync logic
- [ ] **Investigate PO minus issue:** PO values showing as negative in NetSuite — surface to Finance for clarification
- [ ] **Source of truth alignment:** ensure all job number lookups point to Project table, not Pitches

---

## Open Questions

| Question | Owner | Status |
|---|---|---|
| How does Finance revise SO/PO in NetSuite — edit existing or create new? | Finance | ❓ Unresolved |
| When pitching wins, how does pitching cost flow into project cost? | Rayva + Finance | ❓ Unresolved |
| Why are PO totals showing as minus in NetSuite? | Finance / Fariz | ❓ Unresolved |
| Budget remaining/cap feature — what's the design? | Rayva + Ayya | ❓ To be designed |
| Media Plan Number in Orca — how does it map to job number / PO? | Rahmat Hidayat | ❓ Unresolved |

---

## Key Signals

- Budget visibility is a recurring concern — people are spending without knowing remaining budget, risk of blowing freelance or project budgets without realising
- SO integrity is critical: if account can edit sales values freely without a corresponding SO, reconciliation breaks downstream
- Finance doesn't need the internal breakdown (per department, per sub-category) — they only need Third Party / Freelance / Interco at submission level; internal breakdown stays in each agency's own base view
- Orca still uses MCS codes, not PO — alignment needed before Orca can adopt the new flow

---

## Next Steps

- Ship PO form revisions (see action items)
- Coordinate mini meeting (Ayya + Jeff + Rayva) before next full stakeholder session
- Finance discussion to resolve SO revision + PO minus issues
- Finalize Vendor Registration + Sales Tracker as prerequisite before opening Payment flow

---

## Related

- [[AgencyOS]]
- [[Ayya]]
- [[Jeff]]
- [[2026-06-12 Central Office Process Workflow Review]]
