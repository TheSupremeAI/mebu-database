import streamlit as st
import pandas as pd
import os
import glob
import plotly.graph_objects as go

# --- CONFIGURATION ---
DATA_DIR = r"D:\Claude Project\MEBU Database\EXPERIMENT DATA"
st.set_page_config(page_title="MEBU Experiment Dashboard", layout="wide")

st.title("MEBU Experiment Data Dashboard")
st.markdown("Track and visualize 28-day pilot plant operations. The graphs below mirror the 'Lab result summary'.")

# --- SIDEBAR: File Selection & Inputs ---
st.sidebar.header("1. Select Experiment Data")
excel_files = glob.glob(os.path.join(DATA_DIR, "*.xlsx"))
file_names = [os.path.basename(f) for f in excel_files]

if not file_names:
    st.error(f"No Excel files found in {DATA_DIR}")
    st.stop()

selected_file = st.sidebar.selectbox("Experiment File:", file_names)
file_path = os.path.join(DATA_DIR, selected_file)

st.sidebar.markdown("---")
st.sidebar.header("2. Experiment Parameters")
vr_name = st.sidebar.text_input("Name of VR:", value="ABQ3358")
vr_usage = st.sidebar.number_input("% Usage of VR:", min_value=0.0, max_value=100.0, value=100.0, step=1.0)

st.sidebar.subheader("Temperatures (°C)")
rx1_temp = st.sidebar.number_input("Rx-1 Temp:", value=400.0, step=1.0)
rx2_temp = st.sidebar.number_input("Rx-2 Temp:", value=405.0, step=1.0)
rx3_temp = st.sidebar.number_input("Rx-3 Temp:", value=410.0, step=1.0)

# --- DATA PARSING ---
@st.cache_data
def load_data(path):
    try:
        df = pd.read_excel(path, sheet_name="Master Template")
    except Exception as e:
        return None, str(e)
    
    day_row_idx = None
    for idx, val in df.iloc[:, 2].items():
        if pd.notna(val) and "Day on stream" in str(val):
            day_row_idx = idx
            break
            
    if day_row_idx is None:
        return None, "Could not find 'Day on stream' row to align data."
        
    var_col = df.columns[2]
    data_cols = df.columns[5:33] # 28 columns
    
    clean_df = df[[var_col] + list(data_cols)].copy()
    clean_df.rename(columns={var_col: "Variable"}, inplace=True)
    clean_df.dropna(subset=["Variable"], inplace=True)
    
    day_mapping = {col: f"Day {i+1}" for i, col in enumerate(data_cols)}
    clean_df.rename(columns=day_mapping, inplace=True)
    
    clean_df["Variable"] = clean_df["Variable"].astype(str).str.strip()
    return clean_df, None

def main():
    st.markdown("### Loading Data...")
    with st.spinner("Extracting Master Template..."):
        df_clean, err = load_data(file_path)

    if err or df_clean is None:
        st.error(f"Error loading data: {err}")
        st.stop()
        return

    # --- MAIN DASHBOARD: Visualization ---
    st.markdown("### 3. Lab Result Summary Visualization")

    all_vars = [v for v in df_clean["Variable"].unique() if v and v != "nan" and "-->" not in v]

    # Create sub-tabs to mirror the individual charts in the Lab Result Summary Excel sheet
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Conversions", "Asphaltenes & MCRT", "Sulfur & Nitrogen", "Metals (Ni+V)", "Custom Plot"
    ])

    def create_plot(title, target_vars):
        fig = go.Figure()
        found_any = False
        
        for var in target_vars:
            if var in all_vars:
                found_any = True
                row_data = df_clean[df_clean["Variable"] == var].iloc[0]
                y_values = row_data[1:29].values.tolist()
                
                fig.add_trace(go.Scatter(
                    x=list(range(1, 29)), 
                    y=y_values, 
                    mode='lines+markers',
                    name=var
                ))
                
        if found_any:
            fig.update_layout(
                title=title,
                xaxis_title="Day on Stream",
                yaxis_title="Value",
                template="plotly_white",
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"None of the target variables ({target_vars}) were found in the data for this chart.")

    # TAB 1: Conversions
    with tab1:
        create_plot("560+ and Cracking", [
            "560 Plus, g/h", 
            "560 plus, TOP acceptance'Dec24", 
            "560plus, MEBU25002",
            "560 plus, ART, acceptance"
        ])

    # TAB 2: Asphaltenes & MCRT
    with tab2:
        create_plot("Asphaltenes & MCRT", [
            "C7 Asphaltene, wt%", 
            "C7 Asphaltene, wt%, ART, Acceptance",
            "C5 Asphaltene, wt%",
            "MCRT, wt%",
            "MCRT, wt%, ART, Acceptance"
        ])

    # TAB 3: Sulfur & Nitrogen
    with tab3:
        create_plot("Sulfur & Nitrogen", [
            "S, wt% (ASTM D4294)", 
            "S, wt%, ART Acceptance",
            "N, wt% (ASTM D5762)",
            "N, ppm, ART, Acceptance"
        ])

    # TAB 4: Metals (Ni+V)
    with tab4:
        create_plot("Metals (Ni+V)", [
            "Ni, ppm",
            "Ni, ppm, ART, Acceptance",
            "V, ppm",
            "V, ppm, ART, Acceptance",
            "Total(Ni+V), g/h"
        ])

    # TAB 5: Custom Plot
    with tab5:
        selected_vars = st.multiselect("Select Variables to Plot manually:", all_vars)
        if selected_vars:
            create_plot("Custom Selection", selected_vars)
        else:
            st.info("Please select at least one variable to plot.")

    # Show raw data table below
    with st.expander("View Raw Data Table"):
        st.dataframe(df_clean)

    # Show the explicit inputs provided by the user in a summary card
    st.markdown("---")
    st.markdown("### Current Run Parameters")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("VR Name", vr_name)
    col2.metric("VR Usage (%)", f"{vr_usage}%")
    col3.metric("Rx-1 Temp", f"{rx1_temp} °C")
    col4.metric("Rx-2 Temp", f"{rx2_temp} °C")
    col5.metric("Rx-3 Temp", f"{rx3_temp} °C")

if __name__ == "__main__":
    main()
