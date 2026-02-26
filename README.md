# D&C Builders — Proposal PDF Generator

Generates professional project proposal PDFs from a JSON config file.
No design software needed — just Python.

---

## Folder Structure

```
DCB-Proposal-Generator/
├── generate_proposal.py       ← Main script (don't edit unless needed)
├── client_brief_example.md    ← Reference: how to fill in a new client
├── README.md                  ← This file
└── clients/
    └── example_restrepo.json  ← Example client config (copy & edit this)
```

---

## One-Time Setup

### macOS

```bash
# 1. Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install system dependency
brew install pango

# 3. Install Python library
pip3 install weasyprint
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3-pip libpango-1.0-0 libpangoft2-1.0-0
pip3 install weasyprint
```

### Windows

Windows requires the GTK3 runtime first:

1. Download and install GTK3 from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
2. Restart your terminal after installing
3. Then run:
```bash
pip install weasyprint
```

---

## Generating a PDF

### Option A — Edit the example JSON and run

1. Duplicate `clients/example_restrepo.json`
2. Rename it to your client's name (e.g., `clients/johnson.json`)
3. Edit all the fields inside
4. Run:

**macOS:**
```bash
DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 generate_proposal.py --json clients/johnson.json
```

**Linux / Windows:**
```bash
python3 generate_proposal.py --json clients/johnson.json
```

The PDF will be saved in the same folder as the script, named after the client automatically.

---

### Option B — Quick CLI (simple changes only)

Use this when you only need to change name, address, date, and total — no custom payment schedule.

**macOS:**
```bash
DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 generate_proposal.py \
  --client "Jane Doe" \
  --address "123 Main St, Irvine, CA 92602" \
  --date "April 2026" \
  --total "\$175,000" \
  --output "DCB_Proposal_JaneDoe.pdf"
```

**Linux / Windows:**
```bash
python3 generate_proposal.py \
  --client "Jane Doe" \
  --address "123 Main St, Irvine, CA 92602" \
  --date "April 2026" \
  --total "$175,000" \
  --output "DCB_Proposal_JaneDoe.pdf"
```

---

## JSON Config Reference

| Field | Type | Description |
|---|---|---|
| `client_name` | string | Full client name — appears on cover |
| `client_address` | string | Full address — appears on cover |
| `proposal_date` | string | e.g. `"March 2026"` — top right of cover |
| `project_total` | string | e.g. `"$298,800"` — cover + payment page |
| `scope_items` | list of strings | Bullet points on cover page |
| `payments` | list of [description, amount] | Payment schedule milestones |
| `output_path` | string (optional) | Custom output path. If omitted, auto-named from client |

### Minimal JSON example

```json
{
  "client_name":    "Jane Doe",
  "client_address": "123 Main St, Irvine, CA 92602",
  "proposal_date":  "April 2026",
  "project_total":  "$175,000",
  "scope_items": [
    "Plans & Engineering",
    "Kitchen Remodel"
  ],
  "payments": [
    ["Down payment", "$1,000"],
    ["Upon completion", "$174,000"]
  ]
}
```

---

## Tips

- You can have **as many client JSON files as you want** inside the `clients/` folder
- Payment items can be **any number** — the list is fully dynamic
- Scope bullets on the cover can be **any number** of items
- The PDF is always **9 pages**, US Letter size (8.5 × 11 in)
- If you ask Claude Code to generate a proposal, just share this README and the client info — Claude will handle the rest

---

## Asking Claude Code to Generate a PDF

If you're using Claude Code (Claude's CLI), just say:

> "Generate a proposal PDF for this client:"

Then paste the filled-in client brief from `client_brief_example.md`.
Claude will create the JSON and run the script for you.
