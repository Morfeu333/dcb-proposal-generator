#!/usr/bin/env python3
"""D&C Builders — Project Proposal PDF Generator

Parameterized template. Customize via ProposalConfig, a JSON file, or CLI flags.

Run:
    DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 generate_proposal.py
    DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 generate_proposal.py --client "Jane Doe" --total "$150,000"
    DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 generate_proposal.py --json my_client.json
"""
import argparse
import html as html_lib
import json
import os
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from weasyprint import HTML

# ── Brand colors ────────────────────────────────────────────────────────────
NAVY  = "#0f1d2c"
GRAY  = "#e9e9e9"
WHITE = "#ffffff"


# ── Config ──────────────────────────────────────────────────────────────────
@dataclass
class ProposalConfig:
    """All client/project-specific variables for one proposal.

    Edit the defaults here, pass --json <file>, or use CLI flags.
    JSON schema matches field names exactly (snake_case).
    payments: list of [description, amount] pairs.
    """

    # Cover page
    client_name:    str = "Sergio castillo"
    client_address: str = "11263 Stonecress Ave, Fountain Valley, CA, 92708"
    proposal_date:  str = "February 2026"
    project_total:  str = "$298,800"

    # Cover scope bullets (shown on cover page)
    scope_items: List[str] = field(default_factory=lambda: [
        "Plans",
        "350 SF 1st story Addition",
        "Interior Remodel",
    ])

    # Payment schedule — list of (description, amount)
    payments: List[Tuple[str, str]] = field(default_factory=lambda: [
        ("Down payment",                                                          "$1,000"),
        ("Mobilization & Start Architectural Design",                             "$10,500"),
        ("Upon plans approval",                                                   "$6,000"),
        ("Site Prep & Start Demo",                                                "$25,000"),
        ("Upon Start Foundation Work",                                            "$25,000"),
        ("Upon Foundation Inspection",                                            "$15,000"),
        ("Pass framing Inspection",                                               "$30,000"),
        ("Upon Start Rough MEP",                                                  "$36,000"),
        ("Pass rough MEP",                                                        "$20,000"),
        ("Upon Start Drywall Work",                                               "$16,000"),
        ("Upon Start Exterior Lath",                                              "$15,000"),
        ("Upon finish cabinets installation and start countertop fabrication",    "$22,700"),
        ("Upon pass lath & insulation inspection",                                "$15,000"),
        ("Upon Finish Stucco",                                                    "$20,000"),
        ("Upon Start Roofing For addition",                                       "$14,000"),
        ("Upon Pass Final Inspection",                                            "$21,100"),
        ("Upon Completion final touch ups",                                       "$6,500"),
    ])

    # Output PDF path (None = auto-generate from client name)
    output_path: Optional[str] = None

    def resolve_output(self) -> str:
        if self.output_path:
            return self.output_path
        safe = self.client_name.replace(" ", "_").replace("/", "-")
        base = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, f"DCB_Proposal_{safe}.pdf")

    @classmethod
    def from_json(cls, path: str) -> "ProposalConfig":
        with open(path) as f:
            data = json.load(f)
        cfg = cls()
        for key, val in data.items():
            if hasattr(cfg, key):
                if key == "payments":
                    # Accept [[desc, amount], ...] or [[desc, amount], ...]
                    setattr(cfg, key, [tuple(p) for p in val])
                else:
                    setattr(cfg, key, val)
        return cfg


# ── HTML helpers ─────────────────────────────────────────────────────────────
def _scope_html(items: List[str]) -> str:
    return "\n      ".join(f"<li>{html_lib.escape(item)}</li>" for item in items)


def _payments_html(payments: List[Tuple[str, str]]) -> str:
    rows = []
    for i, (desc, amount) in enumerate(payments, 1):
        rows.append(
            f'<div class="pay-item">'
            f'<span class="pay-num">{i}.</span>'
            f'<span>{html_lib.escape(desc)}: {html_lib.escape(amount)}</span>'
            f'</div>'
        )
    return "\n      ".join(rows)


# ── HTML builder ─────────────────────────────────────────────────────────────
def build_html(cfg: ProposalConfig) -> str:
    e = html_lib.escape  # shorthand for escaping dynamic text

    scope   = _scope_html(cfg.scope_items)
    pays    = _payments_html(cfg.payments)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>

