"""
MEBU Analytics — Dashboard Page
Single experiment view with Lab Results Summary charts + Phase bands.
"""
import streamlit as st
import json
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.db import init_db, get_all_experiments, get_measurements, get_experiment, get_phases
from utils.charts import line_chart, PALETTE, add_phase_bands

init_db()

from utils.styles import inject_css, page_header, temp_badge, section_label
inject_css()

st.markdown(page_header(
    "Experiment Dashboard",
    subtitle="Single-experiment view — all key lab result charts mirroring the Lab Results Summary sheet.",
    icon="📊",
), unsafe_allow_html=True)

experiments = get_all_experiments()
if not experiments:
    st.warning("No experiments loaded. Go to **📥 Import** first.")
    st.stop()

# ── Sidebar selector ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Select Experiment")
    exp_names = [e["exp_name"] for e in experiments]
    exp_map   = {e["exp_name"]: e["id"] for e in experiments}
    selected_name = st.selectbox("Experiment:", exp_names, index=len(exp_names) - 1)
    exp_id = exp_map[selected_name]

exp = get_experiment(exp_id)
measurements = get_measurements(exp_id)
phases = get_phases(exp_id)
avail_params = set(m["parameter"] for m in measurements)

# ── Run metadata card ─────────────────────────────────────────────────────────
card_col, phase_col = st.columns([2, 1])

