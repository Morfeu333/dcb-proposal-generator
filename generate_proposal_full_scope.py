#!/usr/bin/env python3
"""D&C Builders — Full Scope Proposal PDF Generator

Extended template that covers all major scope sections:
Plans & Engineering, 2nd Story Addition, Kitchen, Master Bath,
ADU Conversion, Roofing, Payment Schedule, General Notes.

Run:
    DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 generate_proposal_full_scope.py
    DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 generate_proposal_full_scope.py --json clients/test_martinez_full_scope.json
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
    client_name:    str = "Robert & Angela Martinez"
    client_address: str = "4821 Seabreeze Lane, Huntington Beach, CA 92648"
    proposal_date:  str = "March 2026"
    project_total:  str = "$541,000"

    scope_items: List[str] = field(default_factory=lambda: [
        "Plans & Engineering",
        "Full 2nd Story Addition (1,200 SF)",
        "Complete Kitchen Remodel",
        "Master Bathroom Remodel",
        "Garage Conversion to ADU (400 SF)",
        "Roofing (Full Replacement)",
    ])

    payments: List[Tuple[str, str]] = field(default_factory=lambda: [
        ("Down payment",                                               "$1,000"),
        ("Mobilization & Start Architectural Design",                  "$18,000"),
        ("Upon Plans Approval & Permit Submission",                    "$12,000"),
        ("Site Prep & Start Demo",                                     "$35,000"),
        ("Upon Start Foundation Work (Slab on Grade)",                 "$38,000"),
        ("Upon Foundation Inspection Approval",                        "$25,000"),
        ("Upon Start Framing (Wood Framing)",                          "$48,000"),
        ("Pass Framing Inspection",                                    "$35,000"),
        ("Upon Start Rough MEP",                                       "$42,000"),
        ("Pass Rough MEP Inspection",                                  "$28,000"),
        ("Upon Start Drywall & Insulation",                            "$22,000"),
        ("Upon Start Exterior Lath & Stucco",                          "$20,000"),
        ("Upon Start Kitchen Cabinet Installation (Custom Shaker)",    "$35,000"),
        ("Upon Start Countertop Fabrication (Quartz)",                 "$18,000"),
        ("Upon Pass Lath & Insulation Inspection",                     "$15,000"),
        ("Upon Finish Stucco & Exterior Paint",                        "$22,000"),
        ("Upon Start Tile Roof Installation",                          "$28,000"),
        ("Upon Start Master Bath Tile Work (Porcelain)",               "$16,000"),
        ("Upon Start ADU Interior Finishes",                           "$24,000"),
        ("Upon Start Hardwood Flooring (Engineered Wood)",             "$18,000"),
        ("Upon Pass Final Inspection",                                 "$28,000"),
        ("Upon Completion & Final Punch List",                         "$12,000"),
    ])

    output_path: Optional[str] = None

    def resolve_output(self) -> str:
        if self.output_path:
            return self.output_path
        safe = self.client_name.replace(" ", "_").replace("/", "-").replace("&", "&")
        base = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, f"DCB_Proposal_{safe}_FullScope.pdf")

    @classmethod
    def from_json(cls, path: str) -> "ProposalConfig":
        with open(path) as f:
            data = json.load(f)
        cfg = cls()
        for key, val in data.items():
            if hasattr(cfg, key):
                if key == "payments":
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
    e = html_lib.escape
    scope = _scope_html(cfg.scope_items)
    pays  = _payments_html(cfg.payments)

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
  padding: 0.22in 0;
  border-bottom: 1px solid #b0b0b0;
  font-size: 16pt;
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
  background: {GRAY};
}}

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
  padding-right: 0.75in;
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
  margin-top: 0.09in;
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
  margin-bottom: 2pt;
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
   PAYMENT SCHEDULE
   ==================================================== */
.pay-list {{
  margin-bottom: 0.12in;
  padding-left: 0;
}}

.pay-item {{
  font-size: 10pt;
  line-height: 1.65;
  display: flex;
  gap: 3pt;
}}

.pay-num {{
  min-width: 1.6em;
  text-align: right;
  flex-shrink: 0;
}}

.total-line {{
  font-size: 13.5pt;
  font-weight: 700;
  margin: 0.14in 0 0.18in 0;
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
   GENERAL NOTES
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
   THANK YOU
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
  <div class="toc-row"><span>Full 2nd Story Addition — Part 1</span><span>02</span></div>
  <div class="toc-row"><span>Full 2nd Story Addition — Part 2</span><span>03</span></div>
  <div class="toc-row"><span>Complete Kitchen Remodel</span><span>04</span></div>
  <div class="toc-row"><span>Master Bathroom Remodel</span><span>05</span></div>
  <div class="toc-row"><span>Garage Conversion to ADU</span><span>06</span></div>
  <div class="toc-row"><span>Roofing — Full Replacement</span><span>07</span></div>
  <div class="toc-row"><span>Payment Schedule</span><span>08</span></div>
  <div class="toc-row"><span>General Notes</span><span>09</span></div>
</div>

<!-- ============================================================
     PAGE 3 — SECTION 01: Design, Architectural & Engineering
     ============================================================ -->
<div class="page">
  <div class="content">
    <div class="sec-num">01</div>
    <div class="sec-title">Design, Architectural &amp;<br>Engineering</div>

    <div class="link-line">Design: View some of our-----&gt;&nbsp;<a href="https://www.dropbox.com/scl/fo/9b1hgl3gkk5wnihz6hlnt/AEdBIxCvcdq-OKHswSOE1ps">LATEST DESIGNS</a></div>

    <ul class="bl">
      <li>Conduct multiple in-depth meetings with the client to fully understand their design preferences, lifestyle needs, and aesthetic goals for the full 2nd story addition and all remodel scopes.</li>
    </ul>
    <ul class="bl-sub">
      <li>Discuss design styles (modern, contemporary, craftsman, etc.).</li>
      <li>Explore functional priorities — room flow, natural light, ceiling heights, and material selections.</li>
      <li>Multiple rounds of feedback, revisions, and updates based on client preferences.</li>
    </ul>

    <h3>Architectural</h3>
    <h4>Full set of architectural drawings will include:</h4>
    <ul class="bl">
      <li>Floor plans: Complete, to-scale drawings of all floors including new 2nd story layout, room dimensions, and functional spaces.</li>
      <li>Elevations: Exterior and interior elevations showing heights, proportions, and material relationships for both stories.</li>
      <li>Sections: Cross-sectional drawings depicting vertical relationships between 1st and 2nd story construction details.</li>
      <li>Construction Documents: Full construction drawings and specifications including details, schedules, and all documentation required for building permits.</li>
      <li>Permit Acquisition: Submission of all necessary documents and coordination with the city until permits are obtained.</li>
    </ul>

    <h3>Engineering</h3>
    <ul class="bl">
      <li>Work with a licensed structural engineer to develop structural plans ensuring the existing foundation and framing support the new 2nd story load.</li>
      <li>Structural calculations for new slab on grade, shear walls, beams, headers, and lateral bracing per engineering requirements.</li>
      <li>Title 24 energy compliance calculations for all new additions and remodeled spaces.</li>
      <li>Soils report coordination if required by the city.</li>
    </ul>

    <h4>3D Renderings &amp; Mood Boards:</h4>
    <ul class="bl">
      <li>Develop design inspiration boards based on client preferences including colors, textures, materials, and finish themes.</li>
      <li>3D renderings provided for kitchen, master bathroom, ADU, and exterior elevations for client visualization and approval before construction begins.</li>
    </ul>
  </div>
</div>

<!-- ============================================================
     PAGE 4 — SECTION 02: Full 2nd Story Addition — Part 1
     ============================================================ -->
<div class="page">
  <div class="content dense">
    <div class="sec-num">02</div>
    <div class="sec-title">Full 2nd Story Addition (1,200 SF)<br>Site Prep, Foundation &amp; Framing</div>

    <h4>1. Site Preparation &amp; Demo:</h4>
    <ul class="bl">
      <li>Cover and protect all existing 1st floor living areas with plastic sheeting and protective materials throughout construction.</li>
      <li>Provide portable toilet and secured material staging area for the duration of the project.</li>
      <li>Remove existing roof structure, roof covering, sheathing, and any attic insulation as needed per plans.</li>
      <li>Demo any existing ceiling framing, light fixtures, HVAC ducting, and utilities that conflict with new 2nd story structure.</li>
      <li>Remove and haul away all demo debris from the job site promptly.</li>
    </ul>

    <h4>2. Foundation — Slab on Grade (where applicable):</h4>
    <ul class="bl">
      <li>Assess and reinforce existing 1st story foundation and perimeter footings as required by structural engineer to carry new 2nd story load.</li>
      <li>Pour new slab on grade for any new footprint areas per structural plans.</li>
      <li>Install grade beams, anchor bolts, and hold-downs per engineering specifications.</li>
      <li>Install all required electrical and plumbing stub-outs prior to pour.</li>
      <li>Allow adequate curing time and pass all required foundation inspections before proceeding.</li>
    </ul>

    <h4>3. Wood Framing — 2nd Story (1,200 SF):</h4>
    <ul class="bl">
      <li>Frame all new 2nd story walls, bearing walls, and partition walls per approved architectural and structural plans.</li>
      <li>Install engineered lumber (LVL beams, ridge beams, flush beams) per structural engineer specifications.</li>
      <li>Install all shear walls, hold-downs, and lateral bracing as required by engineering calculations.</li>
      <li>Frame new staircase opening and install stair framing per plans.</li>
      <li>Frame all new window and door openings with proper headers per plans.</li>
      <li>Install 2nd story floor system with engineered floor joists or TJIs per structural plans.</li>
      <li>Frame new roof structure — rafters, ridge board, hip/valley framing, and roof sheathing per architectural plans.</li>
      <li>Pass framing inspection before any concealed work proceeds.</li>
    </ul>

    <h4>4. Exterior Sheathing &amp; Weather Barrier:</h4>
    <ul class="bl">
      <li>Install structural plywood or OSB sheathing on all new exterior walls per plans.</li>
      <li>Apply moisture-resistant house wrap over all new exterior framing.</li>
      <li>Install all window and door flashing per waterproofing best practices prior to window installation.</li>
    </ul>

    <h4>5. Windows &amp; Exterior Doors — 2nd Story:</h4>
    <ul class="bl">
      <li>Install new vinyl dual-pane windows per Title 24 requirements and architectural plans (see allowance section).</li>
      <li>Install new exterior doors and hardware at 2nd story access points per plans.</li>
      <li>Flash and seal all windows and doors for complete weather tightness.</li>
    </ul>
  </div>
</div>

<!-- ============================================================
     PAGE 5 — SECTION 03: Full 2nd Story Addition — Part 2
     ============================================================ -->
<div class="page">
  <div class="content dense">
    <div class="sec-num">03</div>
    <div class="sec-title">Full 2nd Story Addition (1,200 SF)<br>MEP, Insulation &amp; Interior Finishes</div>

    <h4>6. Rough MEP — Mechanical, Electrical &amp; Plumbing:</h4>
    <ul class="bl">
      <li>Run all new electrical wiring throughout 2nd story per plans — circuits, panel capacity upgrade if required, outlets, switches, and lighting.</li>
      <li>Install all new plumbing supply and drain lines for 2nd story bathrooms, laundry, and any other wet areas per plans.</li>
      <li>Run new HVAC ducting throughout 2nd story, extending or upgrading existing system capacity as needed per Title 24 compliance.</li>
      <li>Install exhaust fans in all new bathrooms per code.</li>
      <li>Pass all rough MEP inspections (electrical, plumbing, mechanical) prior to closing walls.</li>
    </ul>

    <h4>7. Insulation &amp; Drywall:</h4>
    <ul class="bl">
      <li>Install batt insulation in all 2nd story exterior walls and ceiling per Title 24 energy calculations.</li>
      <li>Install sound insulation between 1st and 2nd floor ceiling/floor assemblies in designated areas.</li>
      <li>Hang drywall on all 2nd story walls and ceilings per plan.</li>
      <li>Tape, mud, and finish all joints to Level 4 finish on walls; Level 5 on ceilings where specified.</li>
      <li>Apply one coat primer and two coats paint throughout 2nd story (customer selects from company options).</li>
    </ul>

    <h4>8. Exterior Lath &amp; Stucco — 2nd Story:</h4>
    <ul class="bl">
      <li>Install moisture barrier and galvanized metal lath over all new 2nd story exterior framing.</li>
      <li>Apply scratch coat, brown coat, and finish coat (Santa Barbara or smooth finish per client selection).</li>
      <li>Blend and match stucco finish and color to existing 1st story exterior as closely as possible.</li>
      <li>Pass lath and insulation inspection prior to brown coat application.</li>
    </ul>

    <h4>9. Interior Doors, Hardware &amp; Trim:</h4>
    <ul class="bl">
      <li>Install all new interior doors, door hardware, and door casings throughout 2nd story per plans.</li>
      <li>Install MDF baseboards throughout all 2nd story rooms from company options.</li>
      <li>Apply window trim and casing at all interior window openings.</li>
    </ul>

    <h4>10. Flooring — Engineered Hardwood:</h4>
    <ul class="bl">
      <li>Prepare subfloor — level, clean, and install moisture barrier as required.</li>
      <li>Install engineered hardwood flooring throughout all 2nd story living areas per allowance (see allowance section).</li>
      <li>Install tile flooring in all 2nd story bathroom and wet areas (customer to provide tile).</li>
    </ul>

    <h4>11. Staircase:</h4>
    <ul class="bl">
      <li>Build and install new staircase connecting 1st and 2nd story per architectural plans and code.</li>
      <li>Install handrail and guardrail per code requirements.</li>
      <li>Apply finish material to treads and risers to match or complement flooring selections.</li>
    </ul>

    <h4>12. Final Cleanup &amp; Punch List — 2nd Story:</h4>
    <ul class="bl">
      <li>Conduct thorough cleanup of all 2nd story construction areas upon substantial completion.</li>
      <li>Perform final walkthrough with client to identify and complete all punch list items.</li>
    </ul>
  </div>
</div>

<!-- ============================================================
     PAGE 6 — SECTION 04: Complete Kitchen Remodel
     ============================================================ -->
<div class="page">
  <div class="content">
    <div class="sec-num">04</div>
    <div class="sec-title">Complete Kitchen Remodel</div>

    <h3>Kitchen 3D Design</h3>
    <ul class="bl">
      <li>Company will provide a full 3D kitchen design prior to starting any work — client has up to 3 revisions included.</li>
      <li>Design will confirm cabinet layout, island dimensions, appliance placement, and traffic flow.</li>
      <li>Company will provide in-person material samples for cabinets, countertops, and backsplash before finalizing selections.</li>
    </ul>

    <h3>Demo &amp; Preparation</h3>
    <ul class="bl">
      <li>Demo and remove existing cabinets, countertops, backsplash tile, and flooring in kitchen area.</li>
      <li>Patch and repair walls, ceiling, and subfloor as needed in preparation for new work.</li>
      <li>Relocate plumbing and electrical as required per new kitchen layout and plans.</li>
    </ul>

    <h3>Custom Shaker Cabinet Installation</h3>
    <ul class="bl">
      <li>Supply and install custom shaker-style cabinets — upper, lower, and island — per approved 3D layout.</li>
      <li>Install all fillers, panels, and crown molding as specified.</li>
      <li>Install all soft-close hinges, drawer slides, and customer-selected hardware throughout.</li>
    </ul>

    <h3>Quartz Countertop Fabrication &amp; Installation</h3>
    <ul class="bl">
      <li>Fabricate and install prefabricated quartz countertops throughout kitchen including island — customer selects slab from company options.</li>
      <li>Fabricate and install under-mount kitchen sink cutout and up to 5 additional cutouts (cooktop, faucet, etc.).</li>
      <li>All edge profiles, seams, and polish included. Natural stone upcharge applies if customer selects outside company slab options.</li>
    </ul>

    <h3>Backsplash</h3>
    <ul class="bl">
      <li>Prepare walls and install cement board backer as needed in backsplash areas.</li>
      <li>Install standard tile backsplash per client selection (customer to provide tile). Full slab backsplash is an additional cost.</li>
      <li>Grout, seal, and complete all tile work to a finish-ready condition.</li>
    </ul>

    <h3>Plumbing &amp; Electrical Finishing</h3>
    <ul class="bl">
      <li>Install new kitchen sink, faucet, disposal hookup, and dishwasher connection (customer to provide fixtures and appliances).</li>
      <li>Install recessed LED lighting, under-cabinet lighting rough-in, and all kitchen outlets and switches per plans.</li>
    </ul>

    <h3>Paint</h3>
    <ul class="bl">
      <li>Apply one coat primer and two coats paint on all kitchen walls and ceiling (customer selects from company options).</li>
    </ul>
  </div>
</div>

<!-- ============================================================
     PAGE 7 — SECTION 05: Master Bathroom Remodel
     ============================================================ -->
<div class="page">
  <div class="content">
    <div class="sec-num">05</div>
    <div class="sec-title">Master Bathroom Remodel</div>

    <h3>3D Design</h3>
    <ul class="bl">
      <li>Company will provide a 3D design of the master bathroom layout prior to starting work — up to 2 revisions included.</li>
      <li>Design will confirm shower size, tub placement, vanity layout, tile patterns, and fixture locations.</li>
    </ul>

    <h3>Demo &amp; Preparation</h3>
    <ul class="bl">
      <li>Full demo of existing master bathroom — remove tile, fixtures, vanity, tub, shower enclosure, and flooring.</li>
      <li>Remove and replace any water-damaged drywall or subfloor found during demo at no additional cost up to 10 SF; beyond that priced separately.</li>
      <li>Rough-in new plumbing supply and drain lines per new layout including shower, tub, dual vanity sinks, and toilet.</li>
      <li>Rough-in new electrical — lighting circuits, exhaust fan, GFCI outlets, and heated floor circuit if specified.</li>
    </ul>

    <h3>Shower Enclosure</h3>
    <ul class="bl">
      <li>Frame and waterproof new shower enclosure using RedGard or equivalent waterproofing membrane on all shower walls and pan.</li>
      <li>Install porcelain tile on shower walls floor-to-ceiling per client selection (customer to provide tile).</li>
      <li>Install mosaic or small-format non-slip tile on shower pan to allow proper slope — customer to provide.</li>
      <li>Install new shower niche(s) per plan. Install frameless glass enclosure or shower door per allowance.</li>
      <li>Install customer-provided shower fixtures — valve, trim, hand shower, and rain head.</li>
    </ul>

    <h3>Soaking Tub</h3>
    <ul class="bl">
      <li>Set and connect freestanding or alcove soaking tub per plans (customer to provide tub and filler fixture).</li>
      <li>Install tile surround or deck as specified. Waterproof all surrounding areas per code.</li>
    </ul>

    <h3>Porcelain Tile — Floors &amp; Accent Walls</h3>
    <ul class="bl">
      <li>Install large-format porcelain tile on master bathroom floor — customer to provide tile.</li>
      <li>Install tile on any accent feature walls per design plan — customer to provide tile.</li>
      <li>Apply grout and sealant throughout all tiled surfaces.</li>
    </ul>

    <h3>Vanity, Mirrors &amp; Fixtures</h3>
    <ul class="bl">
      <li>Install customer-provided dual vanity cabinet, mirrors, and all plumbing fixtures (faucets, sinks, toilet).</li>
      <li>Install vanity lighting and all electrical fixtures per plan.</li>
      <li>Install exhaust fan vented to exterior per code.</li>
    </ul>

    <h3>Paint &amp; Finish</h3>
    <ul class="bl">
      <li>Apply moisture-resistant primer and two coats of paint on all non-tiled walls and ceiling.</li>
      <li>Install MDF baseboard and door casing to match rest of home.</li>
    </ul>
  </div>
</div>

<!-- ============================================================
     PAGE 8 — SECTION 06: Garage Conversion to ADU (400 SF)
     ============================================================ -->
<div class="page">
  <div class="content">
    <div class="sec-num">06</div>
    <div class="sec-title">Garage Conversion to ADU (400 SF)</div>

    <h3>Plans &amp; Permits</h3>
    <ul class="bl">
      <li>Architectural drawings for ADU conversion per California ADU law and local city requirements.</li>
      <li>Submit plans and obtain all required permits — building, mechanical, electrical, plumbing.</li>
      <li>Coordinate with city for any utility upgrades (separate meter, subpanel) required by code.</li>
    </ul>

    <h3>Demo &amp; Structural Modifications</h3>
    <ul class="bl">
      <li>Remove existing garage door, hardware, and opener. Frame and infill garage door opening with new wall, window, and/or entry door per plans.</li>
      <li>Remove any interior garage components, cabinetry, and finishes as needed.</li>
      <li>Patch, level, and prepare existing concrete slab floor for new ADU use.</li>
    </ul>

    <h3>Insulation, Drywall &amp; Ceilings</h3>
    <ul class="bl">
      <li>Install batt insulation in all exterior walls and ceiling per Title 24 requirements for habitable ADU space.</li>
      <li>Hang, tape, and finish drywall on all walls and ceilings to Level 4.</li>
      <li>Install recessed LED lighting and all electrical per plans.</li>
    </ul>

    <h3>Kitchenette</h3>
    <ul class="bl">
      <li>Install compact kitchenette cabinetry — upper and lower units — per ADU layout plan.</li>
      <li>Install quartz or laminate countertop per allowance (customer selects from options).</li>
      <li>Run new plumbing supply and drain for kitchenette sink. Install customer-provided sink and faucet.</li>
      <li>Install outlet circuits for refrigerator, microwave, and small appliances per code.</li>
    </ul>

    <h3>ADU Bathroom</h3>
    <ul class="bl">
      <li>Frame, plumb, and tile new ADU bathroom — shower/tub combo, toilet, and vanity per plans.</li>
      <li>Waterproof shower area and install customer-provided tile. Install customer-provided fixtures.</li>
      <li>Install exhaust fan vented to exterior per code.</li>
    </ul>

    <h3>Flooring</h3>
    <ul class="bl">
      <li>Install LVP or engineered hardwood flooring throughout ADU living areas per allowance.</li>
      <li>Install tile in ADU bathroom and kitchenette wet areas — customer to provide tile.</li>
    </ul>

    <h3>Windows, Doors &amp; Exterior</h3>
    <ul class="bl">
      <li>Install new vinyl dual-pane windows per Title 24 and plans (see allowance section).</li>
      <li>Install new exterior entry door with hardware and weather stripping.</li>
      <li>Match exterior stucco and paint finish to main house.</li>
    </ul>

    <h3>HVAC &amp; Utilities</h3>
    <ul class="bl">
      <li>Install new mini-split HVAC system for ADU per energy compliance requirements (customer to select unit from company options).</li>
      <li>Install subpanel or dedicated circuits as required by city for ADU electrical independence.</li>
    </ul>
  </div>
</div>

<!-- ============================================================
     PAGE 9 — SECTION 07: Roofing — Full Replacement
     ============================================================ -->
<div class="page">
  <div class="content">
    <div class="sec-num">07</div>
    <div class="sec-title">Roofing — Full Replacement</div>

    <h3>Scope &amp; Material</h3>
    <ul class="bl">
      <li>Full tear-off and replacement of existing roof covering on main house, new 2nd story addition, and ADU/garage roof as applicable per plans.</li>
      <li>New roof system: concrete tile or clay tile roofing per client selection from company options.</li>
    </ul>

    <h3>Tear-Off &amp; Deck Inspection</h3>
    <ul class="bl">
      <li>Remove all existing roofing material down to structural sheathing — tear-off, felt, flashings, and any existing tile or shingles.</li>
      <li>Inspect all roof decking (plywood or OSB) for damage, rot, or delamination.</li>
      <li>Replace damaged or deteriorated sheathing panels as identified — priced per sheet at cost + labor if beyond standard allowance.</li>
      <li>Re-nail all existing roof sheathing to current code where required by inspection.</li>
    </ul>

    <h3>Underlayment &amp; Waterproofing</h3>
    <ul class="bl">
      <li>Install self-adhering ice and water shield membrane in all valleys, eaves, and high-risk areas per code.</li>
      <li>Install 30 lb. or synthetic felt underlayment over remaining roof deck areas per manufacturer and code specifications.</li>
      <li>Install new drip edge flashing along all eaves and rake edges.</li>
    </ul>

    <h3>Tile Roof Installation</h3>
    <ul class="bl">
      <li>Install new tile battens (1x2 or 1x3) per tile manufacturer specifications and local code requirements.</li>
      <li>Install new concrete or clay tile roofing throughout entire roof per client-selected profile and color from company options.</li>
      <li>Install ridge caps, hip caps, and rake tiles with mortar set at all ridges, hips, and rakes.</li>
      <li>Cut and fit all tile at valleys, dormers, skylights, and roof penetrations with precision.</li>
    </ul>

    <h3>Flashings &amp; Penetrations</h3>
    <ul class="bl">
      <li>Install new galvanized or aluminum step flashing at all wall-to-roof intersections, chimneys, and parapet walls.</li>
      <li>Install new lead or copper pipe boots on all plumbing vent penetrations.</li>
      <li>Replace all roof vent flashings and ensure all penetrations are fully sealed and waterproof.</li>
      <li>Install new pre-finished aluminum gutters and downspouts as needed per plans (size and color to be confirmed with client).</li>
    </ul>

    <h3>Cool Roof Compliance</h3>
    <ul class="bl">
      <li>All new tile selections will meet California Title 24 cool roof requirements — aged solar reflectance and thermal emittance values to comply.</li>
      <li>Provide documentation of compliance for building department as required.</li>
    </ul>

    <h3>Clean-Up</h3>
    <ul class="bl">
      <li>Daily cleanup and haul-away of all roofing debris and old materials throughout the roofing phase.</li>
      <li>Final magnetic sweep of all ground areas around the home for nails and debris upon completion.</li>
    </ul>
  </div>
</div>

<!-- ============================================================
     PAGE 10 — SECTION 08: Payment Schedule
     ============================================================ -->
<div class="page">
  <div class="content dense">
    <div class="sec-num">08</div>
    <div class="sec-title full-width">Payment Schedule</div>

    <div class="pay-list">
      {pays}
    </div>

    <div class="total-line">Project Total: {e(cfg.project_total)}</div>

    <div class="allow-label">Allowances:</div>
    <ul class="allow">
      <li>Company will provide allowance for engineered hardwood flooring up to $6/sqft (material only).</li>
      <li>Company will provide allowance for LVP/SPC flooring in ADU up to $3/sqft (material only).</li>
      <li>Company will provide allowance for vinyl dual-pane windows up to $350 per window.</li>
      <li>Company will provide allowance for kitchen and bath tile installation up to $8/sqft (labor only — customer provides tile).</li>
      <li>Company will provide allowance for quartz countertop slab up to $65/sqft (prefabricated, from company options).</li>
      <li>Company will provide allowance for ADU mini-split HVAC unit up to $2,500 (equipment only).</li>
    </ul>
  </div>
</div>

<!-- ============================================================
     PAGE 11 — SECTION 09: General Notes  (FIXED — DO NOT EDIT)
     ============================================================ -->
<div class="page">
  <div class="content">
    <div class="sec-num">09</div>
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
     PAGE 12 — THANK YOU  (FIXED — DO NOT EDIT)
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
    p = argparse.ArgumentParser(description="Generate a D&C Builders full-scope proposal PDF.")
    p.add_argument("--json",    metavar="FILE",   help="Load config from a JSON file")
    p.add_argument("--client",  metavar="NAME",   help="Client full name")
    p.add_argument("--address", metavar="ADDR",   help="Client address")
    p.add_argument("--date",    metavar="DATE",   help='Proposal date, e.g. "March 2026"')
    p.add_argument("--total",   metavar="AMOUNT", help='Project total, e.g. "$541,000"')
    p.add_argument("--output",  metavar="PATH",   help="Output PDF file path")
    return p.parse_args()


def main() -> None:
    args = parse_args()
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
