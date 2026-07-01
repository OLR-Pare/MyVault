---
type: project
date: 2026-07-01
description: Automate FCN Networks' Individual Development Plan (IDP) reports from Lark Base appraisal data using AI-generated narrative summaries and DocuGenius rendering.
tags: [project, automation, lark-base, ai]
status: active
quarter:
deadline:
---
# FCN Networks IDP Automation

## Goal
> Generate per-employee IDP reports (9-box placement, gap reading, development focus areas, 90-day action plan, manager coaching guide) automatically from appraisal scores already captured in Lark Base, using AI to write the narrative sections and DocuGenius to render the final document.

## Current State
- Reviewed Base `Manager Review - Senior Account Executive` table (base token `LnySb2dsUaUXhus0zGZll854gMc`, table `tblXvtFuOju2Vss2`) — scores, formulas, and lookups from the linked Self Review table are already in place.
- Reviewed reference IDP template (`FCN_IDP_Intan_Galih_Kesuma_v3.docx`) — identified ~9 distinct narrative sections that need AI summarization (key strengths, placement narrative, gap readings, strength-to-leverage map, development focus areas, 90-day action plan, coaching guide).
- Designed (not yet built): input JSON shape (self/manager/gap per competency, computed averages, 9-box quadrant — all from Base formulas) and an OpenAI structured-output JSON schema whose keys map 1:1 to new `AI - ...` Base fields.
- Rayva is now designing the actual Base fields for these AI outputs.

## Tech Stack
- Lark Base (data + formulas)
- Anycross (orchestration: trigger → HTTP request to OpenAI → write back to Base)
- OpenAI API (structured outputs / json_schema mode for reliability)
- DocuGenius (renders populated Base fields into the final IDP docx)

## Tasks
- [ ] Rayva: design/add `AI - ...` output fields in the Manager Review table matching the JSON schema keys
- [ ] Guide: configure Anycross flow (trigger, HTTP request w/ structured output, field mapping, DocuGenius render step)
- [ ] Add an HR approval gate before DocuGenius render/send (report affects salary & promotion decisions)

## Key Decisions
- All deterministic values (scores, gaps, priority H/M/L, 9-box quadrant, salary/promotion eligibility) stay as Base formulas — AI only writes narrative text, never computes numbers.
- One OpenAI call per employee covering all narrative sections (not one call per field) — cheaper and keeps sections mutually consistent.
- Use OpenAI structured outputs (`response_format: json_schema`, strict mode) rather than prompting for JSON in free text, so Anycross can map response keys directly to Base fields without a validation layer.

## Log

| Date | Update |
|------|--------|
| 2026-07-01 | Read Base structure + reference docx template, designed input/output JSON schema and Anycross flow outline. Rayva to design Base fields next, will return for Anycross setup guide. |

## Related
- [[FCN Networks]]
- [[Memory]]
