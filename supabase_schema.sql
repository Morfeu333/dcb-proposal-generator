-- DCB Proposal Generator — Supabase Schema
-- Run this in your Supabase SQL Editor to set up the database.
-- Reflects all fields from the Base44 intake form.

CREATE TABLE IF NOT EXISTS client_intakes (
  id                    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at            timestamptz NOT NULL DEFAULT now(),

  -- ── Client info ──────────────────────────────────────────
  first_name            text NOT NULL,
  last_name             text NOT NULL,
  email                 text,
  phone                 text,

  -- ── Property address ─────────────────────────────────────
  street_address        text NOT NULL,
  city                  text NOT NULL,
  state                 text NOT NULL DEFAULT 'CA',
  zip                   text NOT NULL,

  -- ── Proposal fields ──────────────────────────────────────
  proposal_date         text,         -- e.g. "March 2026" (auto if blank)
  project_total         text,         -- e.g. "$541,000"

  -- ── Scope of work ────────────────────────────────────────
  -- Array of strings e.g. ["Plans & Engineering", "Kitchen Remodel"]
  scope_items           jsonb NOT NULL DEFAULT '[]',

  -- ── Payment schedule ─────────────────────────────────────
  -- Array of [description, amount] pairs. Empty = Claude auto-generates.
  payments              jsonb NOT NULL DEFAULT '[]',

  -- ── Design section toggles ───────────────────────────────
  -- {"design": true, "architectural": true, "engineering": true,
  --  "mood_boards": true, "space_planning": false}
  design_toggles        jsonb NOT NULL DEFAULT '{}',

  -- ── Construction section toggles (20 items) ──────────────
  -- {"site_prep": true, "foundation": true, "framing": true,
  --  "elec_rough": true, "elec_finish": true, "plumb_rough": true,
  --  "plumb_finish": true, "roofing": true, "insulation": true,
  --  "drywall": true, "exterior": true, "siding": true,
  --  "windows": true, "flooring": true, "interior_doors": true,
  --  "cabinetry": true, "bathroom": true, "hvac": true,
  --  "plans": true, "wall_removal": false}
  construction_toggles  jsonb NOT NULL DEFAULT '{}',

  -- ── Materials (from Materials tab) ───────────────────────
  -- {"flooring": "Engineered Hardwood", "countertop": "Quartz (Prefab)",
  --  "cabinets": "Custom Shaker", "exterior": "Stucco (Santa Barbara)",
  --  "roofing": "Concrete Tile", "windows": "Vinyl Dual-Pane"}
  materials             jsonb NOT NULL DEFAULT '{}',

  -- ── New Construction — Main Details ──────────────────────
  project_type          text,         -- New Build, Fire Rebuild, ADU, 2nd Story, etc.
  stories               text,         -- "1 Story", "2nd Story", "Split Level"
  area_sf               text,         -- Approx area in sq ft
  bedroom_count         text,
  bathroom_count        text,
  hvac_type             text,         -- Central, Mini-Split, None
  construction_notes    text,         -- Notes from Construction section
  nc_notes              text,         -- Notes from New Construction Main Details tab

  -- ── Additional Details tab ───────────────────────────────
  special_requirements  text,
  design_preferences    text,
  desired_start_date    text,
  referred_by           text,

  -- ── Additional Notes section ──────────────────────────────
  additional_notes      text,

  -- ── Status tracking ──────────────────────────────────────
  status                text NOT NULL DEFAULT 'pending'
                        CHECK (status IN ('pending', 'generated', 'sent')),
  pdf_path              text          -- filled in after generation
);

-- ─────────────────────────────────────────────────────────────
-- View: latest_intakes (convenience — newest first, full address)
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW latest_intakes AS
SELECT
  id,
  created_at,
  first_name || ' & ' || last_name                                    AS client_name,
  email,
  phone,
  street_address || ', ' || city || ', ' || state || ' ' || zip       AS full_address,
  proposal_date,
  project_total,
  scope_items,
  payments,
  design_toggles,
  construction_toggles,
  materials,
  project_type,
  stories,
  area_sf,
  bedroom_count,
  bathroom_count,
  hvac_type,
  construction_notes,
  nc_notes,
  special_requirements,
  design_preferences,
  desired_start_date,
  referred_by,
  additional_notes,
  status,
  pdf_path
FROM client_intakes
ORDER BY created_at DESC;

-- ─────────────────────────────────────────────────────────────
-- RLS — anon insert (form), authenticated read/update (team)
-- ─────────────────────────────────────────────────────────────
ALTER TABLE client_intakes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "allow_anon_insert"
  ON client_intakes FOR INSERT TO anon WITH CHECK (true);

CREATE POLICY "allow_auth_select"
  ON client_intakes FOR SELECT TO authenticated USING (true);

CREATE POLICY "allow_auth_update"
  ON client_intakes FOR UPDATE TO authenticated USING (true);
