"""
MEBU Analytics — Settings Page
Edit experiment metadata: VR blend, reactor temperatures, notes.
"""
import streamlit as st
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.db import (init_db, get_all_experiments, get_experiment,
                      update_experiment_meta, delete_experiment, get_measurement_count)
from utils.styles import inject_css, page_header, section_label
from utils.charts import PALETTE

init_db()
inject_css()

st.markdown(page_header(
    "Settings",
    subtitle="Edit VR blend composition, reactor temperatures, and notes for any experiment.",
    icon="⚙️",
), unsafe_allow_html=True)

experiments = get_all_experiments()
if not experiments:
    st.info("No experiments loaded yet. Go to **📥 Import** first.")
    st.stop()

exp_map       = {e["exp_name"]: e for e in experiments}
selected_name = st.selectbox("Select experiment to edit:", list(exp_map.keys()))
exp           = exp_map[selected_name]
exp_id        = exp["id"]

n_meas = get_measurement_count(exp_id)
st.markdown(f"""
<div style="display:inline-flex;align-items:center;gap:12px;
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);padding:10px 20px;margin-bottom:20px;">
  <span style="font-family:var(--font-display);font-size:0.68rem;font-weight:600;
    letter-spacing:2px;text-transform:uppercase;color:var(--text-2);">Database records</span>
  <span style="font-family:var(--font-mono);font-size:1rem;color:var(--plasma);
    font-weight:500;">{n_meas:,}</span>
</div>
""", unsafe_allow_html=True)

# ── VR Blend editor ───────────────────────────────────────────────────────────
st.markdown(section_label("VR Feed Blend"), unsafe_allow_html=True)
current_blend = json.loads(exp.get("vr_blend") or "[]")

sess_key = f"settings_vr_{exp_id}"
if sess_key not in st.session_state:
    st.session_state[sess_key] = (
        [{"name": v["name"], "pct": v["pct"]} for v in current_blend]
        if current_blend else [{"name": "", "pct": 0.0}]
    )

vr_blend_new = []
rows_to_del  = []

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

for i, row in enumerate(st.session_state[sess_key]):
    c1, c2, c3 = st.columns([3, 2, 1])
    name_v = c1.text_input(
        f"s_name_{exp_id}_{i}", value=row.get("name", ""),
        label_visibility="collapsed", placeholder="VR Name"
    )
    pct_v = c2.number_input(
        f"s_pct_{exp_id}_{i}", value=float(row.get("pct", 0.0)),
        min_value=0.0, max_value=100.0, step=1.0, label_visibility="collapsed"
    )
    if c3.button("✕", key=f"sdel_{exp_id}_{i}"):
        rows_to_del.append(i)
    if name_v.strip():
        vr_blend_new.append({"name": name_v.strip(), "pct": pct_v})

for idx in sorted(rows_to_del, reverse=True):
    st.session_state[sess_key].pop(idx)
if rows_to_del:
    st.rerun()

if len(st.session_state[sess_key]) < 6:
    if st.button("+ Add VR Component", key=f"sadd_{exp_id}", type="secondary"):
        st.session_state[sess_key].append({"name": "", "pct": 0.0})
        st.rerun()

total_pct = sum(v["pct"] for v in vr_blend_new)
if vr_blend_new:
    if abs(total_pct - 100.0) < 0.1:
        st.success(f"✅ Total: {total_pct:.1f}%")
    else:
        st.warning(f"⚠️ Total: {total_pct:.1f}% (should be 100%)")

# ── Temperatures & Notes ──────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(section_label("Reactor Temperatures & Notes"), unsafe_allow_html=True)
tc1, tc2, tc3 = st.columns(3)
rx1 = tc1.number_input("Rx-1 (°C)", value=float(exp.get("rx1_temp") or 404.0),
                        step=0.5, format="%.1f", key=f"srx1_{exp_id}")
rx2 = tc2.number_input("Rx-2 (°C)", value=float(exp.get("rx2_temp") or 405.0),
                        step=0.5, format="%.1f", key=f"srx2_{exp_id}")
rx3 = tc3.number_input("Rx-3 (°C)", value=float(exp.get("rx3_temp") or 406.0),
                        step=0.5, format="%.1f", key=f"srx3_{exp_id}")
notes = st.text_area("Notes", value=exp.get("notes") or "",
                      height=100, key=f"snotes_{exp_id}",
                      placeholder="Catalyst info, run conditions, observations...")

st.markdown("<br>", unsafe_allow_html=True)
if st.button("💾  Save Changes", type="primary", key=f"ssave_{exp_id}", use_container_width=False):
    update_experiment_meta(
        exp_id,
        vr_blend=vr_blend_new,
        rx1_temp=rx1, rx2_temp=rx2, rx3_temp=rx3,
        notes=notes,
    )
    st.success("✅ Changes saved successfully.")
    st.rerun()

# ── Preview of current blend ──────────────────────────────────────────────────
if vr_blend_new:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(section_label("Current VR Blend Preview"), unsafe_allow_html=True)
    blend_cols = st.columns(len(vr_blend_new))
    for i, v in enumerate(vr_blend_new):
        color = PALETTE[i % len(PALETTE)]
        with blend_cols[i]:
            st.markdown(f"""
            <div style="background:var(--surface);border:1px solid {color}25;
                        border-top:2px solid {color};border-radius:var(--radius);
                        padding:16px 12px;text-align:center;position:relative;overflow:hidden;">
              <div style="position:absolute;top:0;right:0;width:60px;height:60px;
                background:radial-gradient(circle at top right,{color}12,transparent 70%);
                pointer-events:none;"></div>
              <div style="font-family:var(--font-mono);font-size:1.4rem;font-weight:500;
                color:{color};">{v['pct']:.0f}%</div>
              <div style="font-family:var(--font-display);font-size:0.72rem;font-weight:600;
                letter-spacing:1px;color:var(--text-2);margin-top:6px;text-transform:uppercase;">
                {v['name']}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Danger zone ────────────────────────────────────────────────────────────────
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(section_label("⚠ Danger Zone"), unsafe_allow_html=True)
with st.expander("Delete this experiment and all its data"):
    st.warning(
        f"This will permanently delete **{selected_name}** and all {n_meas:,} associated measurements. "
        f"This cannot be undone."
    )
    confirm_input = st.text_input(
        "Type the full experiment name to confirm:",
        placeholder=selected_name, key=f"sdel_confirm_{exp_id}"
    )
    if st.button("🗑️  Delete Permanently", type="primary", key=f"sdel_btn_{exp_id}"):
        if confirm_input.strip() == selected_name.strip():
            delete_experiment(exp_id)
            st.success("Experiment deleted.")
            st.rerun()
        else:
            st.error("Name does not match. Deletion cancelled.")