with card_col:
    meas_count = len(measurements)
    days_count = len(set(m["day"] for m in measurements)) if measurements else 0

    # Show phase temperature ranges if available
    if phases:
        temps_parts = []
        for p in phases:
            rx_vals = []
            for rx_label, rx_key in [("Rx-1", "rx1_temp"), ("Rx-2", "rx2_temp"), ("Rx-3", "rx3_temp")]:
                val = p.get(rx_key)
                if val:
                    rx_vals.append(f"{rx_label}:{val:.0f}°")
            phase_label = p.get("phase_name") or p.get("feed_name") or "Phase"
            temps_parts.append(f"<small style='color:var(--text-3);'>{phase_label}:</small> {'  '.join(rx_vals)}")
        temps_html = "<br>".join(temps_parts)
    else:
        temps_html = "".join(
            temp_badge(rx, exp.get(key))
            for rx, key in [("Rx-1", "rx1_temp"), ("Rx-2", "rx2_temp"), ("Rx-3", "rx3_temp")]
        )

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,var(--surface) 0%,var(--surface-2) 100%);
                border:1px solid var(--border);border-top:2px solid var(--gold);
                border-radius:var(--radius);padding:24px 28px;margin-bottom:8px;
                box-shadow:0 8px 32px rgba(0,0,0,0.4);position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;right:0;width:160px;height:160px;
        background:radial-gradient(circle at top right,var(--gold-dim),transparent 70%);
        pointer-events:none;"></div>
      <div style="font-family:var(--font-display);font-size:0.7rem;font-weight:700;
        letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:12px;">
        ◈ EXPERIMENT RECORD
      </div>
      <h3 style="font-family:var(--font-display);color:var(--text);margin:0 0 18px;
        font-size:1.3rem;letter-spacing:1px;font-weight:700;">
        {exp['exp_name']}
      </h3>
      <table style="color:var(--text);border-spacing:0;width:100%;font-size:0.86rem;">
        <tr>
          <td style="color:var(--text-3);font-family:var(--font-display);font-size:0.68rem;
            font-weight:600;letter-spacing:1.5px;text-transform:uppercase;width:140px;padding:5px 0;">
            Type</td>
          <td style="font-family:var(--font-mono);">{exp.get('exp_type') or '—'}</td>
        </tr>
        <tr>
          <td style="color:var(--text-3);font-family:var(--font-display);font-size:0.68rem;
            font-weight:600;letter-spacing:1.5px;text-transform:uppercase;padding:5px 0;">
            Start Date</td>
          <td style="font-family:var(--font-mono);">{exp.get('start_date') or '—'}</td>
        </tr>
        <tr>
          <td style="color:var(--text-3);font-family:var(--font-display);font-size:0.68rem;
            font-weight:600;letter-spacing:1.5px;text-transform:uppercase;padding:5px 0;">
            Measurements</td>
          <td style="font-family:var(--font-mono);color:var(--gold);">
            {meas_count:,} readings across {days_count} days</td>
        </tr>
        <tr>
          <td style="color:var(--text-3);font-family:var(--font-display);font-size:0.68rem;
            font-weight:600;letter-spacing:1.5px;text-transform:uppercase;padding:5px 0;">
            Notes</td>
          <td style="color:var(--text-2);font-family:var(--font-body);font-size:0.84rem;">
            {exp.get('notes') or '—'}</td>
        </tr>
      </table>
      <div style="margin-top:18px;font-family:var(--font-mono);font-size:0.78rem;
        color:var(--text-2);line-height:1.8;">{temps_html}</div>
    </div>
    """, unsafe_allow_html=True)

with phase_col:
    if phases and len(phases) >= 1:
        st.markdown(section_label("Phase Summary"), unsafe_allow_html=True)
        for pi, p in enumerate(phases):
            color = PALETTE[pi % len(PALETTE)]
            feed_label = p.get("feed_name") or "No Feed"
            st.markdown(f"""
            <div style="background:var(--surface);border:1px solid {color}25;
                        border-left:3px solid {color};border-radius:var(--radius);
                        padding:10px 14px;margin-bottom:6px;">
              <div style="font-family:var(--font-display);font-size:0.65rem;font-weight:700;
                letter-spacing:2px;text-transform:uppercase;color:{color};">
                {p.get('phase_name') or f'Phase {pi+1}'}</div>
              <div style="font-family:var(--font-mono);font-size:0.82rem;color:var(--text);
                margin-top:2px;">Day {p['from_day']}–{p['to_day']}</div>
              <div style="font-family:var(--font-mono);font-size:0.72rem;color:var(--text-2);
                margin-top:2px;">{feed_label}</div>
              <div style="font-family:var(--font-mono);font-size:0.62rem;color:var(--text-3);
                margin-top:2px;">
                {p.get('rx1_temp', 0):.0f}° / {p.get('rx2_temp', 0):.0f}° / {p.get('rx3_temp', 0):.0f}°
              </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:var(--surface);border:1px solid var(--border);
                    border-radius:var(--radius);padding:40px 20px;text-align:center;">
          <div style="font-family:var(--font-mono);color:var(--text-3);font-size:0.82rem;
            letter-spacing:1px;">NO PHASES SET</div>
          <div style="color:var(--text-3);font-size:0.78rem;margin-top:8px;
            font-family:var(--font-body);">Edit in ⚙️ Settings</div>
        </div>
        """, unsafe_allow_html=True)

if not measurements:
    st.warning("No measurement data found for this experiment. Go to 📥 Import and (re-)import this file.")
    st.stop()

# ── Helper ────────────────────────────────────────────────────────────────────
def get_series(param_key, label=None):
    rows = sorted([m for m in measurements if m["parameter"] == param_key],
                  key=lambda r: r["day"])
    return (
        {"name": label or param_key, "x": [r["day"] for r in rows], "y": [r["value"] for r in rows]},
        rows[0]["art_low"] if rows else None,
        rows[0]["art_high"] if rows else None,
    )

def chart_or_info(title, y_title, param_pairs, color=None):
    """
    Build a line chart from a list of (param_key, label) pairs.
    color: optional hex color to force for the first series.
    Automatically adds phase bands if phases exist.
    """
    series_list = []
    for i, (pk, lbl) in enumerate(param_pairs):
        if pk in avail_params:
            s, _, _ = get_series(pk, lbl)
            if i == 0 and color:
                s["color"] = color
            series_list.append(s)
    
    if series_list:
        fig = line_chart(title, y_title, series_list)
        if phases:
            add_phase_bands(fig, phases)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"Data not available for this chart in the selected experiment.")

# ── Chart tabs ────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

tabs = st.tabs([
    "Cracking Conversion",
    "CATALYTIC CONVERSION",
    "Flow & LHSV",
    "Custom Plot",
])

with tabs[0]:
    chart_or_info(
        "Cracking Conversion (As is)", "wt%",
        [("CrkConv", "Cracking Conv. (wt%)")],
        color="#FFB800" # Molten Gold
    )
    chart_or_info(
        "Total Sedimentation", "ppm",
        [("Sedimentation", "Sedimentation (ppm)")],
        color="#FF6B6B" # Coral
    )

with tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        chart_or_info("Sulfur Conversion", "wt%", [("SConv", "S Conv. (wt%)")], color="#C9901A")
        chart_or_info("Nickel Conversion", "wt%", [("NiConv", "Ni Conv. (wt%)")], color="#00D4FF")
        chart_or_info("MCR Conversion", "wt%", [("MCRConv", "MCR Conv. (wt%)")], color="#C8A2C8")
        chart_or_info("C7 Asphaltene Conversion", "wt%", [("C7_AsphConv", "C7 Conv. (wt%)")], color="#FFB800")
    with c2:
        chart_or_info("Nitrogen Conversion", "wt%", [("NConv", "N Conv. (wt%)")], color="#7B61FF")
        chart_or_info("Vanadium Conversion", "wt%", [("VConv", "V Conv. (wt%)")], color="#FF9F43")
        chart_or_info("Ni+V Conversion", "wt%", [("NiV_Conv", "Ni+V Conv. (wt%)")], color="#00F5A0")
        chart_or_info("C5 Asphaltene Conversion", "wt%", [("C5_AsphConv", "C5 Conv. (wt%)")], color="#FF6B6B")


with tabs[2]:
    c1, c2 = st.columns(2)
    with c1:
        chart_or_info("LHSV — Space Velocity", "hr⁻¹",
                      [("LHSV_actual", "LHSV Actual (hr⁻¹)")])
    with c2:
        chart_or_info("Total Feed Rate", "g/h",
                      [("Total_rate", "Total Rate (g/h)")])

with tabs[3]:
    # Filter parameters to only those used in the first three tabs
    active_keys = [
        "CrkConv", "Sedimentation", "SConv", "NConv", "NiConv", 
        "VConv", "NiV_Conv", "MCRConv", "C7_AsphConv", "C5_AsphConv",
        "LHSV_actual", "Total_rate"
    ]
    custom_params = sorted([p for p in active_keys if p in avail_params])
    
    default_sel = [p for p in ["CrkConv", "SConv"] if p in custom_params]
    selected_params = st.multiselect("Select parameters:", custom_params,
                                      default=default_sel)
    if selected_params:
        series_list = []
        for pk in selected_params:
            s, _, _ = get_series(pk)
            series_list.append(s)
        fig = line_chart("Custom Parameter Selection", "Value", series_list)
        if phases:
            add_phase_bands(fig, phases)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select one or more parameters above to plot.")


# ── Raw data expander ─────────────────────────────────────────────────────────
with st.expander("📋 View Raw Measurement Data"):
    df = pd.DataFrame(measurements)
    if not df.empty:
        st.dataframe(
            df[["day", "op_date", "lab_date", "category", "parameter", "unit", "value", "within_spec"]],
            use_container_width=True, hide_index=True
        )
