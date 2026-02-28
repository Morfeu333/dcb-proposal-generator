# Proposal Writing Guide — Claude Instructions

This guide tells Claude exactly how to write scope content for D&C Builders proposals.
Follow these rules every time you generate a proposal.

---

## Tone & Style

- **Professional and specific** — describe exactly what will be done, not vague promises
- **Client-facing** — written for the homeowner, not a contractor
- **Active voice** — "Company will install..." not "Installation will be performed..."
- **No filler** — every bullet point must describe real, billable work
- **No placeholders** — never write "[to be determined]" or "as needed" as standalone items

---

## Page & Section Rules

- Cover scope bullets: **max 6 items, max ~30 characters each** (must fit single line)
- Bullet lists: use `ul.bl` class — standard disc bullets, not dashes
- Dense pages (2+ pages of same section): use `.dense` class to compress spacing
- Payment page: **max 22 milestones** — if more, consolidate similar phases
- **Last 2 pages are always fixed** — never write content for General Notes or Thank You

---

## Section Content by Scope Type

### Plans & Engineering (always Section 01)
Include:
- Client design consultation meetings
- Architectural drawings (floor plans, elevations, sections, construction documents)
- Permit acquisition
- Structural engineering calculations
- Title 24 energy compliance
- 3D renderings / mood boards if design toggles are on

### 2nd Story Addition
Split into **2 pages** (Part 1 + Part 2):
- Part 1: Site prep & demo, foundation (slab on grade), wood framing, exterior sheathing, windows & doors
- Part 2: Rough MEP, insulation & drywall, exterior lath & stucco, interior doors & trim, flooring, staircase, final cleanup

### Kitchen Remodel
Single page:
- 3D kitchen design (up to 3 revisions)
- Demo & preparation
- Custom cabinet installation (specify style — shaker, flat panel, etc.)
- Countertop fabrication (specify material — quartz, granite, etc.)
- Backsplash
- Plumbing & electrical finishing
- Paint

### Master Bathroom Remodel
Single page:
- 3D bathroom design
- Full demo
- Shower enclosure (tile, waterproofing, glass door)
- Soaking tub (if applicable)
- Porcelain tile — floors & accent walls
- Vanity, mirrors & fixtures
- Paint & finish

### ADU / Garage Conversion
Single page:
- Plans & permits (California ADU law)
- Demo & structural modifications
- Insulation, drywall & ceilings
- Kitchenette
- ADU bathroom
- Flooring
- Windows, doors & exterior
- HVAC & utilities (mini-split)

### Roofing — Full Replacement
Single page:
- Scope & material (specify tile type)
- Tear-off & deck inspection
- Underlayment & waterproofing
- Tile installation
- Flashings & penetrations
- Cool roof compliance (Title 24)
- Clean-up

### Interior Remodel (general)
Single page or two depending on scope:
- Flooring (specify material)
- Interior paint
- Doors & hardware
- Trim & baseboards
- Any additional rooms specified

---

## Payment Schedule Generation Rules

Build milestones that match the construction phases in the scope. General rules:

1. **Always start with**: `Down payment` → `$1,000`
2. **Always end with**: `Upon Completion & Final Punch List` → last ~4% of total
3. **Milestone naming**: Use "Upon Start [Phase]" or "Pass [Inspection] Inspection"
4. **No milestone over 12% of total** — spread large phases into start + pass inspection
5. **Typical phase order**:
   - Down payment
   - Mobilization & Start Architectural Design
   - Upon Plans Approval & Permit Submission
   - Site Prep & Start Demo
   - Upon Start Foundation Work
   - Upon Foundation Inspection Approval
   - Upon Start Framing
   - Pass Framing Inspection
   - Upon Start Rough MEP
   - Pass Rough MEP Inspection
   - Upon Start Drywall & Insulation
   - Upon Start Exterior Work (Lath/Stucco/Roofing as applicable)
   - [Specialty phases — Kitchen, Bath, ADU, etc.]
   - Upon Pass Final Inspection
   - Upon Completion & Final Punch List

6. **Short descriptions** — max ~45 characters per milestone (payment page has limited width)

---

## Allowances

Always include an Allowances section on the payment page. Tailor to the scope:

