# MEBU Analytics Platform — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a multi-page Streamlit analytics platform backed by SQLite that replaces the single-file Excel workflow with a centralized, visualizable, historically-trackable experiment database.

**Architecture:** Multi-page Streamlit app with 4 pages (Import, Dashboard, History, Settings) backed by a SQLite database. A smart name-based extractor reads all 4 existing Excel files, normalizes parameters, and writes them to SQLite. Plotly dark luxury charts mirror the Lab Results Summary sheet.

**Tech Stack:** Python, Streamlit, SQLite3 (stdlib), pandas, plotly, openpyxl. No new packages — all confirmed present in existing codebase.

**Base directory:** `D:\Claude Project\MEBU Database\`

---

## Task 1: Project Structure & Config

**Files:**
- Create: `.streamlit/config.toml`
- Create: `utils/__init__.py`
- Create: `pages/__init__.py` (empty)

**Step 1: Create `.streamlit/config.toml`**

```toml
[theme]
base = "dark"
primaryColor = "#C9A44A"
backgroundColor = "#0D1117"
secondaryBackgroundColor = "#161B22"
textColor = "#E6EDF3"
font = "sans serif"

[server]
runOnSave = true
```

**Step 2: Create `utils/__init__.py`** (empty file — makes utils a package)

**Step 3: Verify Streamlit version supports multi-page**

Run: `python -c "import streamlit; print(streamlit.__version__)"`
Expected: 1.x.x (any version ≥ 1.20 supports pages/)

---

## Task 2: Database Layer — `utils/db.py`

**Files:**
- Create: `utils/db.py`

**Step 1: Write `utils/db.py`**

```python
"""
SQLite database layer for MEBU Analytics Platform.
Two tables: experiments (run-level metadata) and measurements (daily data).
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "mebu_analytics.sqlite"


def get_conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            exp_name    TEXT NOT NULL,
            exp_type    TEXT,
            start_date  TEXT,
            file_path   TEXT,
            vr_blend    TEXT DEFAULT '[]',
            rx1_temp    REAL,
            rx2_temp    REAL,
            rx3_temp    REAL,
            notes       TEXT,
            created_at  TEXT DEFAULT (datetime('now')),
            UNIQUE(exp_name)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            exp_id      INTEGER REFERENCES experiments(id) ON DELETE CASCADE,
            day         INTEGER,
            op_date     TEXT,
            lab_date    TEXT,
            category    TEXT,
            parameter   TEXT,
            unit        TEXT,
            value       REAL,
            art_low     REAL,
            art_high    REAL,
            within_spec TEXT,
            UNIQUE(exp_id, day, parameter)
        )
    """)

    conn.commit()
    conn.close()


# ── Experiments ──────────────────────────────────────────────────────────────

def upsert_experiment(exp_name, exp_type="", start_date="", file_path="",
                      vr_blend=None, rx1_temp=None, rx2_temp=None, rx3_temp=None,
                      notes=""):
    """Insert or update experiment. Returns exp_id."""
    vr_json = json.dumps(vr_blend or [])
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO experiments (exp_name, exp_type, start_date, file_path,
                                  vr_blend, rx1_temp, rx2_temp, rx3_temp, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(exp_name) DO UPDATE SET
            exp_type   = excluded.exp_type,
            start_date = excluded.start_date,
            file_path  = excluded.file_path,
            notes      = excluded.notes
    """, (exp_name, exp_type, start_date, file_path,
          vr_json, rx1_temp, rx2_temp, rx3_temp, notes))
    conn.commit()
    exp_id = c.execute("SELECT id FROM experiments WHERE exp_name=?", (exp_name,)).fetchone()[0]
    conn.close()
    return exp_id


def update_experiment_meta(exp_id, vr_blend=None, rx1_temp=None, rx2_temp=None,
                           rx3_temp=None, notes=None):
    """Update only the editable metadata fields."""
    conn = get_conn()
    c = conn.cursor()
    if vr_blend is not None:
        c.execute("UPDATE experiments SET vr_blend=? WHERE id=?",
                  (json.dumps(vr_blend), exp_id))
    if rx1_temp is not None:
        c.execute("UPDATE experiments SET rx1_temp=? WHERE id=?", (rx1_temp, exp_id))
    if rx2_temp is not None:
        c.execute("UPDATE experiments SET rx2_temp=? WHERE id=?", (rx2_temp, exp_id))
    if rx3_temp is not None:
        c.execute("UPDATE experiments SET rx3_temp=? WHERE id=?", (rx3_temp, exp_id))
    if notes is not None:
        c.execute("UPDATE experiments SET notes=? WHERE id=?", (notes, exp_id))
    conn.commit()
    conn.close()


def get_all_experiments():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM experiments ORDER BY start_date").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_experiment(exp_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM experiments WHERE id=?", (exp_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def delete_experiment(exp_id):
    conn = get_conn()
    conn.execute("DELETE FROM experiments WHERE id=?", (exp_id,))
    conn.commit()
    conn.close()


# ── Measurements ─────────────────────────────────────────────────────────────

def bulk_insert_measurements(records):
    """Insert list of measurement dicts, ignoring duplicates."""
    if not records:
        return 0
    conn = get_conn()
    c = conn.cursor()
    inserted = 0
    for r in records:
        try:
            c.execute("""
                INSERT OR IGNORE INTO measurements
                    (exp_id, day, op_date, lab_date, category, parameter,
                     unit, value, art_low, art_high, within_spec)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (r["exp_id"], r["day"], r.get("op_date",""), r.get("lab_date",""),
                  r["category"], r["parameter"], r.get("unit",""),
                  r["value"], r.get("art_low"), r.get("art_high"),
                  r.get("within_spec","N/A")))
            inserted += c.rowcount
        except Exception:
            pass
    conn.commit()
    conn.close()
    return inserted


