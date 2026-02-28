-- DCB Proposal Generator — Supabase Schema
-- Run this in your Supabase SQL Editor to set up the database.

-- ─────────────────────────────────────────────────────────────
-- Table: client_intakes
-- Stores all new client intake submissions from the form.
-- ─────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS client_intakes (
  id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at       timestamptz NOT NULL DEFAULT now(),

  -- Client info
  first_name       text NOT NULL,
  last_name        text NOT NULL,
  email            text,
  phone            text,

  -- Property address
  street_address   text NOT NULL,
  city             text NOT NULL,
  state            text NOT NULL DEFAULT 'CA',
  zip              text NOT NULL,

  -- Proposal fields
  proposal_date    text,                    -- e.g. "March 2026" (auto-filled if blank)
  project_total    text,                    -- e.g. "$298,000"

  -- Scope of work — array of strings
  -- e.g. ["Plans & Engineering", "Kitchen Remodel", "ADU Conversion"]
  scope_items      jsonb NOT NULL DEFAULT '[]',

  -- Payment schedule — array of [description, amount] pairs
  -- e.g. [["Down payment", "$1,000"], ["Upon Start Demo", "$25,000"]]
  -- Leave empty if Claude should auto-generate from scope + total
  payments         jsonb NOT NULL DEFAULT '[]',

  -- Design section toggles (from intake form)
  -- e.g. {"design": true, "architectural": true, "engineering": true,
  --        "mood_boards": true, "space_planning": false}
  design_toggles   jsonb NOT NULL DEFAULT '{}',

  -- Additional notes from the intake form
  notes            text,

  -- Status tracking
  status           text NOT NULL DEFAULT 'pending'
                   CHECK (status IN ('pending', 'generated', 'sent')),

  -- Path to the generated PDF (filled in after generation)
  pdf_path         text
);

-- ─────────────────────────────────────────────────────────────
-- View: latest_intakes
-- Convenience view — shows most recent intakes first with
-- the full client name as a single field.
-- ─────────────────────────────────────────────────────────────

CREATE OR REPLACE VIEW latest_intakes AS
SELECT
  id,
  created_at,
  first_name || ' ' || last_name  AS client_name,
  email,
  phone,
  street_address || ', ' || city || ', ' || state || ' ' || zip AS full_address,
  proposal_date,
  project_total,
  scope_items,
  payments,
  design_toggles,
  notes,
  status,
  pdf_path
FROM client_intakes
ORDER BY created_at DESC;

-- ─────────────────────────────────────────────────────────────
-- RLS (Row Level Security)
-- Allow anonymous inserts (the form uses the anon key).
-- Restrict reads to authenticated users only.
-- ─────────────────────────────────────────────────────────────

ALTER TABLE client_intakes ENABLE ROW LEVEL SECURITY;

-- Anyone can insert (the intake form uses the public anon key)
CREATE POLICY "allow_anon_insert"
  ON client_intakes
  FOR INSERT
  TO anon
  WITH CHECK (true);

-- Only authenticated users (your team) can read/update
CREATE POLICY "allow_auth_select"
  ON client_intakes
  FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "allow_auth_update"
  ON client_intakes
  FOR UPDATE
  TO authenticated
  USING (true);
