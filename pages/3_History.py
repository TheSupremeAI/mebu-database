"""
MEBU Analytics — History Page
Cross-experiment comparison with overlaid charts.
"""
import streamlit as st
import json
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.db import init_db, get_all_experiments, get_multi_experiment_measurements
from utils.charts import multi_experiment_chart, PALETTE
from utils.styles import inject_css, page_header, section_label

init_db()
inject_css()

st.markdown(page_header(
    "Experiment History",
    subtitle="Compare multiple experiment runs side-by-side with overlaid charts.",
    icon="📈",
), unsafe_allow_html=True)

experiments = get_all_experiments()
if not experiments:
    st.warning("No experiments loaded. Go to **📥 Import** first.")
    st.stop()

# ── Sidebar: multi-select ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Select Experiments")
    exp_options = {e["exp_name"]: e["id"] for e in experiments}
    all_names = list(exp_options.keys())
    selected_names = st.multiselect(
        "Experiments to compare:",
        all_names,
        default=all_names[:min(2, len(all_names))],
    )

if not selected_names:
    st.info("Select at least one experiment from the sidebar to begin comparison.")
    st.stop()

selected_ids = [exp_options[n] for n in selected_names]
all_measurements = get_multi_experiment_measurements(selected_ids)

# ── Experiment legend cards ───────────────────────────────────────────────────
cols = st.columns(min(len(selected_names), 4))
for i, name in enumerate(selected_names):
    exp_meta = next((e for e in experiments if e["exp_name"] == name), None)
    if not exp_meta:
        continue
    blend = json.loads(exp_meta.get("vr_blend") or "[]")
    blend_str = " / ".join(f"{v['name']} {v['pct']}%" for v in blend) if blend else "—"
    color = PALETTE[i % len(PALETTE)]
    with cols[i % 4]:
        st.markdown(f"""
        <div style="background:var(--surface);border:1px solid {color}25;
                    border-left:2px solid {color};border-radius:var(--radius);
                    padding:16px 18px;margin-bottom:8px;position:relative;overflow:hidden;">
          <div style="position:absolute;top:0;right:0;width:80px;height:80px;
            background:radial-gradient(circle at top right,{color}10,transparent 70%);
            pointer-events:none;"></div>
          <div style="font-family:var(--font-display);font-size:0.62rem;font-weight:700;
            letter-spacing:2px;color:{color};margin-bottom:6px;">RUN {i+1}</div>
          <div style="font-family:var(--font-display);font-weight:600;font-size:0.92rem;
            letter-spacing:0.5px;color:var(--text);margin-bottom:10px;line-height:1.3;">
            {name[:45]}
          </div>
          <div style="color:var(--text-3);font-size:0.76rem;line-height:1.9;
            font-family:var(--font-mono);">
            <div><span style="color:var(--text-2);">DATE</span>&nbsp;&nbsp;{exp_meta.get('start_date') or '—'}</div>
            <div><span style="color:var(--text-2);">TYPE</span>&nbsp;&nbsp;{exp_meta.get('exp_type') or '—'}</div>
            <div><span style="color:var(--text-2);">VR&nbsp;&nbsp;&nbsp;</span>&nbsp;{blend_str[:50]}</div>
            <div><span style="color:var(--text-2);">RX°C&nbsp;</span>&nbsp;{exp_meta.get('rx1_temp') or '—'} / {exp_meta.get('rx2_temp') or '—'} / {exp_meta.get('rx3_temp') or '—'}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Helper ────────────────────────────────────────────────────────────────────
def overlay_chart(title, y_title, param_key):
    exp_data = []
    for exp_id, exp_name in zip(selected_ids, selected_names):
        rows = sorted(
            [m for m in all_measurements if m["exp_id"] == exp_id and m["parameter"] == param_key],
            key=lambda r: r["day"]
        )
        if rows:
            exp_data.append({
                "exp_name": exp_name,
                "x": [r["day"] for r in rows],
                "y": [r["value"] for r in rows],
            })
    if exp_data:
        fig = multi_experiment_chart(title, y_title, exp_data)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"No data for **{param_key}** in the selected experiments.")

# ── Comparison tabs ────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Cracking Conversion",
    "CATALYTIC CONVERSION",
    "Flow & LHSV",
])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        overlay_chart("Cracking Conversion (As is)", "wt%", "CrkConv")
    with c2:
        overlay_chart("Total Sedimentation", "ppm", "Sedimentation")

with tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        overlay_chart("Sulfur Conversion", "wt%", "SConv")
        overlay_chart("Nickel Conversion", "wt%", "NiConv")
        overlay_chart("MCR Conversion", "wt%", "MCRConv")
        overlay_chart("C7 Asphaltene Conversion", "wt%", "C7_AsphConv")
    with c2:
        overlay_chart("Nitrogen Conversion", "wt%", "NConv")
        overlay_chart("Vanadium Conversion", "wt%", "VConv")
        overlay_chart("Ni+V Conversion", "wt%", "NiV_Conv")
        overlay_chart("C5 Asphaltene Conversion", "wt%", "C5_AsphConv")

with tabs[2]:
    c1, c2 = st.columns(2)
    with c1:
        overlay_chart("LHSV — Space Velocity", "hr⁻¹", "LHSV_actual")
    with c2:
        overlay_chart("Total Feed Rate", "g/h", "Total_rate")


# ── Summary stats table ───────────────────────────────────────────────────────

st.markdown("<hr>", unsafe_allow_html=True)
with st.expander("📊 Summary Statistics (avg over all days)"):
    summary_rows = []
    key_params = ["CrkConv", "NiConv", "VConv", "NiV_Conv", "SConv", "MCRConv", "Sedimentation"]
    for exp_id, exp_name in zip(selected_ids, selected_names):
        for pk in key_params:
            rows = [m for m in all_measurements if m["exp_id"] == exp_id and m["parameter"] == pk]
            if rows:
                vals = [r["value"] for r in rows]
                summary_rows.append({
                    "Experiment": exp_name,
                    "Parameter": pk,
                    "N Days": len(vals),
                    "Mean": round(sum(vals)/len(vals), 2),
                    "Min": round(min(vals), 2),
                    "Max": round(max(vals), 2),
                })
    if summary_rows:
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No data available for summary.")