def get_measurements(exp_id, parameters=None):
    """Return measurements for one experiment as list of dicts."""
    conn = get_conn()
    if parameters:
        placeholders = ",".join("?" * len(parameters))
        rows = conn.execute(
            f"SELECT * FROM measurements WHERE exp_id=? AND parameter IN ({placeholders}) ORDER BY day",
            [exp_id] + list(parameters)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM measurements WHERE exp_id=? ORDER BY day",
            (exp_id,)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_multi_experiment_measurements(exp_ids, parameters=None):
    """Return measurements for multiple experiments."""
    if not exp_ids:
        return []
    conn = get_conn()
    placeholders = ",".join("?" * len(exp_ids))
    if parameters:
        pphs = ",".join("?" * len(parameters))
        rows = conn.execute(
            f"SELECT m.*, e.exp_name FROM measurements m "
            f"JOIN experiments e ON m.exp_id=e.id "
            f"WHERE m.exp_id IN ({placeholders}) AND m.parameter IN ({pphs}) "
            f"ORDER BY m.exp_id, m.day",
            list(exp_ids) + list(parameters)
        ).fetchall()
    else:
        rows = conn.execute(
            f"SELECT m.*, e.exp_name FROM measurements m "
            f"JOIN experiments e ON m.exp_id=e.id "
            f"WHERE m.exp_id IN ({placeholders}) ORDER BY m.exp_id, m.day",
            list(exp_ids)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_available_parameters(exp_id=None):
    """List all unique parameter names in DB (or for one experiment)."""
    conn = get_conn()
    if exp_id:
        rows = conn.execute(
            "SELECT DISTINCT parameter, category, unit FROM measurements WHERE exp_id=? ORDER BY category, parameter",
            (exp_id,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT DISTINCT parameter, category, unit FROM measurements ORDER BY category, parameter"
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_measurement_count(exp_id):
    conn = get_conn()
    n = conn.execute("SELECT COUNT(*) FROM measurements WHERE exp_id=?", (exp_id,)).fetchone()[0]
    conn.close()
    return n
```

**Step 2: Verify the module is importable**

Run: `python -c "import sys; sys.path.insert(0,'D:/Claude Project/MEBU Database'); from utils.db import init_db; init_db(); print('DB OK')"`
Expected: `DB OK` and file `mebu_analytics.sqlite` created.

---

## Task 3: Excel Extractor — `utils/extractor.py`

**Files:**
- Create: `utils/extractor.py`

This extractor uses **name-based row detection** (searches for parameter strings in column C) rather than hardcoded row numbers, so it works across all 4 experiment files.

```python
"""
Excel → SQLite extractor for MEBU Master Template sheets.
Detects parameter rows by name — works across all 4 experiment files.
"""
import pandas as pd
import numpy as np
import re
from pathlib import Path

# ── Parameter catalogue ───────────────────────────────────────────────────────
# Maps canonical parameter key → (search_strings, category, unit, art_low, art_high)
# search_strings: list of substrings to match (case-insensitive, any match wins)

PARAM_CATALOGUE = {
    # ── Product Distribution ─────────────────────────────────────────────────
    "560plus_wt": (["560 plus", "560plus", "560 Plus"],
                   "Product Distribution", "wt%", None, None),
    "360_500_wt": (["360-500"],
                   "Product Distribution", "wt%", None, None),
    "250_360_wt": (["250-360"],
                   "Product Distribution", "wt%", None, None),
    "160_250_wt": (["160-250"],
                   "Product Distribution", "wt%", None, None),
    "90_160_wt":  (["90-160"],
                   "Product Distribution", "wt%", None, None),
    "IBP_90_wt":  (["IBP-90"],
                   "Product Distribution", "wt%", None, None),

    # ── Metals in Product ────────────────────────────────────────────────────
    "Ni_ppm":   (["Ni, ppm"],       "Metals in Product", "ppm", None, None),
    "V_ppm":    (["V, ppm"],        "Metals in Product", "ppm", None, None),
    "Fe_ppm":   (["Fe, ppm"],       "Metals in Product", "ppm", None, None),

    # ── Impurities ───────────────────────────────────────────────────────────
    "S_wt":     (["S, wt% (ASTM D4294)", "S, wt%"],
                 "Impurities", "wt%", None, None),
    "N_wt":     (["N, wt% (ASTM D5762)", "N, wt%"],
                 "Impurities", "wt%", None, None),

    # ── Stability ────────────────────────────────────────────────────────────
    "C5_Asph":  (["C5 Asphaltene, wt%"],  "Stability", "wt%", None, None),
    "C7_Asph":  (["C7 Asphaltene, wt%"],  "Stability", "wt%", None, None),
    "MCRT":     (["MCRT, wt%"],           "Stability", "wt%", None, None),

    # ── H/C Ratio ────────────────────────────────────────────────────────────
    "HC_ratio": (["H/C Ratio, wt/wt"],    "Composition", "wt/wt", None, None),

    # ── Flow / Operating ─────────────────────────────────────────────────────
    "LHSV_actual": (["MEBU LHSV, Actual"],  "Operating", "hr-1", None, None),
    "Total_rate":  (["Total rate, g/h"],    "Operating", "g/h",  None, None),

    # ── Acceptance Reference Lines ────────────────────────────────────────────
    "560plus_ART": (["560 plus, ART, acceptance", "560plus, ART"],
                    "Reference", "wt%", None, None),
    "Ni_ART":      (["Ni, ppm, ART, Acceptance"],
                    "Reference", "ppm", None, None),
    "V_ART":       (["V, ppm, ART, Acceptance"],
                    "Reference", "ppm", None, None),
    "S_ART":       (["S, wt%, ART Acceptance", "S, wt%, ART"],
                    "Reference", "wt%", None, None),
    "N_ART":       (["N, ppm, ART, Acceptance"],
                    "Reference", "ppm", None, None),
    "C7_ART":      (["C7 Asphaltene, wt%, ART, Acceptance"],
                    "Reference", "wt%", None, None),
    "MCRT_ART":    (["MCRT, wt%, ART, Acceptance"],
                    "Reference", "wt%", None, None),
    "HC_ART":      (["H/C Ratio, wt/wt, ART"],
                    "Reference", "wt/wt", None, None),
    "LHSV_target": (["MEBU Target LHSV"],
                    "Reference", "hr-1", None, None),
}

# Conversion parameters have different row numbers per file — detected by section header
CONVERSION_PARAMS = {
    "CrkConv":    (["Cracking Conversion", "CrkConv", "Conv,560"],
                   "Conversion", "wt%", 70.0, 78.0),
    "NiConv":     (["Ni Conversion", "NiConv"],
                   "Conversion", "wt%", 88.0, 100.0),
    "VConv":      (["V Conversion", "VConv"],
                   "Conversion", "wt%", 98.0, 100.0),
    "NiV_Conv":   (["Ni+V Conversion", "NiV Conv", "NiVConv"],
                   "Conversion", "wt%", 96.0, 100.0),
    "FeConv":     (["Fe Conversion", "FeConv"],
                   "Conversion", "wt%", None, None),
    "SConv":      (["S Conversion", "SConv"],
                   "Conversion", "wt%", 80.0, 100.0),
    "NConv":      (["N Conversion", "NConv"],
                   "Conversion", "wt%", None, None),
    "MCRConv":    (["MCR Conversion", "MCRConv"],
                   "Conversion", "wt%", 70.0, 100.0),
    "Sedimentation": (["Sedimentation", "Sediment"],
                      "Sedimentation", "ppm", 0.0, 1500.0),
}


def _norm(s):
    """Normalize string for matching."""
    return str(s).strip().lower()


def _matches_any(cell_val, search_strings):
    """Return True if cell_val contains any of the search strings (case-insensitive)."""
    n = _norm(cell_val)
    for s in search_strings:
        if _norm(s) in n:
            return True
    return False


def _find_param_rows(df, catalogue):
    """
    Scan column index 2 for parameter names.
    Returns dict: key → row_index (first match, not a reference line).
    """
    found = {}
    col = df.iloc[:, 2].fillna("").astype(str)
    for key, (searches, *_) in catalogue.items():
        for i, val in col.items():
            if val.strip() == "" or "-->" in val:
                continue
            if _matches_any(val, searches):
                # Prefer exact shorter matches for primary params vs reference lines
                found[key] = i
                break
    return found


def _find_day_columns(df):
    """
    Locate the 'Day on stream' row and return list of
    {col_index, day, op_date, lab_date}.
    """
    col2 = df.iloc[:, 2].fillna("").astype(str)
    day_row_idx = None
    op_row_idx = None
    lab_row_idx = None

    for i, val in col2.items():
        v = _norm(val)
        if "day on stream" in v and day_row_idx is None:
            day_row_idx = i
        if "pilot plant operation" in v and op_row_idx is None:
            op_row_idx = i
        if "lab date" in v and "sample" in v and lab_row_idx is None:
            lab_row_idx = i

    if day_row_idx is None:
        return []

    # Data columns: find columns where day is a positive integer
    day_row = df.iloc[day_row_idx]
    op_row = df.iloc[op_row_idx] if op_row_idx is not None else pd.Series(dtype=object)
    lab_row = df.iloc[lab_row_idx] if lab_row_idx is not None else pd.Series(dtype=object)

    results = []
    for col_idx in range(3, len(day_row)):
        v = day_row.iloc[col_idx]
        try:
            day = int(float(v))
            if day < 1 or day > 60:
                continue
        except (ValueError, TypeError):
            continue

        op_d = pd.to_datetime(op_row.iloc[col_idx], errors="coerce") if col_idx < len(op_row) else pd.NaT
        lab_d = pd.to_datetime(lab_row.iloc[col_idx], errors="coerce") if col_idx < len(lab_row) else pd.NaT
        results.append({
            "col": col_idx,
            "day": day,
            "op_date": op_d.strftime("%d-%b-%y") if pd.notna(op_d) else "",
            "lab_date": lab_d.strftime("%d-%b-%y") if pd.notna(lab_d) else "",
        })

    # deduplicate by day (keep first occurrence)
    seen = set()
    unique = []
    for r in results:
        if r["day"] not in seen:
            seen.add(r["day"])
            unique.append(r)
    return sorted(unique, key=lambda x: x["day"])


def _safe_float(val):
    try:
        f = float(val)
        return f if not (f != f) else None  # NaN check
    except (ValueError, TypeError):
        return None


def extract_from_file(file_path, exp_id, exp_name=""):
    """
    Main entry point. Reads Master Template sheet and returns list of
    measurement dicts ready for db.bulk_insert_measurements().
    """
    file_path = str(file_path)
    try:
        df = pd.read_excel(file_path, sheet_name="Master Template", header=None)
    except Exception as e:
        return [], f"Could not read Master Template: {e}"

    day_cols = _find_day_columns(df)
    if not day_cols:
        return [], "Could not locate 'Day on stream' row"

    # Find rows for all known parameters
    all_catalogue = {**PARAM_CATALOGUE, **CONVERSION_PARAMS}
    param_rows = _find_param_rows(df, all_catalogue)

    records = []
    for key, row_idx in param_rows.items():
        searches, category, unit, art_low, art_high = all_catalogue[key]
        for dc in day_cols:
            col_idx = dc["col"]
            val = _safe_float(df.iloc[row_idx, col_idx])
            if val is None:
                continue
            # Skip zeros for conversion/composition (startup artefacts)
            if val == 0.0 and category in ("Conversion", "Product Distribution"):
                continue

            if art_low is not None and art_high is not None:
                within_spec = "YES" if art_low <= val <= art_high else "NO"
            else:
                within_spec = "N/A"

            records.append({
                "exp_id": exp_id,
                "day": dc["day"],
                "op_date": dc["op_date"],
                "lab_date": dc["lab_date"],
                "category": category,
                "parameter": key,
                "unit": unit,
                "value": round(val, 5),
                "art_low": art_low,
                "art_high": art_high,
                "within_spec": within_spec,
            })

    return records, None
```

**Step 2: Quick smoke test**

```python
# Run from D:\Claude Project\MEBU Database\
import sys; sys.path.insert(0, '.')
from utils.extractor import extract_from_file
records, err = extract_from_file(
    r"EXPERIMENT DATA/04_Master_MEBU Result (Repeat Acceptance Test)_Feb-Mar'26.xlsx",
    exp_id=1
)
print(f"Records: {len(records)}, Error: {err}")
if records:
    for r in records[:3]:
        print(r)
```

Expected: 50+ records, `Error: None`.

---

## Task 4: Chart Builder — `utils/charts.py`

**Files:**
- Create: `utils/charts.py`

```python
"""
Plotly chart factory for MEBU Analytics.
All charts use a consistent dark luxury theme.
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import json

# ── Colour palette ─────────────────────────────────────────────────────────
PALETTE = [
    "#C9A44A",  # gold      — primary
    "#4ECDC4",  # teal
    "#A78BFA",  # violet
    "#F97316",  # amber
    "#22D3EE",  # cyan
    "#FB7185",  # rose
    "#86EFAC",  # green
    "#FCD34D",  # yellow
]

REFERENCE_COLOR = "rgba(201,164,74,0.35)"  # gold tint for ART bands
GRID_COLOR = "rgba(255,255,255,0.06)"
PAPER_BG = "#0D1117"
PLOT_BG = "#161B22"

BASE_LAYOUT = dict(
    paper_bgcolor=PAPER_BG,
    plot_bgcolor=PLOT_BG,
    font=dict(color="#E6EDF3", family="Inter, Arial, sans-serif", size=12),
    xaxis=dict(
        gridcolor=GRID_COLOR, zeroline=False,
        title_font=dict(size=11, color="#8B949E"),
        tickfont=dict(size=10, color="#8B949E"),
    ),
    yaxis=dict(
        gridcolor=GRID_COLOR, zeroline=False,
        title_font=dict(size=11, color="#8B949E"),
        tickfont=dict(size=10, color="#8B949E"),
    ),
    legend=dict(
        bgcolor="rgba(22,27,34,0.8)",
        bordercolor="rgba(201,164,74,0.3)",
        borderwidth=1,
        font=dict(size=11),
        orientation="h",
        yanchor="bottom", y=1.02,
        xanchor="right", x=1,
    ),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="#1C2128",
        bordercolor="#C9A44A",
        font=dict(color="#E6EDF3"),
    ),
    margin=dict(l=50, r=20, t=50, b=40),
)


def _base_fig(title="", y_title="", x_title="Day on Stream"):
    fig = go.Figure()
    layout = {**BASE_LAYOUT}
    layout["title"] = dict(text=title, font=dict(size=14, color="#C9A44A"), x=0.01)
    layout["xaxis"]["title"] = x_title
    layout["yaxis"]["title"] = y_title
    fig.update_layout(**layout)
    return fig


def _add_art_band(fig, art_low, art_high, n_days=28, label="ART Acceptance"):
    """Add a shaded ART acceptance band as a filled region."""
    if art_low is None or art_high is None:
        return
    days = list(range(1, n_days + 1))
    fig.add_trace(go.Scatter(
        x=days + days[::-1],
        y=[art_high] * len(days) + [art_low] * len(days),
        fill="toself",
        fillcolor="rgba(34,197,94,0.10)",
        line=dict(color="rgba(34,197,94,0.3)", width=1, dash="dot"),
        name=label,
        hoverinfo="skip",
        showlegend=True,
    ))


def line_chart(title, y_title, series_list, art_low=None, art_high=None):
    """
    Generic line chart.
    series_list: list of {"name": str, "x": [days], "y": [values], "color": optional}
    """
    fig = _base_fig(title=title, y_title=y_title)
    max_day = max((max(s["x"]) for s in series_list if s["x"]), default=28)

    if art_low is not None and art_high is not None:
        _add_art_band(fig, art_low, art_high, n_days=max_day)

    for i, s in enumerate(series_list):
        color = s.get("color", PALETTE[i % len(PALETTE)])
        dash = s.get("dash", "solid")
        fig.add_trace(go.Scatter(
            x=s["x"], y=s["y"],
            mode="lines+markers",
            name=s["name"],
            line=dict(color=color, width=2, dash=dash),
            marker=dict(size=5, color=color),
            connectgaps=False,
        ))
    return fig


def multi_experiment_chart(title, y_title, exp_data_list, art_low=None, art_high=None):
    """
    Multi-experiment overlay chart.
    exp_data_list: list of {"exp_name": str, "x": [days], "y": [values]}
    """
    series = [
        {"name": e["exp_name"], "x": e["x"], "y": e["y"],
         "color": PALETTE[i % len(PALETTE)]}
        for i, e in enumerate(exp_data_list)
    ]
    return line_chart(title, y_title, series, art_low=art_low, art_high=art_high)


def vr_blend_donut(vr_blend):
    """
    Donut chart of VR blend composition.
    vr_blend: list of {"name": str, "pct": float}
    """
    if not vr_blend:
        return None
    labels = [v["name"] for v in vr_blend]
    values = [v["pct"] for v in vr_blend]
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.55,
        marker=dict(colors=PALETTE[:len(labels)],
                    line=dict(color=PAPER_BG, width=2)),
        textfont=dict(color="#E6EDF3", size=11),
    ))
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PAPER_BG,
        font=dict(color="#E6EDF3"),
        showlegend=True,
        legend=dict(
            bgcolor="rgba(22,27,34,0.8)",
            bordercolor="rgba(201,164,74,0.3)",
            borderwidth=1,
            font=dict(size=11),
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        annotations=[dict(
            text="VR Blend",
            x=0.5, y=0.5,
            font=dict(size=13, color="#C9A44A"),
            showarrow=False,
        )],
    )
    return fig


def build_param_series(measurements, param_key, exp_name=None):
    """Extract x,y lists from measurement records for one parameter."""
    rows = [m for m in measurements if m["parameter"] == param_key]
    rows.sort(key=lambda r: r["day"])
    x = [r["day"] for r in rows]
    y = [r["value"] for r in rows]
    art_low = rows[0]["art_low"] if rows else None
    art_high = rows[0]["art_high"] if rows else None
    return {"name": exp_name or param_key, "x": x, "y": y}, art_low, art_high
```

---

## Task 5: Main Entry Point — `main.py`

**Files:**
- Create: `main.py`

```python
"""
MEBU Analytics Platform — Main entry point.
Run with: streamlit run main.py
"""
import streamlit as st
from utils.db import init_db

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MEBU Analytics",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global luxury CSS ─────────────────────────────────────────────────────────
LUXURY_CSS = """
<style>
/* Import Inter font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1117 0%, #111827 100%) !important;
    border-right: 1px solid rgba(201,164,74,0.2) !important;
}

/* Gold header accent */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #C9A44A !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #161B22;
    border: 1px solid rgba(201,164,74,0.2);
    border-radius: 8px;
    padding: 12px 16px !important;
}
[data-testid="stMetricLabel"] { color: #8B949E !important; }
[data-testid="stMetricValue"] { color: #E6EDF3 !important; }

/* Tab styling */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid rgba(201,164,74,0.2);
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    color: #8B949E;
    font-weight: 500;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: #C9A44A !important;
    border-bottom: 2px solid #C9A44A !important;
}

/* Selectbox, multiselect */
[data-baseweb="select"] {
    background: #161B22 !important;
    border-color: rgba(201,164,74,0.3) !important;
}

/* Buttons */
[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #C9A44A, #A07830) !important;
    border: none !important;
    color: #0D1117 !important;
    font-weight: 600 !important;
}
[data-testid="baseButton-secondary"] {
    background: transparent !important;
    border: 1px solid rgba(201,164,74,0.4) !important;
    color: #C9A44A !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(201,164,74,0.15);
    border-radius: 6px;
}

/* Divider */
hr { border-color: rgba(201,164,74,0.15) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0D1117; }
::-webkit-scrollbar-thumb { background: rgba(201,164,74,0.4); border-radius: 3px; }

/* Toast / info boxes */
[data-testid="stAlert"] {
    border-radius: 6px;
    border-left: 3px solid #C9A44A;
}

/* Input fields */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background: #161B22 !important;
    border-color: rgba(201,164,74,0.3) !important;
    color: #E6EDF3 !important;
}
</style>
"""

# ── Initialise ────────────────────────────────────────────────────────────────
init_db()
st.markdown(LUXURY_CSS, unsafe_allow_html=True)

# ── Home page content ─────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 60px 20px 40px;">
    <div style="font-size:48px; margin-bottom:8px;">⚗️</div>
    <h1 style="color:#C9A44A; font-size:2.4rem; font-weight:700; margin:0;">
        MEBU Analytics Platform
    </h1>
    <p style="color:#8B949E; font-size:1.1rem; margin-top:12px;">
        Residue Hydrocracking Pilot Plant — Experiment Data Management
    </p>
    <hr style="border-color:rgba(201,164,74,0.2); margin:32px auto; width:60%;">
</div>
""", unsafe_allow_html=True)

from utils.db import get_all_experiments, get_measurement_count
experiments = get_all_experiments()
total_measurements = sum(get_measurement_count(e["id"]) for e in experiments)

col1, col2, col3 = st.columns(3)
col1.metric("Experiments Loaded", len(experiments))
col2.metric("Total Measurements", f"{total_measurements:,}")
col3.metric("Data Directory", "EXPERIMENT DATA/")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="
    background: #161B22;
    border: 1px solid rgba(201,164,74,0.2);
    border-radius: 10px;
    padding: 24px 32px;
    max-width: 700px;
    margin: 0 auto;
">
    <h3 style="color:#C9A44A; margin-top:0;">Quick Start</h3>
    <ol style="color:#8B949E; line-height:2;">
        <li><b style="color:#E6EDF3;">📥 Import</b> — Load your Excel experiment files into the database</li>
        <li><b style="color:#E6EDF3;">📊 Dashboard</b> — View charts for the current or any single experiment</li>
        <li><b style="color:#E6EDF3;">📈 History</b> — Compare multiple experiments side-by-side</li>
        <li><b style="color:#E6EDF3;">⚙️ Settings</b> — Edit VR blend, temperatures, and run notes</li>
    </ol>
</div>
""", unsafe_allow_html=True)
```

**Step 2: Launch and verify home page loads**

Run: `streamlit run "D:/Claude Project/MEBU Database/main.py"`
Expected: Browser opens showing MEBU Analytics home page with 3 metric cards.

---

## Task 6: Import Page — `pages/1_Import.py`

**Files:**
- Create: `pages/1_Import.py`

```python
"""
📥 Import — Extract data from Excel files into SQLite.
"""
import streamlit as st
import os
import glob
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.db import init_db, upsert_experiment, bulk_insert_measurements, get_all_experiments, get_measurement_count
from utils.extractor import extract_from_file

init_db()

DATA_DIR = Path(__file__).parent.parent / "EXPERIMENT DATA"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("## 📥 Import Experiment Data")
st.markdown("<hr style='border-color:rgba(201,164,74,0.2);'>", unsafe_allow_html=True)

# ── File discovery ────────────────────────────────────────────────────────────
excel_files = sorted(glob.glob(str(DATA_DIR / "*.xlsx")))
if not excel_files:
    st.error(f"No Excel files found in: {DATA_DIR}")
    st.stop()

st.markdown("### Select File to Import")
file_names = [os.path.basename(f) for f in excel_files]
selected_name = st.selectbox("Excel file:", file_names)
selected_path = os.path.join(DATA_DIR, selected_name)

# ── Experiment metadata form ──────────────────────────────────────────────────
st.markdown("### Experiment Metadata")
st.caption("This is stored once per experiment run (not per day).")

col1, col2 = st.columns(2)
with col1:
    exp_name = st.text_input("Experiment Name", value=selected_name.replace(".xlsx", ""))
    exp_type = st.selectbox("Type", ["Acceptance Test", "L&H + Sedim", "R1R2 + Repro", "Other"])
    start_date = st.text_input("Start Date (e.g. 23-Feb-26)", value="")

with col2:
    rx1_temp = st.number_input("Rx-1 Temperature (°C)", value=404.0, step=0.5)
    rx2_temp = st.number_input("Rx-2 Temperature (°C)", value=405.0, step=0.5)
    rx3_temp = st.number_input("Rx-3 Temperature (°C)", value=406.0, step=0.5)

# ── VR Blend input ────────────────────────────────────────────────────────────
st.markdown("### VR Feed Blend")
st.caption("Add up to 6 VR components. Percentages should sum to 100%.")

if "vr_rows" not in st.session_state:
    st.session_state.vr_rows = [{"name": "", "pct": 0.0}]

vr_cols = st.columns([3, 2, 1])
vr_cols[0].markdown("**VR Name**")
vr_cols[1].markdown("**% Usage (wt%)**")
vr_cols[2].markdown("**&nbsp;**", unsafe_allow_html=True)

vr_blend = []
rows_to_delete = []

for i, row in enumerate(st.session_state.vr_rows):
    c1, c2, c3 = st.columns([3, 2, 1])
    name_val = c1.text_input(f"vr_name_{i}", value=row["name"], label_visibility="collapsed",
                              placeholder=f"e.g. Basrah Heavy")
    pct_val = c2.number_input(f"vr_pct_{i}", value=float(row["pct"]),
                               min_value=0.0, max_value=100.0, step=1.0,
                               label_visibility="collapsed")
    if c3.button("✕", key=f"del_vr_{i}", help="Remove"):
        rows_to_delete.append(i)
    if name_val.strip():
        vr_blend.append({"name": name_val.strip(), "pct": pct_val})

for i in sorted(rows_to_delete, reverse=True):
    st.session_state.vr_rows.pop(i)

if len(st.session_state.vr_rows) < 6:
    if st.button("+ Add VR Component", type="secondary"):
        st.session_state.vr_rows.append({"name": "", "pct": 0.0})
        st.rerun()

total_pct = sum(v["pct"] for v in vr_blend)
if vr_blend:
    if abs(total_pct - 100.0) > 0.1:
        st.warning(f"⚠️ VR blend total = {total_pct:.1f}% (should be 100%)")
    else:
        st.success(f"✅ VR blend total = {total_pct:.1f}%")

notes = st.text_area("Notes (optional)", height=80)

# ── Import button ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Import & Extract Data", type="primary"):
    with st.spinner("Reading Excel file and extracting measurements..."):
        exp_id = upsert_experiment(
            exp_name=exp_name, exp_type=exp_type, start_date=start_date,
            file_path=selected_path, vr_blend=vr_blend,
            rx1_temp=rx1_temp, rx2_temp=rx2_temp, rx3_temp=rx3_temp,
            notes=notes
        )
        records, err = extract_from_file(selected_path, exp_id=exp_id, exp_name=exp_name)

        if err:
            st.error(f"Extraction error: {err}")
        else:
            inserted = bulk_insert_measurements(records)
            st.success(f"✅ Imported **{inserted}** new measurements ({len(records)} extracted) for **{exp_name}**")

# ── Current database status ───────────────────────────────────────────────────
st.markdown("<hr style='border-color:rgba(201,164,74,0.2);'>", unsafe_allow_html=True)
st.markdown("### Current Database")

experiments = get_all_experiments()
if experiments:
    import pandas as pd
    rows = []
    for e in experiments:
        blend = json.loads(e["vr_blend"] or "[]")
        blend_str = ", ".join(f"{v['name']} {v['pct']}%" for v in blend) if blend else "—"
        rows.append({
            "ID": e["id"],
            "Name": e["exp_name"],
            "Type": e["exp_type"] or "—",
            "Start Date": e["start_date"] or "—",
            "VR Blend": blend_str,
            "Rx1 (°C)": e["rx1_temp"] or "—",
            "Rx2 (°C)": e["rx2_temp"] or "—",
            "Rx3 (°C)": e["rx3_temp"] or "—",
            "Measurements": get_measurement_count(e["id"]),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
else:
    st.info("No experiments imported yet. Use the form above to get started.")
```

---

## Task 7: Dashboard Page — `pages/2_Dashboard.py`

**Files:**
- Create: `pages/2_Dashboard.py`

```python
"""
📊 Dashboard — Single experiment view with all Lab Results Summary charts.
"""
import streamlit as st
import json
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.db import init_db, get_all_experiments, get_measurements, get_experiment
from utils.charts import (line_chart, vr_blend_donut, build_param_series, PALETTE)

init_db()

# ── Luxury CSS (shared) ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
[data-testid="stMetric"] {
    background: #161B22; border: 1px solid rgba(201,164,74,0.2);
    border-radius: 8px; padding: 12px 16px !important;
}
[data-testid="stMetricLabel"] { color: #8B949E !important; }
[data-testid="stMetricValue"] { color: #E6EDF3 !important; }
[data-testid="stTabs"] [aria-selected="true"] { color: #C9A44A !important; border-bottom: 2px solid #C9A44A !important; }
hr { border-color: rgba(201,164,74,0.2) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("## 📊 Experiment Dashboard")
st.markdown("<hr style='border-color:rgba(201,164,74,0.2);'>", unsafe_allow_html=True)

experiments = get_all_experiments()
if not experiments:
    st.warning("No experiments loaded. Go to **📥 Import** first.")
    st.stop()

# ── Sidebar: experiment selector ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Select Experiment")
    exp_map = {e["exp_name"]: e["id"] for e in experiments}
    # Default to last (most recent)
    exp_names = [e["exp_name"] for e in experiments]
    selected_name = st.selectbox("Experiment:", exp_names, index=len(exp_names)-1)
    exp_id = exp_map[selected_name]

exp = get_experiment(exp_id)
measurements = get_measurements(exp_id)
vr_blend = json.loads(exp["vr_blend"] or "[]")

# ── Run Metadata Card ─────────────────────────────────────────────────────────
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown(f"""
    <div style="background:#161B22; border:1px solid rgba(201,164,74,0.25);
                border-radius:10px; padding:20px 24px; margin-bottom:16px;">
        <h3 style="color:#C9A44A; margin:0 0 12px;">{exp['exp_name']}</h3>
        <table style="color:#E6EDF3; border-spacing:0; width:100%;">
            <tr><td style="color:#8B949E; width:140px; padding:4px 0;">Type</td>
                <td>{exp.get('exp_type') or '—'}</td></tr>
            <tr><td style="color:#8B949E; padding:4px 0;">Start Date</td>
                <td>{exp.get('start_date') or '—'}</td></tr>
            <tr><td style="color:#8B949E; padding:4px 0;">Rx-1 Temp</td>
                <td>{f"{exp['rx1_temp']} °C" if exp.get('rx1_temp') else '—'}</td></tr>
            <tr><td style="color:#8B949E; padding:4px 0;">Rx-2 Temp</td>
                <td>{f"{exp['rx2_temp']} °C" if exp.get('rx2_temp') else '—'}</td></tr>
            <tr><td style="color:#8B949E; padding:4px 0;">Rx-3 Temp</td>
                <td>{f"{exp['rx3_temp']} °C" if exp.get('rx3_temp') else '—'}</td></tr>
            <tr><td style="color:#8B949E; padding:4px 0;">Notes</td>
                <td>{exp.get('notes') or '—'}</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # Temperature badges
    temps = []
    for rx, key in [("Rx-1", "rx1_temp"), ("Rx-2", "rx2_temp"), ("Rx-3", "rx3_temp")]:
        v = exp.get(key)
        if v:
            temps.append(f"<span style='background:#1C2128; border:1px solid rgba(201,164,74,0.3); border-radius:20px; padding:4px 14px; color:#C9A44A; font-size:13px; margin-right:8px;'>🌡 {rx}: {v} °C</span>")
    if temps:
        st.markdown("".join(temps), unsafe_allow_html=True)

with c2:
    if vr_blend:
        donut = vr_blend_donut(vr_blend)
        if donut:
            st.plotly_chart(donut, use_container_width=True)
    else:
        st.info("No VR blend set.\nEdit in ⚙️ Settings.")

# ── Measurements available ────────────────────────────────────────────────────
if not measurements:
    st.warning("No measurement data found for this experiment. Import data first.")
    st.stop()

avail_params = set(m["parameter"] for m in measurements)

def get_series(param_key, label=None):
    rows = sorted([m for m in measurements if m["parameter"] == param_key],
                  key=lambda r: r["day"])
    x = [r["day"] for r in rows]
    y = [r["value"] for r in rows]
    art_low = rows[0]["art_low"] if rows else None
    art_high = rows[0]["art_high"] if rows else None
    return {"name": label or param_key, "x": x, "y": y}, art_low, art_high

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:rgba(201,164,74,0.2);'>", unsafe_allow_html=True)

# ── Chart tabs ────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "560+ Conversion", "Metal Conversion", "Impurity Conv.",
    "MCR & Sedimentation", "Asphaltenes & MCRT",
    "Metals in Product", "S & N in Product", "Flow & LHSV", "Custom Plot"
])