@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@200;300;400;600;700;800&display=swap');

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
  font-family: 'Raleway', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  color: {NAVY};
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}}

@page {{ size: 8.5in 11in; margin: 0; }}

.page {{
  width: 8.5in;
  height: 11in;
  overflow: hidden;
  page-break-after: always;
  position: relative;
}}

/* ====================================================
   PAGE 1: COVER
   ==================================================== */
.cover {{
  background: {GRAY};
  display: flex;
  flex-direction: column;
  height: 11in;
}}

.cover-body {{
  flex: 1;
  padding: 0.55in 0.65in 0.3in 0.65in;
}}

.cover-date {{
  text-align: right;
  font-weight: 700;
  font-size: 12pt;
  letter-spacing: 0.5pt;
  margin-bottom: 0.72in;
  color: {NAVY};
}}

.cover-title {{
  font-size: 68pt;
  font-weight: 200;
  line-height: 1.05;
  margin-bottom: 0.32in;
  color: {NAVY};
}}

.cover-prepared {{
  font-size: 11pt;
  font-weight: 400;
  margin-bottom: 2pt;
}}

.cover-client {{
  font-size: 13.5pt;
  font-weight: 700;
  margin-bottom: 3pt;
}}

.cover-address {{
  font-size: 10.5pt;
  font-weight: 400;
  margin-bottom: 0.22in;
}}

.cover-scope-label {{
  font-size: 10.5pt;
  font-weight: 700;
  margin-bottom: 5pt;
}}

.cover-scope-list {{
  list-style: disc;
  margin-left: 1.25em;
  margin-bottom: 0.2in;
}}

.cover-scope-list li {{
  font-size: 10.5pt;
  line-height: 1.6;
}}

.cover-total {{
  font-size: 19pt;
  font-weight: 700;
}}

.cover-footer {{
  background: {NAVY};
  height: 1.55in;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}}

.logo {{
  color: white;
  font-size: 20pt;
  font-weight: 300;
  letter-spacing: 3pt;
}}

.logo-bold {{ font-weight: 700; }}

/* ====================================================
   PAGE 2: TABLE OF CONTENTS
   ==================================================== */
.toc-page {{
  background: {GRAY};
  height: 11in;
  padding: 0.95in 0.85in 0.85in 0.85in;
}}

.toc-row {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.29in 0;
  border-bottom: 1px solid #b0b0b0;
  font-size: 17.5pt;
  font-weight: 300;
  color: {NAVY};
}}

/* ====================================================
   CONTENT PAGES (shared)
   ==================================================== */
.content {{
  height: 11in;
  padding: 0.44in 0.55in;
  position: relative;
}}

.bg-white {{ background: {WHITE}; }}
.bg-gray  {{ background: {GRAY};  }}

.sec-num {{
  position: absolute;
  top: 0.32in;
  right: 0.55in;
  font-size: 46pt;
  font-weight: 200;
  color: {NAVY};
  line-height: 1;
}}

.sec-title {{
  font-size: 15.5pt;
  font-weight: 700;
  text-align: center;
  line-height: 1.3;
  margin-bottom: 0.2in;
  padding-right: 0.75in; /* clear sec-num */
}}

.sec-title.full-width {{
  padding-right: 0;
}}

.link-line {{
  font-size: 9.5pt;
  font-weight: 700;
  margin-bottom: 0.15in;
}}

.link-line a {{
  color: {NAVY};
  text-decoration: underline;
  font-weight: 700;
  font-size: 9.5pt;
}}

h3 {{
  font-size: 10.5pt;
  font-weight: 700;
  margin-top: 0.12in;
  margin-bottom: 4pt;
  color: {NAVY};
}}

h4 {{
  font-size: 10pt;
  font-weight: 700;
  margin-top: 0.07in;
  margin-bottom: 3pt;
  color: {NAVY};
}}

ul.bl {{
  list-style: disc;
  margin-left: 1.3em;
  margin-bottom: 0.07in;
}}

ul.bl li {{
  font-size: 10pt;
  line-height: 1.48;
  margin-bottom: 1.5pt;
}}

ul.bl-sub {{
  list-style: disc;
  margin-left: 2.5em;
  margin-bottom: 0.04in;
}}

