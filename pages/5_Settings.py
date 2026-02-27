"""
MEBU Analytics — Settings Page
Phase Timeline Editor + VR Feed Library + Notes.
"""
import streamlit as st
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.db import (init_db, get_all_experiments, get_experiment,
                      update_experiment_meta, delete_experiment, get_measurement_count,
                      get_all_vr_feeds, upsert_vr_feed, delete_vr_feed,
                      save_phases, get_phases)
from utils.styles import inject_css, page_header, section_label
from utils.charts import PALETTE, PHASE_COLORS, PHASE_BORDER_COLORS

init_db()
inject_css()

st.markdown(page_header(
    "Settings",
    subtitle="Manage experiment phases, VR feed library, and metadata.",
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
  <span style="font-family:var(--font-ui);font-size:0.68rem;font-weight:700;
    letter-spacing:2px;text-transform:uppercase;color:var(--text-2);">Database records</span>
  <span style="font-family:var(--font-mono);font-size:1rem;color:var(--gold-bright);
    font-weight:500;">{n_meas:,}</span>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ── VR Feed Library ──────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(section_label("📚 VR Feed Library"), unsafe_allow_html=True)

with st.expander("Manage VR Feed Recipes", expanded=False):
    feeds = get_all_vr_feeds()

    # ── Session state for new feed form ──
    if "new_feed_mode" not in st.session_state:
        st.session_state["new_feed_mode"] = False

    # ── Existing feeds ──
    if feeds:
        for fi, feed in enumerate(feeds):
            comp = json.loads(feed.get("composition") or "[]")
            comp_str = ", ".join(f"{c['name']} {c['pct']:.0f}%" for c in comp) if comp else "No composition"
            col_name, col_del = st.columns([5, 1])
            col_name.markdown(f"""
            <div style="background:var(--surface);border:1px solid var(--border);
                        border-radius:var(--radius);padding:12px 16px;margin-bottom:6px;">
              <div style="font-family:var(--font-display);font-size:0.82rem;font-weight:700;
                color:var(--gold);letter-spacing:1px;text-transform:uppercase;">
                {feed['feed_name']}</div>
              <div style="font-family:var(--font-mono);font-size:0.78rem;color:var(--text-2);
                margin-top:4px;">{comp_str}</div>
            </div>
            """, unsafe_allow_html=True)
            if col_del.button("🗑️", key=f"delfeed_{feed['id']}"):
                delete_vr_feed(feed["id"])
                st.rerun()
    else:
        st.caption("No feeds in library yet. Create one below.")

    st.markdown("---")
    st.markdown("##### ➕ Create New VR Feed")

    new_feed_name = st.text_input("Feed Name (e.g. ABQ3358)", key="new_feed_name",
                                   placeholder="ABQ3358")

    # Composition rows
    comp_key = "new_feed_comp"
    if comp_key not in st.session_state:
        st.session_state[comp_key] = [{"name": "", "pct": 0.0}]

    ch1, ch2, ch3 = st.columns([3, 2, 1])
    ch1.markdown("<small style='color:var(--text-3);font-family:var(--font-display);"
                 "letter-spacing:1px;font-size:0.7rem;text-transform:uppercase;'>Crude VR Name</small>",
                 unsafe_allow_html=True)
    ch2.markdown("<small style='color:var(--text-3);font-family:var(--font-display);"
                 "letter-spacing:1px;font-size:0.7rem;text-transform:uppercase;'>% (wt%)</small>",
                 unsafe_allow_html=True)

    comp_new = []
    comp_to_del = []
    for ci, crow in enumerate(st.session_state[comp_key]):
        cc1, cc2, cc3 = st.columns([3, 2, 1])
        cn = cc1.text_input(f"comp_n_{ci}", value=crow.get("name", ""),
                           label_visibility="collapsed", placeholder="Basrah Heavy")
        cp = cc2.number_input(f"comp_p_{ci}", value=float(crow.get("pct", 0.0)),
                             min_value=0.0, max_value=100.0, step=1.0,
                             label_visibility="collapsed")
        if cc3.button("✕", key=f"comp_del_{ci}"):
            comp_to_del.append(ci)
        if cn.strip():
            comp_new.append({"name": cn.strip(), "pct": cp})

    for idx in sorted(comp_to_del, reverse=True):
        st.session_state[comp_key].pop(idx)
    if comp_to_del:
        st.rerun()

    bc1, bc2 = st.columns(2)
    if bc1.button("+ Add Component", key="add_comp_row"):
        st.session_state[comp_key].append({"name": "", "pct": 0.0})
        st.rerun()

    if bc2.button("💾 Save Feed", key="save_new_feed", type="primary"):
        if new_feed_name.strip() and comp_new:
            upsert_vr_feed(new_feed_name.strip(), comp_new)
            st.session_state[comp_key] = [{"name": "", "pct": 0.0}]
            st.success(f"✅ Feed '{new_feed_name.strip()}' saved!")
            st.rerun()
        else:
            st.error("Enter a feed name and at least one component.")


# ══════════════════════════════════════════════════════════════════════════════
# ── Phase Timeline Editor ────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(section_label("🔬 Phase Timeline Editor"), unsafe_allow_html=True)

# Load existing phases
existing_phases = get_phases(exp_id)
feeds = get_all_vr_feeds()  # refresh
feed_map = {f["id"]: f["feed_name"] for f in feeds}
feed_names = ["— None —"] + [f["feed_name"] for f in feeds]
feed_id_by_name = {f["feed_name"]: f["id"] for f in feeds}

phase_sess_key = f"phases_{exp_id}"
if phase_sess_key not in st.session_state:
    if existing_phases:
        st.session_state[phase_sess_key] = [
            {
                "phase_name": p.get("phase_name") or "",
                "from_day": p.get("from_day") or 1,
                "to_day": p.get("to_day") or 28,
                "feed_name": p.get("feed_name") or "— None —",
                "rx1_temp": p.get("rx1_temp") or 404.0,
                "rx2_temp": p.get("rx2_temp") or 405.0,
                "rx3_temp": p.get("rx3_temp") or 406.0,
            }
            for p in existing_phases
        ]
    else:
        st.session_state[phase_sess_key] = [{
            "phase_name": "Phase 1",
            "from_day": 1,
            "to_day": 28,
            "feed_name": "— None —",
            "rx1_temp": 404.0,
            "rx2_temp": 405.0,
            "rx3_temp": 406.0,
        }]

phases_to_del = []

for pi, phase in enumerate(st.session_state[phase_sess_key]):
    phase_color = PALETTE[pi % len(PALETTE)]

    st.markdown(f"""
    <div style="background:var(--surface);border:1px solid {phase_color}25;
                border-left:3px solid {phase_color};border-radius:var(--radius);
                padding:16px 20px;margin-bottom:10px;">
      <div style="font-family:var(--font-display);font-size:0.72rem;font-weight:700;
        letter-spacing:2px;text-transform:uppercase;color:{phase_color};margin-bottom:10px;">
        ◆ Phase {pi+1}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Row 1: Phase Name + Day Range + Delete
    r1c1, r1c2, r1c3, r1c4 = st.columns([3, 1.5, 1.5, 0.5])
    pname = r1c1.text_input("Phase Name", value=phase.get("phase_name", ""),
                            key=f"pname_{exp_id}_{pi}", placeholder="e.g. Catalyst Aging")
    fday = r1c2.number_input("From Day", value=int(phase.get("from_day", 1)),
                             min_value=1, max_value=365, step=1, key=f"fday_{exp_id}_{pi}")
    tday = r1c3.number_input("To Day", value=int(phase.get("to_day", 28)),
                             min_value=1, max_value=365, step=1, key=f"tday_{exp_id}_{pi}")
    if r1c4.button("✕", key=f"pdel_{exp_id}_{pi}"):
        phases_to_del.append(pi)

    # Row 2: VR Feed + Temperatures
    r2c1, r2c2, r2c3, r2c4 = st.columns([2.5, 1.5, 1.5, 1.5])
    current_feed = phase.get("feed_name", "— None —")
    feed_idx = feed_names.index(current_feed) if current_feed in feed_names else 0
    selected_feed = r2c1.selectbox("VR Feed", feed_names, index=feed_idx,
                                    key=f"pfeed_{exp_id}_{pi}")
    rx1 = r2c2.number_input("Rx-1 (°C)", value=float(phase.get("rx1_temp", 404.0)),
                            step=0.5, format="%.1f", key=f"prx1_{exp_id}_{pi}")
    rx2 = r2c3.number_input("Rx-2 (°C)", value=float(phase.get("rx2_temp", 405.0)),
                            step=0.5, format="%.1f", key=f"prx2_{exp_id}_{pi}")
    rx3 = r2c4.number_input("Rx-3 (°C)", value=float(phase.get("rx3_temp", 406.0)),
                            step=0.5, format="%.1f", key=f"prx3_{exp_id}_{pi}")

    # Update session state
    st.session_state[phase_sess_key][pi] = {
        "phase_name": pname,
        "from_day": fday,
        "to_day": tday,
        "feed_name": selected_feed,
        "rx1_temp": rx1,
        "rx2_temp": rx2,
        "rx3_temp": rx3,
    }

# Delete phases
for idx in sorted(phases_to_del, reverse=True):
    st.session_state[phase_sess_key].pop(idx)
if phases_to_del:
    st.rerun()

# Add Phase button
if len(st.session_state[phase_sess_key]) < 8:
    if st.button("➕ Add Phase", key=f"padd_{exp_id}", type="secondary"):
        last = st.session_state[phase_sess_key][-1] if st.session_state[phase_sess_key] else {}
        next_from = (last.get("to_day", 0) or 0) + 1
        st.session_state[phase_sess_key].append({
            "phase_name": f"Phase {len(st.session_state[phase_sess_key]) + 1}",
            "from_day": next_from,
            "to_day": next_from + 6,
            "feed_name": "— None —",
            "rx1_temp": last.get("rx1_temp", 404.0),
            "rx2_temp": last.get("rx2_temp", 405.0),
            "rx3_temp": last.get("rx3_temp", 406.0),
        })
        st.rerun()

# ── Notes ─────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(section_label("Notes"), unsafe_allow_html=True)
notes = st.text_area("Notes", value=exp.get("notes") or "",
                      height=100, key=f"snotes_{exp_id}",
                      placeholder="Catalyst info, run conditions, observations...")

# ── Save button ──────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if st.button("💾  Save All Changes", type="primary", key=f"ssave_{exp_id}"):
    # Build phases list for DB
    phases_for_db = []
    for p in st.session_state[phase_sess_key]:
        feed_id = feed_id_by_name.get(p["feed_name"]) if p["feed_name"] != "— None —" else None
        phases_for_db.append({
            "phase_name": p["phase_name"],
            "from_day": p["from_day"],
            "to_day": p["to_day"],
            "feed_id": feed_id,
            "rx1_temp": p["rx1_temp"],
            "rx2_temp": p["rx2_temp"],
            "rx3_temp": p["rx3_temp"],
        })
    save_phases(exp_id, phases_for_db)
    update_experiment_meta(exp_id, notes=notes)
    st.success("✅ Phases and notes saved successfully.")
    st.rerun()

# ── Phase Timeline Preview ────────────────────────────────────────────────────
if st.session_state[phase_sess_key]:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(section_label("Phase Timeline Preview"), unsafe_allow_html=True)

    phase_cols = st.columns(len(st.session_state[phase_sess_key]))
    for pi, p in enumerate(st.session_state[phase_sess_key]):
        color = PALETTE[pi % len(PALETTE)]
        with phase_cols[pi]:
            feed_display = p["feed_name"] if p["feed_name"] != "— None —" else "No Feed"
            st.markdown(f"""
            <div style="background:var(--surface);border:1px solid {color}25;
                        border-top:3px solid {color};border-radius:var(--radius);
                        padding:14px 10px;text-align:center;position:relative;overflow:hidden;">
              <div style="position:absolute;top:0;right:0;width:50px;height:50px;
                background:radial-gradient(circle at top right,{color}15,transparent 70%);
                pointer-events:none;"></div>
              <div style="font-family:var(--font-display);font-size:0.65rem;font-weight:700;
                letter-spacing:2px;text-transform:uppercase;color:{color};margin-bottom:6px;">
                {p.get('phase_name') or f'Phase {pi+1}'}</div>
              <div style="font-family:var(--font-mono);font-size:1.1rem;font-weight:500;
                color:{color};">Day {p['from_day']}–{p['to_day']}</div>
              <div style="font-family:var(--font-mono);font-size:0.72rem;color:var(--text-2);
                margin-top:6px;">{feed_display}</div>
              <div style="font-family:var(--font-mono);font-size:0.65rem;color:var(--text-3);
                margin-top:4px;">
                {p.get('rx1_temp', 0):.0f}° / {p.get('rx2_temp', 0):.0f}° / {p.get('rx3_temp', 0):.0f}°
              </div>
            </div>
            """, unsafe_allow_html=True)

# ── Export Experiment Data ─────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(section_label("📤 Export Experiment Data"), unsafe_allow_html=True)

with st.expander("Export phases, VR feeds, and temperatures to CSV", expanded=False):
    import io
    import csv

    export_phases = get_phases(exp_id)
    if export_phases:
        # Build CSV in memory
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow([
            "Experiment", "Phase Name", "From Day", "To Day",
            "VR Feed Name", "VR Composition",
            "Rx-1 (°C)", "Rx-2 (°C)", "Rx-3 (°C)"
        ])
        for p in export_phases:
            comp = json.loads(p.get("composition") or "[]")
            comp_str = " | ".join(f"{c['name']} {c['pct']:.0f}%" for c in comp) if comp else ""
            writer.writerow([
                selected_name,
                p.get("phase_name") or "",
                p.get("from_day", ""),
                p.get("to_day", ""),
                p.get("feed_name") or "",
                comp_str,
                p.get("rx1_temp") or "",
                p.get("rx2_temp") or "",
                p.get("rx3_temp") or "",
            ])

        csv_data = buffer.getvalue()
        safe_name = selected_name.replace("'", "").replace('"', '').replace("/", "_")
        st.download_button(
            label="⬇️ Download Phase Data (CSV)",
            data=csv_data,
            file_name=f"{safe_name}_phases.csv",
            mime="text/csv",
            key=f"export_phases_{exp_id}",
        )

        # Preview
        st.markdown("**Preview:**")
        preview_data = []
        for p in export_phases:
            comp = json.loads(p.get("composition") or "[]")
            comp_str = " | ".join(f"{c['name']} {c['pct']:.0f}%" for c in comp) if comp else "—"
            preview_data.append({
                "Phase": p.get("phase_name") or "—",
                "Days": f"{p.get('from_day', '?')}–{p.get('to_day', '?')}",
                "VR Feed": p.get("feed_name") or "—",
                "Composition": comp_str,
                "Rx-1": f"{p.get('rx1_temp', 0):.0f}°" if p.get('rx1_temp') else "—",
                "Rx-2": f"{p.get('rx2_temp', 0):.0f}°" if p.get('rx2_temp') else "—",
                "Rx-3": f"{p.get('rx3_temp', 0):.0f}°" if p.get('rx3_temp') else "—",
            })
        import pandas as pd
        st.dataframe(pd.DataFrame(preview_data), use_container_width=True, hide_index=True)
    else:
        st.info("No phases to export. Add phases above first.")


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