# TAB 0: 560+ Conversion
with tabs[0]:
    series_list = []
    art_low = art_high = None
    for pk, lbl in [("560plus_wt", "560+ Product (wt%)"),
                     ("560plus_ART", "ART Acceptance (ref)")]:
        if pk in avail_params:
            s, al, ah = get_series(pk, lbl)
            series_list.append(s)
            if al is not None: art_low = al
            if ah is not None: art_high = ah
    if series_list:
        fig = line_chart("560+ Product — Conversion Indicator", "wt%",
                         series_list, art_low=art_low, art_high=art_high)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("560+ data not found in this experiment's measurements.")

# TAB 1: Metal Conversion
with tabs[1]:
    conv_params = [("CrkConv","Cracking Conv. (wt%)"),
                   ("NiConv","Ni Conversion (wt%)"),
                   ("VConv","V Conversion (wt%)"),
                   ("NiV_Conv","Ni+V Conversion (wt%)"),
                   ("FeConv","Fe Conversion (wt%)")]
    series_list = []
    art_low = art_high = None
    for pk, lbl in conv_params:
        if pk in avail_params:
            s, al, ah = get_series(pk, lbl)
            series_list.append(s)
    if "CrkConv" in avail_params:
        rows = [m for m in measurements if m["parameter"] == "CrkConv"]
        if rows:
            art_low, art_high = rows[0]["art_low"], rows[0]["art_high"]
    if series_list:
        fig = line_chart("Hydrocracking Conversions", "wt%",
                         series_list, art_low=art_low, art_high=art_high)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Conversion data not found.")