ul.bl-sub li {{
  font-size: 10pt;
  line-height: 1.45;
}}

/* Dense layout for long content pages */
.dense {{
  padding: 0.36in 0.55in;
}}

.dense .sec-title {{
  margin-bottom: 0.12in;
}}

.dense h3 {{
  font-size: 9.5pt;
  margin-top: 6pt;
  margin-bottom: 1pt;
}}

.dense h4 {{
  font-size: 9pt;
  margin-top: 5pt;
  margin-bottom: 1pt;
}}

.dense ul.bl {{
  margin-left: 1.2em;
  margin-bottom: 2pt;
}}

.dense ul.bl li {{
  font-size: 8.5pt;
  line-height: 1.38;
  margin-bottom: 0;
}}

/* ====================================================
   PAGE 7: PAYMENT SCHEDULE
   ==================================================== */
.pay-list {{
  margin-bottom: 0.12in;
  padding-left: 0;
}}

.pay-item {{
  font-size: 10.5pt;
  line-height: 1.72;
  display: flex;
  gap: 3pt;
}}

.pay-num {{
  min-width: 1.4em;
  text-align: right;
  flex-shrink: 0;
}}

.total-line {{
  font-size: 13.5pt;
  font-weight: 700;
  margin: 0.16in 0 0.22in 0;
}}

.allow-label {{
  font-size: 10pt;
  font-weight: 700;
  margin-bottom: 5pt;
}}

ul.allow {{
  list-style: disc;
  margin-left: 1.3em;
}}

ul.allow li {{
  font-size: 9.5pt;
  line-height: 1.6;
}}

/* ====================================================
   PAGE 8: GENERAL NOTES
   ==================================================== */
.notes-rule {{
  border: none;
  border-top: 1.5px solid {NAVY};
  margin: 0.12in 0 0.18in 0;
}}

.notes-list {{
  counter-reset: note-counter;
}}

.note {{
  counter-increment: note-counter;
  font-size: 9pt;
  line-height: 1.44;
  margin-bottom: 3pt;
  padding-left: 1.8em;
  text-indent: -1.8em;
}}

.note::before {{
  content: counter(note-counter) ". ";
  font-weight: 700;
}}

/* ====================================================
   PAGE 9: THANK YOU
   ==================================================== */
.thankyou {{
  background: {NAVY};
  display: flex;
  flex-direction: column;
  height: 11in;
  padding: 0.5in 0.6in 0.55in 0.6in;
}}

.ty-logo {{
  text-align: right;
  color: white;
  font-size: 14pt;
  font-weight: 300;
  letter-spacing: 2pt;
}}

.ty-logo-bold {{ font-weight: 700; }}

.ty-spacer {{ flex: 1; }}

.ty-text {{
  font-size: 78pt;
  font-weight: 200;
  color: white;
  line-height: 1;
  margin-bottom: 1.5in;
}}

.ty-bottom {{
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}}

.ty-arrow {{
  color: white;
  font-size: 28pt;
  font-weight: 200;
}}

.ty-contact {{
  color: white;
  font-size: 10pt;
  text-align: right;
  line-height: 1.7;
}}

.ty-contact a {{
  color: white;
  text-decoration: underline;
  display: block;
}}

</style>
</head>
<body>

<!-- ============================================================
     PAGE 1 — COVER
     ============================================================ -->
<div class="page cover">
  <div class="cover-body">
    <div class="cover-date">{e(cfg.proposal_date)}</div>
    <div class="cover-title">Project<br>Proposal</div>
    <div class="cover-prepared">Prepared for</div>
    <div class="cover-client">{e(cfg.client_name)}</div>
    <div class="cover-address">{e(cfg.client_address)}</div>
    <div class="cover-scope-label">Project Scope:</div>
    <ul class="cover-scope-list">
      {scope}
    </ul>
    <div class="cover-total">Project Total: {e(cfg.project_total)}</div>
  </div>
  <div class="cover-footer">
    <div class="logo"><span class="logo-bold">D&amp;C</span> | BUILDERS</div>
  </div>
</div>

<!-- ============================================================
     PAGE 2 — TABLE OF CONTENTS
     ============================================================ -->
