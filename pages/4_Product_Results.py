"""
MEBU Analytics — Product Lab Results Page
Displays daily results for HPS, LTO, ISV and Gas compositions.
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.db import init_db, get_all_experiments, get_measurements, get_experiment, get_phases
from utils.charts import line_chart, add_phase_bands
from utils.styles import inject_css, page_header, section_label

init_db()
inject_css()

st.markdown(page_header(
    "Product Lab Results",
    subtitle="Detailed daily properties for HPS, LTO, ISV, and Gas components.",
    icon="🧪",
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

measurements = get_measurements(exp_id)
phases = get_phases(exp_id)
avail_params = set(m["parameter"] for m in measurements)

with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Record Counts")
    cat_counts = {}
    for m in measurements:
        cat_counts[m["category"]] = cat_counts.get(m["category"], 0) + 1
    
    for cat in ["HPS Product", "LTO Product", "ISV Product", "High Gas", "Low Gas"]:
        count = cat_counts.get(cat, 0)
        st.write(f"**{cat}:** {count} records")

if not measurements:

    st.warning("No measurement data found for this experiment. Please (re-)import this file.")
    st.stop()

def get_series(param_key, label=None):
    rows = sorted([m for m in measurements if m["parameter"] == param_key],
                  key=lambda r: r["day"])
    return (
        {"name": label or param_key, "x": [r["day"] for r in rows], "y": [r["value"] for r in rows]},
    )

def product_chart(title, y_title, param_pairs, color=None):
    series_list = []
    for i, (pk, lbl) in enumerate(param_pairs):
        if pk in avail_params:
            s_tuple = get_series(pk, lbl)
            s = s_tuple[0]
            if i == 0 and color:
                s["color"] = color
            series_list.append(s)
    
    if series_list:
        fig = line_chart(title, y_title, series_list)
        if phases:
            add_phase_bands(fig, phases)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"Data not available for {title}.")

def product_table(category):
    """Render a pivoted dataframe for a specific product category."""
    cat_data = [m for m in measurements if m["category"] == category]
    if not cat_data:
        return
    
    df = pd.DataFrame(cat_data)
    # Pivot: Days as rows, Parameters as columns
    pivot_df = df.pivot(index="day", columns="parameter", values="value")
    # Clean up column names (remove category prefix if exists)
    pivot_df.columns = [c.replace(f"{category.split()[0]}_", "").replace("_", " ") for c in pivot_df.columns]
    
    with st.expander(f"📋 View {category} Data Table", expanded=False):
        st.dataframe(pivot_df, use_container_width=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs(["HPS Results", "LTO Results", "ISV Results", "Gas Composition"])

with tabs[0]:
    st.markdown(section_label("HPS Daily Properties"), unsafe_allow_html=True)
    product_table("HPS Product")
    c1, c2 = st.columns(2)
    with c1:
        product_chart("HPS API (ASTM D4052)", "API", [("HPS_API", "API")], color="#FFB800")
        product_chart("HPS Sulfur (ASTM D4294)", "wt%", [("HPS_Sulfur", "Sulfur (wt%)")], color="#C9901A")
        product_chart("HPS CCR (ASTM D4530)", "wt%", [("HPS_CCR", "CCR (wt%)")], color="#C8A2C8")
    with c2:
        product_chart("HPS Density (ASTM D4052)", "g/cm³", [("HPS_Density", "Density")], color="#FF6B6B")
        product_chart("HPS Nitrogen (ASTM D5762)", "ppmw", [("HPS_Nitrogen", "Nitrogen (ppmw)")], color="#7B61FF")
        product_chart("HPS Sediment (ASTM D4870)", "wt%", [("HPS_Sediment", "Total Sediment (wt%)")], color="#FF9F43")

with tabs[1]:
    st.markdown(section_label("LTO Daily Properties"), unsafe_allow_html=True)
    product_table("LTO Product")
    c1, c2 = st.columns(2)
    with c1:
        product_chart("LTO API (ASTM D4052)", "API", [("LTO_API", "API")], color="#FFB800")
        product_chart("LTO Sulfur (ASTM D4294)", "wt%", [("LTO_Sulfur", "Sulfur (wt%)")], color="#C9901A")
    with c2:
        product_chart("LTO Density (ASTM D4052)", "g/cm³", [("LTO_Density", "Density")], color="#FF6B6B")
        product_chart("LTO Nitrogen (ASTM D5762)", "ppmw", [("LTO_Nitrogen", "Nitrogen (ppmw)")], color="#7B61FF")

with tabs[2]:
    st.markdown(section_label("ISV Daily Properties"), unsafe_allow_html=True)
    product_table("ISV Product")
    c1, c2 = st.columns(2)
    with c1:
        product_chart("ISV Sulfur (ASTM D4294)", "wt%", [("ISV_Sulfur", "Sulfur (wt%)")], color="#C9901A")
        product_chart("ISV Metals (Ni, V)", "ppm", [("ISV_Ni", "Ni (ppm)"), ("ISV_V", "V (ppm)")])
    with c2:
        product_chart("ISV 560+", "wt%", [("ISV_560plus", "560+ (wt%)")], color="#FFB800")
        product_chart("ISV Nitrogen (ASTM D5762)", "ppmw", [("ISV_Nitrogen", "Nitrogen (ppmw)")], color="#7B61FF")
        product_chart("ISV MCRT", "wt%", [("ISV_MCRT", "MCRT (wt%)")], color="#C8A2C8")








with tabs[3]:
    st.markdown(section_label("Gas Composition"), unsafe_allow_html=True)
    col_hg, col_lg = st.columns(2)
    with col_hg:
        st.markdown(section_label("High Gas"), unsafe_allow_html=True)
        product_table("High Gas")
        product_chart("High Gas H2 (ASTM D7833)", "mol%", [("HG_H2", "H2")], color="#C9901A")
        product_chart("High Gas C1-C3 (ASTM D7833)", "mol%", [("HG_C1", "C1"), ("HG_C2", "C2"), ("HG_C3", "C3")])
        product_chart("High Gas C4-C6+ & N2 (ASTM D7833)", "mol%", [("HG_C4", "C4"), ("HG_C5", "C5"), ("HG_C6plus", "C6+"), ("HG_N2", "N2")])
    with col_lg:
        st.markdown(section_label("Low Gas"), unsafe_allow_html=True)
        product_table("Low Gas")
        product_chart("Low Gas H2 (ASTM D7833)", "mol%", [("LG_H2", "H2")], color="#C9901A")
        product_chart("Low Gas C1-C3 (ASTM D7833)", "mol%", [("LG_C1", "C1"), ("LG_C2", "C2"), ("LG_C3", "C3")])
        product_chart("Low Gas C4-C6+ & N2 (ASTM D7833)", "mol%", [("LG_C4", "C4"), ("LG_C5", "C5"), ("LG_C6plus", "C6+"), ("LG_N2", "N2")])