# TAB 2: Impurity Conversion
with tabs[2]:
    series_list = []
    for pk, lbl in [("SConv","S Conversion (wt%)"),
                     ("NConv","N Conversion (wt%)")]:
        if pk in avail_params:
            s, _, _ = get_series(pk, lbl)
            series_list.append(s)
    if series_list:
        art_low = art_high = None
        if "SConv" in avail_params:
            rows = [m for m in measurements if m["parameter"] == "SConv"]
            if rows: art_low, art_high = rows[0]["art_low"], rows[0]["art_high"]
        fig = line_chart("Impurity Removal — S & N Conversion", "wt%",
                         series_list, art_low=art_low, art_high=art_high)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("S/N conversion data not found.")

# TAB 3: MCR Conv & Sedimentation
with tabs[3]:
    col_a, col_b = st.columns(2)
    with col_a:
        if "MCRConv" in avail_params:
            s, al, ah = get_series("MCRConv", "MCR Conversion (wt%)")
            fig = line_chart("MCR Conversion", "wt%", [s], art_low=al, art_high=ah)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("MCRConv not found.")
    with col_b:
        if "Sedimentation" in avail_params:
            s, al, ah = get_series("Sedimentation", "Sedimentation (ppm)")
            fig = line_chart("Sedimentation", "ppm", [s], art_low=al, art_high=ah)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sedimentation not found.")

