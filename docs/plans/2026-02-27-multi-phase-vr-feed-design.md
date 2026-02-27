# Multi-Phase VR Feed Design

## Problem

Currently each experiment has a single VR blend and one set of reactor temperatures. In reality, experiments switch between multiple VR feeds and temperatures across different day ranges (e.g., Day 1–4 uses ABQ3358 at 404°C, Day 5–11 uses ABQ3400 at 410°C).

## Architecture

Two-level data model:
1. **VR Feed Library** — reusable named blends (e.g., ABQ3358 = Basrah Heavy 55% + Arab Medium 10% + Arab Light 35%)
2. **Phases** — per-experiment day ranges, each linked to a VR feed and its own temperatures

### New Tables

```sql
CREATE TABLE vr_feeds (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    feed_name  TEXT NOT NULL UNIQUE,
    composition TEXT DEFAULT '[]'  -- JSON: [{"name":"Basrah Heavy","pct":55}, ...]
);

CREATE TABLE phases (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    exp_id     INTEGER REFERENCES experiments(id) ON DELETE CASCADE,
    phase_name TEXT DEFAULT '',
    from_day   INTEGER NOT NULL,
    to_day     INTEGER NOT NULL,
    feed_id    INTEGER REFERENCES vr_feeds(id),
    rx1_temp   REAL,
    rx2_temp   REAL,
    rx3_temp   REAL
);
```

The old `experiments.vr_blend`, `rx1_temp`, `rx2_temp`, `rx3_temp` columns remain for backward compatibility but are no longer used by the UI. A one-time migration converts existing data into phases.

## UI Changes

### Settings Page (`pages/5_Settings.py`)
- Replace the VR Blend editor + Temperature section with a **Phase Timeline Editor**
- Each phase row: Phase Name, From Day, To Day, VR Feed (dropdown from library), Rx-1, Rx-2, Rx-3 temps
- Add/Delete phase buttons
- Below: a **VR Feed Library** manager (expandable section) to create/edit named feed recipes
- Phase reference table showing the timeline visually

### Dashboard (`pages/2_Dashboard.py`)
- Replace the single VR blend donut with a **Phase Summary Table** showing all phases
- Add colored vertical background bands on all charts showing phase boundaries
- Each band labeled with the VR Feed name

### Product Results (`pages/4_Product_Results.py`)
- Same colored background bands on all charts

### Charts (`utils/charts.py`)
- New `add_phase_bands(fig, phases)` function to add vertical `vrect` shapes with labels

## Migration Strategy

On `init_db()`, if the `phases` table doesn't exist:
1. Create the new tables
2. For each experiment with existing `vr_blend` data, create a `vr_feeds` entry and a single phase spanning all days

## Data Flow

```
Settings → User creates VR Feeds in library
Settings → User adds phases to experiment (from_day, to_day, feed, temps)
Dashboard → Queries phases for the selected experiment
Dashboard → Passes phases to chart functions for background bands
Dashboard → Renders phase reference table
```