<div class="page toc-page">
  <div class="toc-row"><span>Design, Architectural &amp; Engineering</span><span>01</span></div>
  <div class="toc-row"><span>1st story Addition &amp; Interior Remodel</span><span>02</span></div>
  <div class="toc-row"><span>Kitchen &amp; Electric Fireplace</span><span>04</span></div>
  <div class="toc-row"><span>Payment Schedule &amp; Allowances</span><span>05</span></div>
  <div class="toc-row"><span>General Notes</span><span>06</span></div>
</div>

<!-- ============================================================
     PAGE 3 — SECTION 01: Design, Architectural & Engineering
     ============================================================ -->
<div class="page">
  <div class="content bg-gray">
    <div class="sec-num">01</div>
    <div class="sec-title">Design, Architectural &amp;<br>Engineering</div>

    <div class="link-line">Design: View some of our-----&gt;&nbsp;<a href="https://www.dropbox.com/scl/fo/9b1hgl3gkk5wnihz6hlnt/AEdBIxCvcdq-OKHswSOE1ps">LATEST DESIGNS</a></div>

    <ul class="bl">
      <li>Conduct multiple in-depth meetings with the client to fully understand their design preferences, lifestyle needs, and aesthetic goals.</li>
    </ul>
    <ul class="bl-sub">
      <li>Discuss design styles (e.g., modern, contemporary, craftsman, etc.).</li>
      <li>Explore functional priorities (e.g., flow of spaces, natural light, use of materials).</li>
      <li>Company will allow time for multiple rounds of feedback, revisions, and updates to the plans based on client preferences and functional needs.</li>
    </ul>

    <h3>Architectural</h3>
    <h4>Develop detailed architectural plans, which will include:</h4>
    <ul class="bl">
      <li>Floor plans: Complete, to-scale drawings of all floors, including room layouts, dimensions, and functional spaces.</li>
      <li>Elevations: Exterior and interior elevations showing heights, proportions, and relationships between materials and design elements.</li>
      <li>Sections: Cross-sectional drawings to depict vertical relationships and construction details.</li>
      <li>Construction Documents: Preparation of complete construction drawings and specifications, including necessary details, schedules, and other relevant documentation required for obtaining building permits.</li>
      <li>Permit Acquisition: Assistance in the permit acquisition process, including the submission of all necessary documents and coordination with the relevant authorities until the permits are obtained.</li>
    </ul>

    <h3>Engineering</h3>
    <ul class="bl">
      <li>Work with a structural engineer and develop structural plans to ensure that the design is feasible and that the home maintains structural integrity.</li>
      <li>Determine the required changes or reinforcements for removing or altering load-bearing walls in the kitchen and living room areas.</li>
      <li>Create detailed framing plans to ensure the foundation, beams, and supports meet the engineering requirements.</li>
    </ul>

    <h4>Inspiration and Mood Boards:</h4>
    <ul class="bl">
      <li>Develop a mood board or design inspiration board based on the client's preferences, including colors, textures, materials, and themes.</li>
      <li>Specific design features the client wishes to incorporate will be illustrated.</li>
    </ul>

    <h4>Preliminary Space Planning:</h4>
    <ul class="bl">
      <li>Collaborate on initial space planning concepts, laying out potential floor plans and room adjacencies to achieve the desired flow.</li>
      <li>Create rough sketches or 3D renderings to help the client visualize the possibilities.</li>
      <li>Incorporate initial feedback into the design, refining it to meet aesthetic and functional goals.</li>
    </ul>
  </div>
</div>

<!-- ============================================================
     PAGE 4 — SECTION 02: 1st story Addition (items 1–5)
     ============================================================ -->