# TAB 4: Asphaltenes & MCRT
with tabs[4]:
    series_list = []
    for pk, lbl in [("C5_Asph","C5 Asphaltene (wt%)"),
                     ("C7_Asph","C7 Asphaltene (wt%)"),
                     ("MCRT","MCRT (wt%)"),
                     ("C7_ART","C7 Asph ART Acceptance (ref)")]:
        if pk in avail_params:
            s, _, _ = get_series(pk, lbl)
            series_list.append(s)
    if series_list:
        fig = line_chart("Stability — Asphaltenes & MCRT", "wt%", series_list)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Asphaltene/MCRT data not found.")

# TAB 5: Metals in Product
with tabs[5]:
    col_a, col_b = st.columns(2)
    with col_a:
        series_list = []
        for pk, lbl in [("Ni_ppm","Ni in Product (ppm)"),
                         ("Ni_ART","Ni ART Acceptance (ref)")]:
            if pk in avail_params:
                s, _, _ = get_series(pk, lbl)
                series_list.append(s)
        if series_list:
            fig = line_chart("Nickel Removal", "ppm", series_list)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Ni data not found.")

    with col_b:
        series_list = []
        for pk, lbl in [("V_ppm","V in Product (ppm)"),
                         ("V_ART","V ART Acceptance (ref)")]:
            if pk in avail_params:
                s, _, _ = get_series(pk, lbl)
                series_list.append(s)
        if series_list:
            fig = line_chart("Vanadium Removal", "ppm", series_list)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("V data not found.")

