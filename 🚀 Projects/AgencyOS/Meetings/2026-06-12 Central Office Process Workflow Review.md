---
type: meeting
date: 2026-06-12
description: Review of Vendor Registration and PO form flows for AgencyOS — aligning structure, field changes, approval layers, and NetSuite sync strategy.
attendees: [Ayya, Rayva, Peter Novianto, Petrus Nugroho Wicaksono, Reza Andika (Batak), Fariz, Rahmat Hidayat]
attendees_source: transcript
source: https://fcn.sg.larksuite.com/minutes/obsg685fqri44i717jei3jxv
tags: [meeting, agencyos, vendor-registration, purchase-order, netsuite]
project: AgencyOS
quarter: Q2 2026
---
# [Online] Central Office Process Workflow Review

**Date:** 2026-06-12 (Fri), 17:32 WIB — 2h 1m
**Attendees:** [[Ayya]] (facilitator), Rayva/pare (system builder), [[Batak]], Peter Novianto (Proc), Petrus Nugroho Wicaksono, Fariz, Rahmat Hidayat
**Context:** First full walkthrough of Vendor Registration and PO forms — aligning field structure, approval flow, and NetSuite integration requirements across all FCN agencies.

---

## Summary

Rayva and Ayya walked the group through two forms: the **Vendor Registration form** and the **PO Request form**. The session focused on validating field structure, resolving terminology gaps, and agreeing on the approval flow before NetSuite sync. Key outcomes: remove two fields from vendor registration, add expiry date for non-PKP letters, add Term of Payment to PO form, and auto-derive vendor cost type from the vendor database instead of manual input. The group also aligned on a backfill plan: pool all existing vendor data from each agency, deduplicate via AI, then inject into NetSuite as a clean baseline.

---

## Key Decisions

- **Person field** → removed from vendor registration (security: exposes internal contacts)
- **Maksimal Nilai PO** → removed from registration (credit limit is a per-agreement discussion, not registration data)
- **Freelance** stays as a vendor type option in the form, but is treated as *vendor perorangan* in the system/NetSuite
- **Bank beneficiary name** must match KTP (for individuals) or NPWP (for companies) — to be enforced by instruction text, not hard system block at registration stage
- **Surat Non-PKP** has an annual expiry (valid within fiscal year Jan–Dec) — vendor must input expiry date so system can auto-remind
- **Term of Payment (TOP)** to be added to PO form as a select field — filled by Account, based on negotiation with vendor
- **Type of Cost** in PO form → do not ask manually; auto-derive from vendor type in vendor database (perorangan = freelance, network entity = interco, others = third party)
- **PO Number replaces MCS Number** in orca's media flow — same function, different label
- **Interco vendors** have IC prefix in NetSuite; this flag needs to be captured in the vendor database
- **Pinjam PT** (borrowing PT from another entity) needs a separate automation flow — ASF % and progressive tax implications must be visible in the PO
- **Blacklist** to be scoped per category/pillar, not necessarily network-wide
- **Backfill plan**: collect all agency vendor data → AI dedup + fuzzy match → resolve conflicts → inject into NetSuite as baseline before go-live

---

## 🎯 My Action Items

- [ ] **Remove** "Person" field from vendor registration form
- [ ] **Remove** "Maksimal Nilai PO" field from vendor registration form
- [ ] **Add description** to Beneficiary Name field: *"Name must match your KTP (individual) or NPWP (company)"*
- [ ] **Add** date field "Tanggal Expire Surat Non-PKP" — visible only for non-PKP vendors; hook automation reminder to this date
- [ ] **Add** "Term of Payment" select field to PO form — options: 30 / 60 / 90 / 120 days
- [ ] **Remove** manual "Type of Cost" from PO form — replace with auto-fill from vendor type in vendor database
- [ ] **Update** vendor/resource field in PO form → dropdown from vendor database (not free text); if vendor not registered, show prompt to register first
- [ ] **Add** description to TOP field clarifying that Account fills this based on vendor quotation/negotiation
- [ ] **Coordinate with Fariz** to get the correct vendor data export from NetSuite (confirm the right dataset, not the joined/subsidiary view)
- [ ] Finalize and clean up vendor registration form → share updated version next meeting
- [ ] Prepare for **trial run** of vendor registration with Petrus (next meeting after Petrus's leave week)

---

## Pinpoint: Form Changes

### Vendor Registration Form

| Field | Action | Notes |
|-------|--------|-------|
| Person | ❌ Remove | Security risk — exposes internal team contacts |
| Maksimal Nilai PO | ❌ Remove | Not a registration field; handle per-agreement |
| Beneficiary Name | ✏️ Add description | "Must match name on KTP / NPWP" |
| Tanggal Expire Surat Non-PKP | ➕ Add (date field) | Shown only when vendor = non-PKP; triggers reminder automation |
| Freelance (vendor type) | ✅ Keep | UI label = Freelance; maps to vendor perorangan in system |
| NIK + NPWP | ✅ Keep both | Both mandatory; for companies NPWP is the key ID |

### PO Form

| Field | Action | Notes |
|-------|--------|-------|
| Term of Payment | ➕ Add (select) | Options: 30 / 60 / 90 / 120 days; filled by Account |
| Type of Cost | ♻️ Auto-fill | Derive from vendor type in vendor DB — remove manual selection |
| Vendor / Resource Name | ♻️ Update | Change to dropdown from vendor database; trigger vendor registration prompt if not found |
| Include/Exclude PPh | ✅ Keep | Per-vendor per-job decision confirmed necessary |

### Approval Flow (Vendor Registration)

```
Vendor submits form
  ↓
Account PIC notified (Lark chat, Approve/Reject button)
  ↓
BD / HOD second layer verification
  ↓
Prokirman (Peter Novianto) final check
  ↓
Status → Approved → auto-sync to NetSuite
  ↓
If correction needed → send form edit link back to vendor
```

---

## Key Signals

- Petrus confirmed that NIK/KTP and NPWP names are always the same for individuals — bank beneficiary name must also match; this is a tax subject identification requirement
- Peter Novianto flagged real-world data quality issues: wrong categories, double spaces, account name mismatches, PKP ↔ non-PKP flips — the new form + flow needs to handle these cleanly via vendor re-edit, not manual Finance correction
- Interco transaction handling (pinjam PT + ASF) is complex and needs a separate flow — agreed this is out of scope for current milestone
- Petrus is on leave next week — coordinate with Fariz, Rahmat, Batak in the interim

---

## Next Steps

- Rayva to ship updated form (see action items above)
- Fariz to confirm correct NetSuite vendor export dataset
- Schedule trial/testing session once updated form is ready (after Petrus returns)
- Separate session needed for: pinjam PT automation, blacklist feature, progressive tax visibility

---

## Related

- [[AgencyOS]]
- [[Ayya]]
- [[Batak]]
