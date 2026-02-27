"""
MEBU Analytics Platform — Main entry point.
Run with: streamlit run main.py
"""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from utils.db import init_db, get_all_experiments, get_measurement_count
from utils.styles import inject_css, page_header

st.set_page_config(
    page_title="MEBU Analytics",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()
inject_css()

# ── Home page ─────────────────────────────────────────────────────────────────
st.markdown(page_header(
    "MEBU Analytics Platform",
    subtitle="Residue Hydrocracking Pilot Plant — Experiment Data Management",
), unsafe_allow_html=True)

experiments = get_all_experiments()
total_measurements = sum(get_measurement_count(e["id"]) for e in experiments)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Experiments Loaded", len(experiments))
col2.metric("Total Measurements", f"{total_measurements:,}")
col3.metric("Database", "SQLite")
col4.metric("Platform Version", "v1.1")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="font-family:var(--font-display);font-size:0.75rem;font-weight:700;
  letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:16px;">
  ◈ QUICK START GUIDE
</div>
""", unsafe_allow_html=True)

row1_c1, row1_c2 = st.columns(2)
with row1_c1:
    st.markdown("""
    <div style="background:var(--surface);border:1px solid var(--border);border-left:2px solid var(--gold);
      border-radius:var(--radius);padding:20px;display:flex;align-items:flex-start;gap:16px;height:120px;">
      <span style="font-family:var(--font-mono);font-size:0.75rem;color:var(--gold);
        background:var(--gold-dim);border:1px solid var(--gold-border);
        border-radius:2px;padding:3px 8px;min-width:28px;text-align:center;margin-top:2px;">01</span>
      <div>
        <div style="font-family:var(--font-display);font-weight:600;font-size:1rem;
          letter-spacing:1px;color:var(--text);text-transform:uppercase;">Import</div>
        <div style="color:var(--text-2);font-size:0.85rem;margin-top:6px;line-height:1.5;font-family:var(--font-ui);">
          Load Excel experiment files into the DB. Set VR blend and temperatures.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with row1_c2:
    st.markdown("""
    <div style="background:var(--surface);border:1px solid var(--border);border-left:2px solid var(--gold-bright);
      border-radius:var(--radius);padding:20px;display:flex;align-items:flex-start;gap:16px;height:120px;">
      <span style="font-family:var(--font-mono);font-size:0.75rem;color:var(--gold);
        background:var(--gold-dim);border:1px solid var(--gold-border);
        border-radius:2px;padding:3px 8px;min-width:28px;text-align:center;margin-top:2px;">02</span>
      <div>
        <div style="font-family:var(--font-display);font-weight:600;font-size:1rem;
          letter-spacing:1px;color:var(--text);text-transform:uppercase;">Dashboard</div>
        <div style="color:var(--text-2);font-size:0.85rem;margin-top:6px;line-height:1.5;font-family:var(--font-ui);">
          View all high-density data charts for a single experiment instantly.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
row2_c1, row2_c2 = st.columns(2)

with row2_c1:
    st.markdown("""
    <div style="background:var(--surface);border:1px solid var(--border);border-left:2px solid var(--text-3);
      border-radius:var(--radius);padding:20px;display:flex;align-items:flex-start;gap:16px;height:120px;">
      <span style="font-family:var(--font-mono);font-size:0.75rem;color:var(--text-2);
        background:var(--surface-3);border:1px solid var(--border);
        border-radius:2px;padding:3px 8px;min-width:28px;text-align:center;margin-top:2px;">03</span>
      <div>
        <div style="font-family:var(--font-display);font-weight:600;font-size:1rem;
          letter-spacing:1px;color:var(--text);text-transform:uppercase;">History</div>
        <div style="color:var(--text-2);font-size:0.85rem;margin-top:6px;line-height:1.5;font-family:var(--font-ui);">
          Compare multiple experiments side-by-side with overlaid charts.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with row2_c2:
    st.markdown("""
    <div style="background:var(--surface);border:1px solid var(--border);border-left:2px solid var(--text-3);
      border-radius:var(--radius);padding:20px;display:flex;align-items:flex-start;gap:16px;height:120px;">
      <span style="font-family:var(--font-mono);font-size:0.75rem;color:var(--text-2);
        background:var(--surface-3);border:1px solid var(--border);
        border-radius:2px;padding:3px 8px;min-width:28px;text-align:center;margin-top:2px;">04</span>
      <div>
        <div style="font-family:var(--font-display);font-weight:600;font-size:1rem;
          letter-spacing:1px;color:var(--text);text-transform:uppercase;">Settings</div>
        <div style="color:var(--text-2);font-size:0.85rem;margin-top:6px;line-height:1.5;font-family:var(--font-ui);">
          Edit VR blend composition, temperatures, and database records.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

if experiments:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Loaded Experiments")
    import pandas as pd
    rows = []
    for e in experiments:
        blend = json.loads(e.get("vr_blend") or "[]")
        blend_str = " / ".join(f"{v['name']} {v['pct']}%" for v in blend) if blend else "—"
        rows.append({
            "Name": e["exp_name"],
            "Type": e.get("exp_type") or "—",
            "Start": e.get("start_date") or "—",
            "VR Blend": blend_str,
            "Rx1 °C": e.get("rx1_temp") or "—",
            "Rx2 °C": e.get("rx2_temp") or "—",
            "Rx3 °C": e.get("rx3_temp") or "—",
            "Measurements": get_measurement_count(e["id"]),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
