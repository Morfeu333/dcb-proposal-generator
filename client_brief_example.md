# New Client Proposal Brief

Use this file as a reference when asking Claude to generate a new proposal PDF.
Copy it, fill in your client's details, and paste it into the chat.

---

## How to Ask

> "Generate a proposal PDF for this client:"
> *(then paste the filled-in brief below)*

---

## Client Brief — Example

```
Client Name:    David & Maria Restrepo
Address:        2847 Hillcrest Drive, Newport Beach, CA 92660
Proposal Date:  March 2026
Project Total:  $312,500
Output File:    DCB_Proposal_Restrepo.pdf
```

### Project Scope (cover page bullets)

```
- Plans & Engineering
- 500 SF 2nd Story Addition
- Custom Kitchen Remodel
- Hardwood Floor Restoration
```

### Payment Schedule

```
1.  Down payment                                                    $1,000
2.  Mobilization & Start Architectural Design                       $12,000
3.  Upon plans approval                                              $8,000
4.  Site Prep & Start Demo                                          $22,000
5.  Upon Start Foundation & Structural Work                         $28,000
6.  Upon Foundation Inspection                                      $18,000
7.  Pass Framing Inspection                                         $35,000
8.  Upon Start Rough MEP                                            $38,000
9.  Pass Rough MEP Inspection                                       $22,000
10. Upon Start Drywall Work                                         $18,000
11. Upon Start Exterior Lath & Stucco                               $16,000
12. Upon Start Custom Kitchen Cabinet Installation                  $30,000
13. Upon Start Countertop Fabrication                               $14,500
14. Upon Finish Stucco & Exterior Paint                             $18,000
15. Upon Start Hardwood Floor Restoration                           $12,000
16. Upon Pass Final Inspection                                      $15,000
17. Upon Final Completion & Punch List                               $5,000
```

---

## Variables Reference

| Variable        | Where it appears              | Example value                                |
|-----------------|-------------------------------|----------------------------------------------|
| `client_name`   | Cover, Thank You              | `David & Maria Restrepo`                     |
| `client_address`| Cover                         | `2847 Hillcrest Drive, Newport Beach, CA 92660` |
| `proposal_date` | Cover (top right)             | `March 2026`                                 |
| `project_total` | Cover, Payment Schedule page  | `$312,500`                                   |
| `scope_items`   | Cover bullet list             | One bullet per line                          |
| `payments`      | Payment Schedule page         | Description + amount per milestone           |
| `output_path`   | Output PDF filename           | `DCB_Proposal_Restrepo.pdf`                  |

---

## Quick CLI (simple changes only)

```bash
DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 generate_proposal.py \
  --client "David & Maria Restrepo" \
  --address "2847 Hillcrest Drive, Newport Beach, CA 92660" \
  --date "March 2026" \
  --total "\$312,500" \
  --output "DCB_Proposal_Restrepo.pdf"
```

> **Note:** CLI only changes the 5 simple fields above.
> For custom scope bullets or a different payment schedule, use the JSON method below.

---

## JSON Config (full control)

Save as `restrepo.json` and run:

```bash
DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 generate_proposal.py --json restrepo.json
```

```json
{
  "client_name":    "David & Maria Restrepo",
  "client_address": "2847 Hillcrest Drive, Newport Beach, CA 92660",
  "proposal_date":  "March 2026",
  "project_total":  "$312,500",
  "output_path":    "DCB_Proposal_Restrepo.pdf",
  "scope_items": [
    "Plans & Engineering",
    "500 SF 2nd Story Addition",
    "Custom Kitchen Remodel",
    "Hardwood Floor Restoration"
  ],
  "payments": [
    ["Down payment",                                               "$1,000"],
    ["Mobilization & Start Architectural Design",                  "$12,000"],
    ["Upon plans approval",                                        "$8,000"],
    ["Site Prep & Start Demo",                                     "$22,000"],
    ["Upon Start Foundation & Structural Work",                    "$28,000"],
    ["Upon Foundation Inspection",                                 "$18,000"],
    ["Pass Framing Inspection",                                    "$35,000"],
    ["Upon Start Rough MEP",                                       "$38,000"],
    ["Pass Rough MEP Inspection",                                  "$22,000"],
    ["Upon Start Drywall Work",                                    "$18,000"],
    ["Upon Start Exterior Lath & Stucco",                          "$16,000"],
    ["Upon Start Custom Kitchen Cabinet Installation",             "$30,000"],
    ["Upon Start Countertop Fabrication",                          "$14,500"],
    ["Upon Finish Stucco & Exterior Paint",                        "$18,000"],
    ["Upon Start Hardwood Floor Restoration",                      "$12,000"],
    ["Upon Pass Final Inspection",                                 "$15,000"],
    ["Upon Final Completion & Punch List",                         "$5,000"]
  ]
}
```
