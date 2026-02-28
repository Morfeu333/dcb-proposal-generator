# Skill: /generate-proposal

Generates a D&C Builders PDF proposal from a client intake stored in Supabase.

---

## Usage

```
/generate-proposal
/generate-proposal [client name or partial name]
/generate-proposal --latest
```

---

## Steps Claude must follow

### 1. Find the intake

If a client name was given, query Supabase for a matching row:
```sql
SELECT * FROM latest_intakes
WHERE client_name ILIKE '%[name]%'
ORDER BY created_at DESC
LIMIT 1;
```

If `--latest` or no argument, use:
```sql
SELECT * FROM latest_intakes
WHERE status = 'pending'
ORDER BY created_at DESC
LIMIT 1;
```

### 2. Map fields to ProposalConfig

| Supabase field | JSON field |
|---|---|
| `client_name` | `client_name` |
| `full_address` | `client_address` |
| `proposal_date` | `proposal_date` (use current month/year if blank) |
| `project_total` | `project_total` |
| `scope_items` | `scope_items` |
| `payments` | `payments` (generate if empty array) |

### 3. Choose the right template

- **`generate_proposal.py`** — 3 or fewer scope items, or simple remodel
- **`generate_proposal_full_scope.py`** — 4+ scope items, or includes 2nd story addition, ADU, or roofing

### 4. Generate the payment schedule (if payments is empty)

Read `PROPOSAL_WRITING_GUIDE.md` → "Payment Schedule Generation Rules" section.
Build a payment schedule that:
- Matches the construction phases in scope_items
- Starts with Down payment $1,000
- Ends with Upon Completion & Final Punch List (~4% of total)
- Has no single milestone over 12% of project total
- Uses short milestone descriptions (max ~45 chars)

### 5. Write the scope section content

Read `PROPOSAL_WRITING_GUIDE.md` → "Section Content by Scope Type".
Write detailed, professional bullet points for each scope section.
Adapt content specifically to this client's project — do not use generic copy.

### 6. Save the JSON file

Save to: `clients/[LastName]_[FirstName].json`

Example:
```json
{
  "client_name":    "Robert & Angela Martinez",
  "client_address": "4821 Seabreeze Lane, Huntington Beach, CA 92648",
  "proposal_date":  "March 2026",
  "project_total":  "$541,000",
  "scope_items": ["Plans & Engineering", "Full 2nd Story Addition (1,200 SF)"],
  "payments": [["Down payment", "$1,000"], ...]
}
```

### 7. Run the generator

**macOS:**
```bash
DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 generate_proposal_full_scope.py --json clients/Martinez_Robert.json
```

**Linux / Windows:**
```bash
python3 generate_proposal_full_scope.py --json clients/Martinez_Robert.json
```

### 8. Update Supabase status

After successful generation, update the intake row:
```sql
UPDATE client_intakes
SET status = 'generated', pdf_path = '[output path]'
WHERE id = '[intake id]';
```

### 9. Confirm to user

Tell the user:
- The PDF path
- How many pages were generated
- The payment schedule total (confirm it matches project_total)

---

## Error handling

- If no intake found → ask user to confirm the client name or check Supabase
- If WeasyPrint not installed → remind user to run `pip3 install weasyprint` and `brew install pango`
- If project_total is missing → ask user to provide it before generating
