# System Architecture — DCB Proposal Generator

## Overview

A lightweight proposal generation system for D&C Builders that turns client intake
data into polished, branded PDF proposals. Claude acts as the intelligent content
layer; Python handles deterministic PDF rendering.

---

## Component Map

```
┌─────────────────────────────────────────────────────────┐
│                    INTAKE LAYER                          │
│                                                          │
│  artifact_form.html                                      │
│  ─ HTML/JS form opened inside Claude.ai                  │
│  ─ Client info, design toggles, scope of work            │
│  ─ On submit → inserts row to Supabase                   │
└──────────────────────┬──────────────────────────────────┘
                       │ Supabase JS client (anon key)
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   DATA LAYER                             │
│                                                          │
│  Supabase — client_intakes table                         │
│  ─ Stores all intake submissions                         │
│  ─ Fields: name, address, scope_items, payments, etc.   │
│  ─ status: pending → generated → sent                    │
└──────────────────────┬──────────────────────────────────┘
                       │ Claude reads via Supabase MCP
                       ▼
┌─────────────────────────────────────────────────────────┐
│                 INTELLIGENCE LAYER                       │
│                                                          │
│  Claude Code (via /generate-proposal skill)              │
│  ─ Reads intake from Supabase                            │
│  ─ Decides: standard vs full-scope template              │
│  ─ Writes all scope section content                      │
│  ─ Generates payment schedule milestones                 │
│  ─ Builds the client JSON file                           │
└──────────────────────┬──────────────────────────────────┘
                       │ runs Python script
                       ▼
┌─────────────────────────────────────────────────────────┐
│                 RENDERING LAYER                          │
│                                                          │
│  generate_proposal.py / generate_proposal_full_scope.py  │
│  ─ Pure Python + WeasyPrint                              │
│  ─ No LLM, no API calls at runtime                       │
│  ─ HTML template → PDF                                   │
│  ─ Outputs: DCB_Proposal_ClientName.pdf                  │
└─────────────────────────────────────────────────────────┘
```

---

## Data Flow (step by step)

1. **Sales rep** opens `artifact_form.html` inside Claude.ai
2. Fills in client name, address, scope items, project total, notes
3. Clicks **Submit** → row inserted to `client_intakes` in Supabase
4. Sales rep tells Claude Code: **"Generate proposal for [client name]"**
5. Claude runs `/generate-proposal` skill
6. Claude queries Supabase, reads the intake row
7. Claude writes scope content adapted to the project type
8. Claude generates payment schedule based on scope + total
9. Claude saves JSON to `clients/clientName.json`
10. Claude runs the Python script
11. **PDF saved** to the project folder, ready for delivery

---

## What Claude does vs what Python does

| Responsibility | Claude | Python script |
|---|---|---|
| Read client intake data | ✅ | — |
| Choose which template to use | ✅ | — |
| Write scope section content | ✅ | — |
| Generate payment milestones | ✅ | — |
| Build JSON config file | ✅ | — |
| Render HTML → PDF | — | ✅ |
| Apply brand colors / fonts | — | ✅ |
| Enforce page structure | — | ✅ |
| Fixed General Notes text | — | ✅ (hardcoded) |

---

## Deployment

| Component | Where it runs |
|---|---|
| Intake form | Claude.ai (artifact) — internal use |
| Supabase | Supabase Cloud (free tier sufficient) |
| Claude Code | Local machine (any computer with the repo cloned) |
| Python script | Local machine (macOS/Linux/Windows) |
| PDF output | Local machine — save/email/upload manually |

No servers to host. No deployments to manage.

---

## Future extensions (optional)

- **Auto-email**: After PDF is generated, send it via SendGrid/Resend
- **Supabase Storage**: Upload the PDF to Supabase Storage for team access
- **Status webhook**: Update `status` field in Supabase when proposal is sent
- **Client portal**: Share a public Supabase Storage URL with the client