<div class="page">
  <div class="content bg-gray dense">
    <div class="sec-num">02</div>
    <div class="sec-title">1st story Addition &amp; Interior Remodel</div>

    <h4>1. Site Preparation &amp; Demo:</h4>
    <ul class="bl">
      <li>Cover work areas as needed.</li>
      <li>Provide portable toilet for workers for the duration of the project as necessary.</li>
      <li>Demo interior walls, flooring, chimney, kitchen and fixtures as specified in the plans.</li>
      <li>Company will remove existing pavers and will stack them on the side (we will reset them after finishing work and its included in the scope of work — additional hardscape work will be discussed during the project).</li>
      <li>Remove and haul away all demo debris from the job site.</li>
    </ul>

    <h4>2. Foundation</h4>
    <ul class="bl">
      <li>Install necessary electrical stub-outs per plan.</li>
      <li>Form new foundation per plan.</li>
      <li>Install rebars per plan.</li>
      <li>Pour concrete foundation according to architectural and structural plans.</li>
      <li>Allow curing time and inspect for structural integrity.</li>
      <li>Pass all foundation inspection required by the city in order to proceed with the project.</li>
    </ul>

    <h4>3. Framing:</h4>
    <ul class="bl">
      <li>Frame new walls according to the approved layout and plans.</li>
      <li>Frame new door openings, and any architectural features following plans as needed.</li>
      <li>Install new structural supports, headers, shear walls, and beams as required (per engineer's specifications).</li>
      <li>Pass framing inspection.</li>
    </ul>

    <h4>4. Plumbing and Electrical:</h4>
    <h4>4.1 Electrical Rough In:</h4>
    <ul class="bl">
      <li>Install new electrical wiring in new designated areas.</li>
      <li>Install/upgrade new 200AMP per plans.</li>
      <li>Position outlets, light fixtures, and switches according to the plans.</li>
      <li>Ensure wiring is up to code and ready for inspection.</li>
      <li>Pass rough electrical inspection.</li>
    </ul>

    <h4>4.2 Electrical Finishing:</h4>
    <ul class="bl">
      <li>Install standard LED recessed light per plan.</li>
      <li>Install outlets as needed and up to code.</li>
      <li>Install new switches to control lights per plan in new house.</li>
      <li>All new outlets and switches to be standard white decor.</li>
      <li>Install Water rated led recessed light in the powder room as needed.</li>
      <li>Install Ceiling exhaust fan above toilet in powder room.</li>
    </ul>

    <h4>4.3 Plumbing Rough In:</h4>
    <ul class="bl">
      <li>Company will Run new water supply and drain lines for sinks, toilet for powder room, and any other fixtures according to plans.</li>
      <li>Company will prepare all necessary plumbing for new tankless water heater, company will provide new tankless water heat from company options.</li>
    </ul>

    <h4>4.4 Plumbing Finishing:</h4>
    <ul class="bl">
      <li>Install final plumbing fixtures, faucets, toilet, and sinks.</li>
      <li>Test water pressure and drainage to insure everything is working properly.</li>
      <li>Pass rough plumbing inspection.</li>
    </ul>

    <h4>5. Roofing:</h4>
    <ul class="bl">
      <li>Install new roof sheathing according to plan in front new addition area.</li>
      <li>Install new waterproofing underlayment per code.</li>
      <li>Install 30 lbs. tar paper and cool roof composition shingles per plan to match existing as possible.</li>
      <li>Install new metal flashing on all new pipes and vents per plan.</li>
    </ul>
  </div>
</div>

<!-- ============================================================
     PAGE 5 — SECTION 03: 1st story Addition (items 6–11)
     ============================================================ -->
<div class="page">
  <div class="content bg-gray dense">
    <div class="sec-num">03</div>
    <div class="sec-title">1st story Addition &amp; Interior Remodel</div>

    <h4>6. Insulation, Drywall &amp; Paint:</h4>
    <ul class="bl">
      <li>Install standard insulation in walls per title 24 plan in designated work areas.</li>
      <li>Install standard insulation above ceiling per title 24 plan in designated work areas.</li>
      <li>Install drywall on all walls and ceiling per plan.</li>
      <li>Apply tape and mud and on all joints of new drywalls. Drywall Will be level 3.</li>
      <li>Apply one coat of primer on interior walls, ceiling, baseboards, casing and as needed per plan in designated work areas.</li>
      <li>Apply two coats of paint on interior walls, ceiling, baseboards and as needed per plan in designated work areas (customer to choose from company's options).</li>
      <li>Note: Standard Dunn Edwards / Benjamin Moore paint from company's options is included, specialty paint such as lime wash &amp; venetian plaster will be extra.</li>
    </ul>

    <h4>7. Windows &amp; Exterior Doors:</h4>
    <ul class="bl">
      <li>Flash and seal windows and exterior doors to ensure weather tightness.</li>
      <li>Install new exterior doors and hardware following plans.</li>
      <li>Install new vinyl windows per title 24 and per architectural plan and engineering calculations (see allowance section).</li>
    </ul>

    <h4>8. Exterior Finish &amp; Re-stucco:</h4>
    <ul class="bl">
      <li>Install waterproof tar paper and chicken wire around new windows and exterior doors in addition area as needed per plan.</li>
      <li>Cover doors, windows and work area as needed with plastic. Install moisture barrier on new framing in addition work areas.</li>
      <li>Install metal lath over moisture barrier. Scratch coat all new walls.</li>
      <li>Brown coat after scratch coat has cured. Apply "Santa barbara" finish or smooth stucco finish coat and texture.</li>
    </ul>
    <h4>Re-stucco existing house:</h4>
    <ul class="bl">
      <li>Pressure wash existing stucco exterior surfaces as needed. Prep all walls for re-coat application, including scraping/grinding loose areas as required.</li>
      <li>Patch cracks and damaged areas with mortar mix reinforced with fiber as needed.</li>
      <li>Install fiberglass mesh at repaired areas and crack-prone sections as needed for improved crack resistance.</li>
      <li>Apply one base coat then new stucco finish (smooth or Santa barbara) across all designated exterior wall surfaces per client request.</li>
      <li>Client to select finish color from company catalog. Prime and paint fascia boards and trim.</li>
    </ul>

    <h4>9.1 Flooring:</h4>
    <ul class="bl">
      <li>Demo existing flooring and haul away the debris. Prep the floor as needed.</li>
      <li>Install LVP floors all throughout the house (see allowance section). Provide and install MDF baseboards from company's options.</li>
    </ul>

    <h4>9.2 Interior Doors &amp; Windows:</h4>
    <ul class="bl">
      <li>Install new interior doors, door hardware, and baseboards.</li>
      <li>Apply trim around windows and doors for a finished look. Install new exterior and interior doors.</li>
    </ul>

    <h4>9.3 Powder Room:</h4>
    <ul class="bl">
      <li>Company will install tile in the new powder room area, client to provide the tile.</li>
      <li>Company will install new vanity (customer to provide) and all powder room fixtures (customer to provide finished material).</li>
      <li>Hook up plumbing fixtures and ensure proper functionality.</li>
    </ul>

    <h4>10. HVAC/Ducting Work:</h4>
    <ul class="bl">
      <li>Ensure that all gas lines are pressure tested for leaks before closing up walls.</li>
      <li>Run new ductings all throughout the new addition area as needed.</li>
      <li>Company will not replace existing HVAC unit and only will run ductings to new areas.</li>
    </ul>

    <h4>11. Final Cleanup and Punch List:</h4>
    <ul class="bl">
      <li>Conduct detailed cleanup of all construction areas. Remove all construction debris, dust, and materials from site.</li>
      <li>Perform final walkthrough with client to identify any remaining punch list items.</li>
      <li>Complete all final touch-ups before project closeout.</li>
    </ul>
  </div>
</div>

<!-- ============================================================
     PAGE 6 — SECTION 04: Kitchen & Electric Fireplace
     ============================================================ -->
<div class="page">
  <div class="content bg-gray">
    <div class="sec-num">04</div>
    <div class="sec-title">Kitchen &amp; Electric Fireplace</div>

    <h3>Kitchen 3D Design</h3>
    <ul class="bl">
      <li>Company will provide a 3D design prior to starting any work, the client have up to 3 revisions.</li>
      <li>The purpose of the design is to make sure the new layout of the cabinets is clear (the color in the render will not never 100% match the color of the actual cabinet).</li>
      <li>Company will provide in-person samples when finalizing the cabinets colors.</li>
    </ul>

    <h3>Prefabricated Cabinets installation, material and labor</h3>
    <ul class="bl">
      <li>Purchasing material, building and installing prefab cabinets according to current agreed upon layout with the client.</li>
      <li>Adding fillers and panels where needed installing all the soft closing hardware and installing the handles for all the cabinets.</li>
      <li>Customer to choose from company's shaker options.</li>
    </ul>

    <h3>Prefabricated Countertops, installation labor and material</h3>
    <ul class="bl">
      <li>Fabrication of pre fab quartz counter tops, adjust prefabs to size.</li>
      <li>Fabricate under-mount sink, fabricate new layout core up to 5 holes in the counter-sink area.</li>
      <li>Installation labor and material are included.</li>
      <li>Material is prefab quartz, customer to choose from company's options, material is included.</li>
      <li>In case the client wants to do a different material for the counters it will be an additional cost.</li>
    </ul>

    <h3>Backsplash</h3>
    <ul class="bl">
      <li>Demo current tiles in backsplash.</li>
      <li>Drywall and prepare area for new backsplash installation.</li>
      <li>Install standard tiles in the backsplash area.</li>
      <li>If the backsplash is full slab, it will be an additional cost.</li>
    </ul>

    <h3>Paint The Kitchen</h3>
    <ul class="bl">
      <li>Prepare and cover all work area for paint.</li>
      <li>Match current texture in the kitchen as much as possible.</li>
      <li>Lay one coat of primer.</li>
      <li>Lay two coats of paint, client to choose from company's options and colors.</li>
      <li>Clean up area and haul away debris.</li>
    </ul>

    <h3>Electric Fireplace</h3>
    <ul class="bl">
      <li>Company will run necessary electric for the new electric fireplace, customer to provide the fireplace fixtures.</li>
    </ul>
  </div>
</div>

<!-- ============================================================
     PAGE 7 — SECTION 05: Payment Schedule & Allowances
     ============================================================ -->
<div class="page">
  <div class="content bg-gray">
    <div class="sec-num">05</div>
    <div class="sec-title full-width">Payment Schedule</div>

    <div class="pay-list">
      {pays}
    </div>

    <div class="total-line">Project Total: {e(cfg.project_total)}</div>

    <div class="allow-label">Allowances:</div>
    <ul class="allow">
      <li>Company will provide allowance for SPC/ Vinyl for up to $3/sqft.</li>
      <li>Company will provide allowance for tile installation in backsplash kitchen up to $5/sqft.</li>
      <li>Company will provide allowance for tile installation in the powder room up to $5/sqft.</li>
      <li>Company will provide allowance for windows up to $300 per window.</li>
      <li>Company will provide allowance for tankless water heater of up to $1,700.</li>
    </ul>
  </div>
</div>

<!-- ============================================================
     PAGE 8 — SECTION 06: General Notes
     ============================================================ -->
<div class="page">
  <div class="content bg-gray">
    <div class="sec-num">06</div>
    <div class="sec-title full-width">General Notes</div>
    <hr class="notes-rule">

    <div class="notes-list">
      <div class="note">Contractor will pull permit under his license and Customer will reimburse permit fees.</div>
      <div class="note">Blueprints provided by Contractor will include a full set of architectural drawings, structural calculations, Title 24 calculations. Blueprints do not include any slope analysis, topographical or soil reports if required.</div>
      <div class="note">Any coastal commission requirements will be quoted separately and accordingly.</div>
      <div class="note">Any structural observation fees or deputy inspector fees related to the project will be paid by the Contractor and reimbursed by the Customer.</div>
      <div class="note">Contractor will install his sign in front of the house for the duration of the project.</div>
      <div class="note">Contractor will provide a portable toilet for the duration of the project.</div>
      <div class="note">Company will provide prefabricated quartz slabs, customer to choose from company's options.</div>
      <div class="note">Granite or any other natural stone may have cracks, veins, seams, fissures, etc. and Contractor is not responsible for the imperfections of a natural slab.</div>
      <div class="note">Glass or stone tile will require additional work at extra cost.</div>
      <div class="note">Tile in shower pan should be of smaller pieces of tile or even mosaic to allow proper slope and should be a non-slip surface.</div>
      <div class="note">Customer will provide all tiles, grout, appliances, plumbing fixtures, exhaust fans, and any light fixtures other than recessed lights (check allowance section).</div>
      <div class="note">Any low voltage work such as phones, cable, alarm, computer, sound, cameras etc. as well as the consequences of such work is not included and are to be done by Customer.</div>
      <div class="note">Any changes to electrical outlets or switches, such as difference in color, style, or dimmers, are to be provided by Customer unless stated differently in the estimate.</div>
      <div class="note">Job does not include any fire sprinkler system if required by the city.</div>
      <div class="note">Contractor cannot take responsibility for any existing item(s) set aside or delivered to the job site, including but not limited to appliances &amp; finished materials.</div>
      <div class="note">Job does not include any fire sprinkler system if required by the city.</div>
      <div class="note">Job does not include any landscaping work such as: tree removal, flowers or irrigation sprinklers, revival of grass area etc. as well as any hardscape, walkways, driveway etc.</div>
      <div class="note">Contractor will do their best to keep job site clean and protected, will cover the floors and/or place plastic from floors to ceiling to avoid dirt and dust from spreading. Contractor will pick up &amp; remove large debris at the end of the job, but final cleaning is to be done by Customer as Contractor is not a cleaning company.</div>
      <div class="note">Job site area is an active construction zone. To avoid any damage to customer property, contractor strongly recommends any items of value be relocated prior to the project start date.</div>
      <div class="note">Customer agrees not to talk directly to workers and only to the assigned project coordinator in the office in order for us to effectively manage the job and to give the best possible customer service.</div>
      <div class="note">Customer agrees to give Contractor access to the job site for the entire project duration, Monday through Saturday, between the hours of 8am-5pm for all work, delivery of material, and inspections.</div>
      <div class="note">Customer understands that certain workdays may be shortened, or no work conducted due to scheduled inspection, bad weather, crew scheduling efficiencies, waiting on ordered materials, etc.</div>
      <div class="note">If any lead, asbestos, and mold are found, they will be quoted separately by a licensed remediation or abatement company.</div>
      <div class="note">Any attached computer-generated drawings are simply an aesthetic representation of the project. They do not reflect the actual tile or finishes the customer ultimately chooses.</div>
      <div class="note">Larger scale interior remodel or addition projects are disruptive by nature due to the work involved. Contractor strongly advises that the Customer relocate during the construction phase of the project.</div>
      <div class="note">Customer understands that the above specifications are the actual final agreement between Customer and for work to be done. No other verbal promises by representative / salesperson are included in this contract.</div>
      <div class="note">Any unforeseen relocation of A/C ducts, gas lines, plumbing or electrical issues that need to be addressed after opening walls, as well as lack of insulation will be quoted separately and accordingly.</div>
      <div class="note">Interior paint will not include doors, shelving, casings, windows, shutters, or any other cabinets unless specially mentioned in the above specification.</div>
      <div class="note">If the city requires us to build a brand new gas system it will be an additional charge.</div>
    </div>
  </div>
</div>

<!-- ============================================================
     PAGE 9 — THANK YOU
     ============================================================ -->
<div class="page thankyou">
  <div class="ty-logo"><span class="ty-logo-bold">D&amp;C</span> | BUILDERS</div>
  <div class="ty-spacer"></div>
  <div class="ty-text">Thank you.</div>
  <div class="ty-bottom">
    <div class="ty-arrow">&#8594;</div>
    <div class="ty-contact">
      <a href="https://designandcreatebuilders.com">designandcreatebuilders.com</a>
      License Number: 1116111
    </div>
  </div>
</div>

</body>
</html>"""


# ── CLI ───────────────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a D&C Builders proposal PDF.")
    p.add_argument("--json",    metavar="FILE",   help="Load config from a JSON file")
    p.add_argument("--client",  metavar="NAME",   help="Client full name")
    p.add_argument("--address", metavar="ADDR",   help="Client address")
    p.add_argument("--date",    metavar="DATE",   help='Proposal date, e.g. "March 2026"')
    p.add_argument("--total",   metavar="AMOUNT", help='Project total, e.g. "$150,000"')
    p.add_argument("--output",  metavar="PATH",   help="Output PDF file path")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    # Start from defaults, then apply JSON file, then CLI overrides
    cfg = ProposalConfig.from_json(args.json) if args.json else ProposalConfig()

    if args.client:  cfg.client_name    = args.client
    if args.address: cfg.client_address = args.address
    if args.date:    cfg.proposal_date  = args.date
    if args.total:   cfg.project_total  = args.total
    if args.output:  cfg.output_path    = args.output

    output = cfg.resolve_output()
    print(f"Client  : {cfg.client_name}")
    print(f"Address : {cfg.client_address}")
    print(f"Date    : {cfg.proposal_date}")
    print(f"Total   : {cfg.project_total}")
    print(f"Output  : {output}")
    print("Generating PDF...")

    HTML(string=build_html(cfg), base_url=".").write_pdf(output)
    print(f"Done! Saved to:\n  {output}")


if __name__ == "__main__":
    main()
