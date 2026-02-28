# DCB Proposal Generator — Claude Instructions

## What this project is

Python-based PDF proposal generator for **D&C Builders** (Design and Create Builders),
a licensed general contractor in Southern California (License #1116111).

The tool generates professional project proposals in PDF format from client intake data.
Claude is the **content intelligence layer** — it writes scope descriptions, generates
payment schedules, and adapts content to each project type.
The Python scripts are the **rendering layer** — pure HTML-to-PDF, no LLM at runtime.

---

## Architecture

```
[Intake Form (artifact_form.html)]
        ↓  submits to
   [Supabase — client_intakes table]
        ↓  Claude reads via MCP or query
   [Claude — writes scope content + payment schedule]
        ↓  creates JSON, runs script
   [generate_proposal.py OR generate_proposal_full_scope.py]
        ↓
   [PDF output — saved locally]
```

---

## Which script to use

| Project type | Script |
|---|---|
| 1–3 scope items (simple remodel, kitchen only, etc.) | `generate_proposal.py` |
| 4+ scope items OR includes 2nd story addition / ADU | `generate_proposal_full_scope.py` |

---

## How to run

```bash
# macOS — always use this prefix
DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 generate_proposal.py --json clients/myClient.json

# Linux / Windows — no prefix needed
python3 generate_proposal.py --json clients/myClient.json

# Full scope version
DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 generate_proposal_full_scope.py --json clients/myClient.json
```

---

## One-time setup (new machine)

```bash
# macOS
brew install pango
pip3 install weasyprint

# Linux
sudo apt install libpango-1.0-0 libpangoft2-1.0-0
pip3 install weasyprint
```

---

## JSON format (client data)

```json
{
  "client_name":    "First & Last Name",
  "client_address": "123 Street, City, CA 90000",
  "proposal_date":  "March 2026",
  "project_total":  "$298,000",
  "scope_items": [
    "Plans & Engineering",
    "Kitchen Remodel"
  ],
  "payments": [
    ["Down payment", "$1,000"],
    ["Mobilization & Start Architectural Design", "$10,000"],
    ["Upon Completion & Final Punch List", "$5,000"]
  ]
}
```

Save files to `clients/clientName.json`. Output PDF is auto-named from `client_name`.

---

## Template structure rules

- **Page 1**: Cover (dynamic — client name, address, date, total, scope bullets)
- **Page 2**: Table of Contents (dynamic — update section titles to match project)
- **Pages 3 → N-2**: Scope sections (variable — depends on project size)
- **Page N-1**: General Notes (**FIXED** — 29 standard clauses, never edit)
- **Page N**: Thank You (**FIXED** — D&C Builders branding, never edit)

---

## Design system

| Token | Value |
|---|---|
| Navy | `#0f1d2c` |
| Gray | `#e9e9e9` |
| White | `#ffffff` |
| Font | Raleway (Google Fonts) |
| Page size | 8.5 × 11 in (US Letter) |
| All content pages | Gray background |
| Cover + Thank You | Special (gray cover, navy thank you) |

---

## Supabase integration

- **Table**: `client_intakes`
- **Project URL**: `YOUR_SUPABASE_URL`
- **Anon key**: `YOUR_SUPABASE_ANON_KEY`
- See `supabase_schema.sql` for full table structure
- See `.claude/skills/generate-proposal.md` for the `/generate-proposal` skill

---

## Key files

| File | Purpose |
|---|---|
| `generate_proposal.py` | Standard renderer (up to 9 pages) |
| `generate_proposal_full_scope.py` | Full renderer (up to 12 pages) |
| `PROPOSAL_WRITING_GUIDE.md` | How to write scope content |
| `artifact_form.html` | Intake form — open in Claude.ai |
| `supabase_schema.sql` | Database schema |
| `.claude/skills/generate-proposal.md` | `/generate-proposal` slash command |
| `clients/` | Client JSON files |

---

## Slash command

Run `/generate-proposal` to generate a proposal from the latest Supabase intake.
See `.claude/skills/generate-proposal.md` for full instructions.
