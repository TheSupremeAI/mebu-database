"""
MEBU Analytics — Import Page
Load Excel experiment files into SQLite, configure metadata and VR blend.
"""
import streamlit as st
import os
import glob
import json
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.db import init_db, upsert_experiment, bulk_insert_measurements, get_all_experiments, get_measurement_count
from utils.extractor import extract_from_file
from utils.styles import inject_css, page_header, glass_card, section_label

init_db()
inject_css()

st.markdown("""
<style>
[data-testid="stFileUploader"] {
  border: 1px solid var(--gold-border) !important;
  border-radius: var(--radius) !important;
  background: var(--surface) !important;
}
label[data-testid="stWidgetLabel"] > div > p {
  font-family: var(--font-ui) !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  color: var(--text-2) !important;
}
</style>
""", unsafe_allow_html=True)

DATA_DIR = Path(__file__).parent.parent / "EXPERIMENT DATA"

st.markdown(page_header(
    "Import Experiment Data",
    subtitle="Load an Excel experiment file into the database and configure its metadata.",
    icon="📥",
), unsafe_allow_html=True)

# ── File discovery ────────────────────────────────────────────────────────────
excel_files = sorted(glob.glob(str(DATA_DIR / "*.xlsx")))
if not excel_files:
    st.error(f"No Excel files found in: {DATA_DIR}")
    st.stop()

file_names = [os.path.basename(f) for f in excel_files]