# TAB 6: S & N in product
with tabs[6]:
    col_a, col_b = st.columns(2)
    with col_a:
        series_list = []
        for pk, lbl in [("S_wt","S in Product (wt%)"),
                         ("S_ART","S ART Acceptance (ref)")]:
            if pk in avail_params:
                s, _, _ = get_series(pk, lbl)
                series_list.append(s)
        if series_list:
            fig = line_chart("Sulfur in Product", "wt%", series_list)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("S data not found.")
    with col_b:
        series_list = []
        for pk, lbl in [("N_wt","N in Product (wt%)"),
                         ("N_ART","N ART Acceptance (ref)")]:
            if pk in avail_params:
                s, _, _ = get_series(pk, lbl)
                series_list.append(s)
        if series_list:
            fig = line_chart("Nitrogen in Product", "wt%", series_list)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("N data not found.")

# TAB 7: Flow & LHSV
with tabs[7]:
    col_a, col_b = st.columns(2)
    with col_a:
        if "LHSV_actual" in avail_params:
            series_list = []
            for pk, lbl in [("LHSV_actual","LHSV Actual (hr⁻¹)"),
                             ("LHSV_target","LHSV Target (hr⁻¹)")]:
                if pk in avail_params:
                    s, _, _ = get_series(pk, lbl)
                    series_list.append(s)
            fig = line_chart("LHSV — Space Velocity", "hr⁻¹", series_list)
            st.plotly_chart(fig, use_container_width=True)
    with col_b:
        if "Total_rate" in avail_params:
            s, _, _ = get_series("Total_rate", "Total Feed Rate (g/h)")
            fig = line_chart("Total Feed Rate", "g/h", [s])
            st.plotly_chart(fig, use_container_width=True)