| Scope item | Standard allowance |
|---|---|
| LVP/SPC flooring | $3/sqft (material) |
| Engineered hardwood | $6/sqft (material) |
| Windows | $300–$350 per window |
| Kitchen/bath tile install | $8/sqft (labor only) |
| Quartz countertop | $65/sqft (prefab, from company options) |
| Tankless water heater | $1,700 (equipment) |
| ADU mini-split HVAC | $2,500 (equipment) |

---

## Fixed General Notes (verbatim — never modify)

These 29 notes are hardcoded in the Python script. Do NOT rewrite them.
They are automatically included on the second-to-last page of every proposal.

1. Contractor will pull permit under his license and Customer will reimburse permit fees.
2. Blueprints provided by Contractor will include a full set of architectural drawings, structural calculations, Title 24 calculations. Blueprints do not include any slope analysis, topographical or soil reports if required.
3. Any coastal commission requirements will be quoted separately and accordingly.
4. Any structural observation fees or deputy inspector fees related to the project will be paid by the Contractor and reimbursed by the Customer.
5. Contractor will install his sign in front of the house for the duration of the project.
6. Contractor will provide a portable toilet for the duration of the project.
7. Company will provide prefabricated quartz slabs, customer to choose from company's options.
8. Granite or any other natural stone may have cracks, veins, seams, fissures, etc. and Contractor is not responsible for the imperfections of a natural slab.
9. Glass or stone tile will require additional work at extra cost.
10. Tile in shower pan should be of smaller pieces of tile or even mosaic to allow proper slope and should be a non-slip surface.
11. Customer will provide all tiles, grout, appliances, plumbing fixtures, exhaust fans, and any light fixtures other than recessed lights (check allowance section).
12. Any low voltage work such as phones, cable, alarm, computer, sound, cameras etc. as well as the consequences of such work is not included and are to be done by Customer.
13. Any changes to electrical outlets or switches, such as difference in color, style, or dimmers, are to be provided by Customer unless stated differently in the estimate.
14. Job does not include any fire sprinkler system if required by the city.
15. Contractor cannot take responsibility for any existing item(s) set aside or delivered to the job site, including but not limited to appliances & finished materials.
16. Job does not include any fire sprinkler system if required by the city.
17. Job does not include any landscaping work such as: tree removal, flowers or irrigation sprinklers, revival of grass area etc. as well as any hardscape, walkways, driveway etc.
18. Contractor will do their best to keep job site clean and protected, will cover the floors and/or place plastic from floors to ceiling to avoid dirt and dust from spreading. Contractor will pick up & remove large debris at the end of the job, but final cleaning is to be done by Customer as Contractor is not a cleaning company.
19. Job site area is an active construction zone. To avoid any damage to customer property, contractor strongly recommends any items of value be relocated prior to the project start date.
20. Customer agrees not to talk directly to workers and only to the assigned project coordinator in the office in order for us to effectively manage the job and to give the best possible customer service.
21. Customer agrees to give Contractor access to the job site for the entire project duration, Monday through Saturday, between the hours of 8am-5pm for all work, delivery of material, and inspections.
22. Customer understands that certain workdays may be shortened, or no work conducted due to scheduled inspection, bad weather, crew scheduling efficiencies, waiting on ordered materials, etc.
23. If any lead, asbestos, and mold are found, they will be quoted separately by a licensed remediation or abatement company.
24. Any attached computer-generated drawings are simply an aesthetic representation of the project. They do not reflect the actual tile or finishes the customer ultimately chooses.
25. Larger scale interior remodel or addition projects are disruptive by nature due to the work involved. Contractor strongly advises that the Customer relocate during the construction phase of the project.
26. Customer understands that the above specifications are the actual final agreement between Customer and for work to be done. No other verbal promises by representative / salesperson are included in this contract.
27. Any unforeseen relocation of A/C ducts, gas lines, plumbing or electrical issues that need to be addressed after opening walls, as well as lack of insulation will be quoted separately and accordingly.
28. Interior paint will not include doors, shelving, casings, windows, shutters, or any other cabinets unless specially mentioned in the above specification.
29. If the city requires us to build a brand new gas system it will be an additional charge.