col_sel, col_info = st.columns([3, 2])
with col_sel:
    st.markdown(section_label("01 — Select Excel File"), unsafe_allow_html=True)
    selected_name = st.selectbox("Excel file:", file_names, label_visibility="collapsed")
    selected_path = str(DATA_DIR / selected_name)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(section_label("02 — Experiment Metadata"), unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        exp_name = st.text_input("Experiment Name", value=selected_name.replace(".xlsx", ""))
        exp_type = st.selectbox("Experiment Type", ["Acceptance Test", "L&H + Sedim", "R1R2 + Repro", "Other"])
        start_date = st.text_input("Start Date", placeholder="e.g. 23-Feb-26")
    with c2:
        rx1_temp = st.number_input("Rx-1 Temperature (°C)", value=404.0, step=0.5, format="%.1f")
        rx2_temp = st.number_input("Rx-2 Temperature (°C)", value=405.0, step=0.5, format="%.1f")
        rx3_temp = st.number_input("Rx-3 Temperature (°C)", value=406.0, step=0.5, format="%.1f")

with col_info:
    st.markdown("&nbsp;", unsafe_allow_html=True)
    st.markdown(glass_card("""
      <div style="font-family:var(--font-display);font-size:0.7rem;font-weight:700;
        letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:16px;">
        ◈ HOW TO IMPORT
      </div>
      <ol style="color:var(--text-2);font-size:0.86rem;line-height:2.1;margin:0;
        padding-left:20px;font-family:var(--font-body);">
        <li>Select the Excel file from the list</li>
        <li>Set the experiment name and type</li>
        <li>Enter the VR feed blend below</li>
        <li>Set reactor temperatures</li>
        <li>Click <b style="color:var(--gold);font-family:var(--font-display);
          letter-spacing:1px;">IMPORT &amp; EXTRACT DATA</b></li>
      </ol>
      <div style="color:var(--text-3);font-size:0.78rem;margin-top:16px;
        font-family:var(--font-mono);border-top:1px solid var(--border);padding-top:12px;">
        ↻ Re-importing the same experiment will not duplicate data.
      </div>
    """), unsafe_allow_html=True)

# ── VR Blend input ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(section_label("03 — VR Feed Blend"), unsafe_allow_html=True)
st.caption("Enter each VR component and its weight percentage. Total should equal 100%.")

if "import_vr_rows" not in st.session_state:
    st.session_state["import_vr_rows"] = [{"name": "", "pct": 0.0}]

vr_blend = []
rows_to_delete = []

col_h1, col_h2, col_h3 = st.columns([3, 2, 1])
col_h1.markdown(
    "<small style='color:var(--text-3);font-family:var(--font-display);"
    "letter-spacing:1px;font-size:0.7rem;text-transform:uppercase;'>VR Name</small>",
    unsafe_allow_html=True
)
col_h2.markdown(
    "<small style='color:var(--text-3);font-family:var(--font-display);"
    "letter-spacing:1px;font-size:0.7rem;text-transform:uppercase;'>% Usage (wt%)</small>",
    unsafe_allow_html=True
)

for i, row in enumerate(st.session_state["import_vr_rows"]):
    c1, c2, c3 = st.columns([3, 2, 1])
    name_val = c1.text_input(
        f"vr_name_{i}", value=row.get("name", ""),
        label_visibility="collapsed", placeholder="e.g. Basrah Heavy"
    )
    pct_val = c2.number_input(
        f"vr_pct_{i}", value=float(row.get("pct", 0.0)),
        min_value=0.0, max_value=100.0, step=1.0,
        label_visibility="collapsed"
    )
    if c3.button("✕", key=f"del_vr_import_{i}", help="Remove this VR"):
        rows_to_delete.append(i)
    if name_val.strip():
        vr_blend.append({"name": name_val.strip(), "pct": pct_val})

for idx in sorted(rows_to_delete, reverse=True):
    st.session_state["import_vr_rows"].pop(idx)
if rows_to_delete:
    st.rerun()

if len(st.session_state["import_vr_rows"]) < 6:
    if st.button("+ Add VR Component", type="secondary"):
        st.session_state["import_vr_rows"].append({"name": "", "pct": 0.0})
        st.rerun()

total_pct = sum(v["pct"] for v in vr_blend)
if vr_blend:
    if abs(total_pct - 100.0) < 0.1:
        st.success(f"✅ VR blend total: {total_pct:.1f}% — OK")
    else:
        st.warning(f"⚠️ VR blend total: {total_pct:.1f}% (should equal 100%)")

notes = st.text_area("Notes (optional)", height=72, placeholder="e.g. Run conditions, catalyst info, observations")

# ── Import button ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀  Import & Extract Data", type="primary", use_container_width=True):
    with st.spinner("Reading Excel file and extracting measurements..."):
        exp_id = upsert_experiment(
            exp_name=exp_name.strip(),
            exp_type=exp_type,
            start_date=start_date.strip(),
            file_path=selected_path,
            vr_blend=vr_blend,
            rx1_temp=rx1_temp,
            rx2_temp=rx2_temp,
            rx3_temp=rx3_temp,
            notes=notes.strip(),
        )
        records, err = extract_from_file(selected_path, exp_id=exp_id, exp_name=exp_name.strip())

    if err:
        st.error(f"Extraction error: {err}")
    elif not records:
        st.warning("No measurements could be extracted from this file. Check that the file has a 'Master Template' sheet with data.")
    else:
        inserted = bulk_insert_measurements(records)
        st.success(f"✅ **{exp_name}** imported successfully — {inserted} new measurements added ({len(records)} extracted from Excel).")
from utils.db import get_phases

# ── Database status ───────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(section_label("Current Database Status"), unsafe_allow_html=True)

experiments = get_all_experiments()
if not experiments:
    st.info("No experiments in the database yet. Use the form above to import your first experiment.")
else:
    sorted_exps = sorted(experiments, key=lambda e: e["exp_name"])
    rows = []
    for idx, e in enumerate(sorted_exps, start=1):
        phases = get_phases(e["id"])
        n_phases = len(phases)

        # Build VR feed names string from phases
        feed_names = []
        for p in phases:
            fn = p.get("feed_name")
            if fn and fn not in feed_names:
                feed_names.append(fn)
        vr_str = ", ".join(feed_names) if feed_names else "—"

        # Build temperature string from phases
        if phases:
            temp_parts = []
            for p in phases:
                label = p.get("phase_name") or "Phase"
                rx1 = p.get("rx1_temp", 0)
                rx2 = p.get("rx2_temp", 0)
                rx3 = p.get("rx3_temp", 0)
                temp_parts.append(f"{label}: {rx1:.0f}/{rx2:.0f}/{rx3:.0f}")
            temp_str = " | ".join(temp_parts)
        else:
            temp_str = "—"

        rows.append({
            "No": idx,
            "Experiment Name": e["exp_name"],
            "Start Date": e.get("start_date") or "—",
            "VR Feed": vr_str,
            "Phases": n_phases,
            "Temperature (Rx1/Rx2/Rx3)": temp_str,
            "Records": get_measurement_count(e["id"]),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