# TAB 8: Custom plot
with tabs[8]:
    all_params = sorted(avail_params)
    selected_params = st.multiselect("Select parameters to plot:", all_params,
                                      default=all_params[:3] if len(all_params) >= 3 else all_params)
    if selected_params:
        series_list = []
        for pk in selected_params:
            s, _, _ = get_series(pk)
            series_list.append(s)
        fig = line_chart("Custom Parameter Selection", "Value", series_list)
        st.plotly_chart(fig, use_container_width=True)

# ── Raw data expander ─────────────────────────────────────────────────────────
with st.expander("📋 Raw Measurement Data"):
    df = pd.DataFrame(measurements)
    if not df.empty:
        st.dataframe(df[["day","op_date","lab_date","category","parameter","unit","value","within_spec"]],
                     use_container_width=True, hide_index=True)
```

---

## Task 8: History Page — `pages/3_History.py`

**Files:**
- Create: `pages/3_History.py`

```python
"""
📈 History — Cross-experiment comparison with overlaid charts.
"""
import streamlit as st
import json
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.db import init_db, get_all_experiments, get_multi_experiment_measurements
from utils.charts import multi_experiment_chart, PALETTE
import plotly.graph_objects as go

init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
[data-testid="stTabs"] [aria-selected="true"] { color: #C9A44A !important; border-bottom: 2px solid #C9A44A !important; }
hr { border-color: rgba(201,164,74,0.2) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("## 📈 Experiment History — Cross-Run Comparison")
st.markdown("<hr style='border-color:rgba(201,164,74,0.2);'>", unsafe_allow_html=True)

experiments = get_all_experiments()
if len(experiments) < 1:
    st.warning("No experiments loaded. Go to **📥 Import** first.")
    st.stop()

# ── Sidebar: multi-select experiments ────────────────────────────────────────
with st.sidebar:
    st.markdown("### Select Experiments to Compare")
    exp_options = {e["exp_name"]: e["id"] for e in experiments}
    selected_names = st.multiselect(
        "Experiments:", list(exp_options.keys()),
        default=list(exp_options.keys())[:min(2, len(exp_options))]
    )

if not selected_names:
    st.info("Select at least one experiment from the sidebar.")
    st.stop()

selected_ids = [exp_options[n] for n in selected_names]
all_measurements = get_multi_experiment_measurements(selected_ids)

# ── Legend cards ──────────────────────────────────────────────────────────────
cols = st.columns(len(selected_names))
for i, name in enumerate(selected_names):
    exp_meta = next(e for e in experiments if e["exp_name"] == name)
    blend = json.loads(exp_meta.get("vr_blend") or "[]")
    blend_str = ", ".join(f"{v['name']} {v['pct']}%" for v in blend) or "—"
    with cols[i]:
        color = PALETTE[i % len(PALETTE)]
        st.markdown(f"""
        <div style="background:#161B22; border:1px solid {color}40;
                    border-left:3px solid {color}; border-radius:8px; padding:14px;">
            <div style="font-size:11px; color:#8B949E; margin-bottom:4px;">
                {chr(9632)} RUN {i+1}</div>
            <div style="color:#E6EDF3; font-weight:600; font-size:13px;">{name[:40]}</div>
            <div style="color:#8B949E; font-size:11px; margin-top:6px;">
                Start: {exp_meta.get('start_date') or '—'}</div>
            <div style="color:#8B949E; font-size:11px;">
                VR: {blend_str[:50]}</div>
            <div style="color:#8B949E; font-size:11px;">
                Rx1: {exp_meta.get('rx1_temp') or '—'}°C
                Rx2: {exp_meta.get('rx2_temp') or '—'}°C
                Rx3: {exp_meta.get('rx3_temp') or '—'}°C</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

def overlay_chart(title, y_title, param_key, art_low=None, art_high=None):
    exp_data = []
    for exp_id, exp_name in zip(selected_ids, selected_names):
        rows = sorted([m for m in all_measurements
                       if m["exp_id"] == exp_id and m["parameter"] == param_key],
                      key=lambda r: r["day"])
        if rows:
            exp_data.append({
                "exp_name": exp_name,
                "x": [r["day"] for r in rows],
                "y": [r["value"] for r in rows],
            })
            if art_low is None and rows[0]["art_low"] is not None:
                art_low = rows[0]["art_low"]
            if art_high is None and rows[0]["art_high"] is not None:
                art_high = rows[0]["art_high"]
    if exp_data:
        fig = multi_experiment_chart(title, y_title, exp_data,
                                      art_low=art_low, art_high=art_high)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"No data for `{param_key}` in selected experiments.")

# ── Comparison tabs ────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Cracking Conv.", "Metal Conv.", "Impurity Conv.",
    "MCR & Sedim.", "Asphaltenes", "Metals in Product", "S & N"
])

with tabs[0]:
    col1, col2 = st.columns(2)
    with col1: overlay_chart("Cracking Conversion", "wt%", "CrkConv", 70.0, 78.0)
    with col2: overlay_chart("560+ Product", "wt%", "560plus_wt")

with tabs[1]:
    col1, col2 = st.columns(2)
    with col1: overlay_chart("Ni Conversion", "wt%", "NiConv", 88.0, 100.0)
    with col2: overlay_chart("V Conversion", "wt%", "VConv", 98.0, 100.0)

with tabs[2]:
    col1, col2 = st.columns(2)
    with col1: overlay_chart("S Conversion", "wt%", "SConv", 80.0, 100.0)
    with col2: overlay_chart("N Conversion", "wt%", "NConv")

with tabs[3]:
    col1, col2 = st.columns(2)
    with col1: overlay_chart("MCR Conversion", "wt%", "MCRConv", 70.0, 100.0)
    with col2: overlay_chart("Sedimentation", "ppm", "Sedimentation", 0.0, 1500.0)

with tabs[4]:
    col1, col2 = st.columns(2)
    with col1: overlay_chart("C7 Asphaltene", "wt%", "C7_Asph")
    with col2: overlay_chart("C5 Asphaltene", "wt%", "C5_Asph")

with tabs[5]:
    col1, col2 = st.columns(2)
    with col1: overlay_chart("Ni in Product", "ppm", "Ni_ppm")
    with col2: overlay_chart("V in Product", "ppm", "V_ppm")

with tabs[6]:
    col1, col2 = st.columns(2)
    with col1: overlay_chart("S in Product", "wt%", "S_wt")
    with col2: overlay_chart("N in Product", "wt%", "N_wt")
```

---

## Task 9: Settings Page — `pages/4_Settings.py`

**Files:**
- Create: `pages/4_Settings.py`

```python
"""
⚙️ Settings — Edit experiment metadata (VR blend, temperatures, notes).
"""
import streamlit as st
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.db import init_db, get_all_experiments, update_experiment_meta, delete_experiment, get_measurement_count

init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
hr { border-color: rgba(201,164,74,0.2) !important; }
[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #C9A44A, #A07830) !important;
    color: #0D1117 !important; font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## ⚙️ Settings — Experiment Metadata")
st.markdown("<hr style='border-color:rgba(201,164,74,0.2);'>", unsafe_allow_html=True)

experiments = get_all_experiments()
if not experiments:
    st.info("No experiments loaded yet. Go to **📥 Import** first.")
    st.stop()

exp_map = {e["exp_name"]: e for e in experiments}
selected_name = st.selectbox("Select experiment to edit:", list(exp_map.keys()))
exp = exp_map[selected_name]
exp_id = exp["id"]

st.markdown(f"**Measurements in DB:** {get_measurement_count(exp_id)}")
st.markdown("<br>", unsafe_allow_html=True)

# ── VR Blend editor ───────────────────────────────────────────────────────────
st.markdown("### VR Feed Blend")
current_blend = json.loads(exp.get("vr_blend") or "[]")

session_key = f"vr_rows_{exp_id}"
if session_key not in st.session_state:
    st.session_state[session_key] = current_blend if current_blend else [{"name": "", "pct": 0.0}]

vr_cols = st.columns([3, 2, 1])
vr_cols[0].markdown("**VR Name**")
vr_cols[1].markdown("**% Usage (wt%)**")

vr_blend_new = []
rows_to_del = []
for i, row in enumerate(st.session_state[session_key]):
    c1, c2, c3 = st.columns([3, 2, 1])
    name_v = c1.text_input(f"s_vr_n_{exp_id}_{i}", value=row.get("name",""),
                            label_visibility="collapsed", placeholder="VR Name")
    pct_v = c2.number_input(f"s_vr_p_{exp_id}_{i}", value=float(row.get("pct",0)),
                             min_value=0.0, max_value=100.0, step=1.0,
                             label_visibility="collapsed")
    if c3.button("✕", key=f"s_del_{exp_id}_{i}"):
        rows_to_del.append(i)
    if name_v.strip():
        vr_blend_new.append({"name": name_v.strip(), "pct": pct_v})

for i in sorted(rows_to_del, reverse=True):
    st.session_state[session_key].pop(i)

if len(st.session_state[session_key]) < 6:
    if st.button("+ Add VR Component", key=f"add_vr_{exp_id}", type="secondary"):
        st.session_state[session_key].append({"name": "", "pct": 0.0})
        st.rerun()

total_pct = sum(v["pct"] for v in vr_blend_new)
if vr_blend_new:
    msg = f"Total: {total_pct:.1f}%"
    if abs(total_pct - 100.0) < 0.1:
        st.success(f"✅ {msg}")
    else:
        st.warning(f"⚠️ {msg} (should be 100%)")

# ── Temperature & Notes editor ────────────────────────────────────────────────
st.markdown("### Reactor Temperatures & Notes")
col1, col2, col3 = st.columns(3)
rx1 = col1.number_input("Rx-1 (°C)", value=float(exp.get("rx1_temp") or 404), step=0.5, key=f"rx1_{exp_id}")
rx2 = col2.number_input("Rx-2 (°C)", value=float(exp.get("rx2_temp") or 405), step=0.5, key=f"rx2_{exp_id}")
rx3 = col3.number_input("Rx-3 (°C)", value=float(exp.get("rx3_temp") or 406), step=0.5, key=f"rx3_{exp_id}")
notes = st.text_area("Notes", value=exp.get("notes") or "", height=80, key=f"notes_{exp_id}")

if st.button("💾 Save Changes", type="primary", key=f"save_{exp_id}"):
    update_experiment_meta(
        exp_id,
        vr_blend=vr_blend_new,
        rx1_temp=rx1, rx2_temp=rx2, rx3_temp=rx3,
        notes=notes
    )
    st.success("✅ Saved successfully.")
    st.rerun()

# ── Danger zone ────────────────────────────────────────────────────────────────
st.markdown("<br><hr style='border-color:rgba(201,164,74,0.2);'>", unsafe_allow_html=True)
st.markdown("### ⚠️ Danger Zone")
with st.expander("Delete this experiment"):
    st.warning(f"This will permanently delete **{selected_name}** and all its {get_measurement_count(exp_id)} measurements.")
    confirm = st.text_input("Type the experiment name to confirm deletion:")
    if st.button("🗑️ Delete Permanently", type="primary", key=f"del_{exp_id}"):
        if confirm.strip() == selected_name.strip():
            delete_experiment(exp_id)
            st.success("Deleted.")
            st.rerun()
        else:
            st.error("Name does not match. Deletion cancelled.")
```

---

## Task 10: Final Verification

**Step 1: Run the app**

```bash
cd "D:/Claude Project/MEBU Database"
streamlit run main.py
```

**Step 2: Import all 4 experiment files via the UI**

Navigate to 📥 Import and import each file one by one:
- `01_Master_MEBU Acceptance Test(18-24Dec'24)...xlsx`
- `02_Master_MEBU Result LnH Sedim...xlsx`
- `03_Master_MEBU Result R1R2 with Repro...xlsx`
- `04_Master_MEBU Result (Repeat Acceptance Test)_Feb-Mar'26.xlsx`

**Step 3: Verify Dashboard charts load**

Navigate to 📊 Dashboard, select each experiment, confirm charts render.

**Step 4: Verify History comparison works**

Navigate to 📈 History, select 2+ experiments, confirm overlay charts show multiple traces.

**Step 5: Edit VR blend in Settings**

Navigate to ⚙️ Settings, edit VR blend for Experiment 4, save, verify it shows in the Dashboard donut chart.

---

## Dependencies Checklist

All packages are already confirmed in the existing project:
- `streamlit` (app.py uses it)
- `pandas` (all scripts use it)
- `plotly` (app.py uses it)
- `openpyxl` (read_chart.py uses it)
- `sqlite3` (stdlib — no install needed)
