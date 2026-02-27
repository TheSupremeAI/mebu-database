# Frontend Redesign: The "Focused Storyteller" (Dark Luxury Bloomberg)
Date: 2026-02-27

## Objective
Upgrade the MEBU Analytics Platform Streamlit UI to a high-density, ultra-premium data layout. The goal is to maximize data visibility without overwhelming the user, utilizing a pure dark mode with gold and high-contrast accents akin to a modern trading terminal.

## Core Aesthetic (Global Styling)
- **Background:** Flat matte black (`#0E1117` or `#131722`) rather than grayish gradients to maximize data contrast and readability.
- **Borders & Accents:** Razor-sharp 1px gold lines (`rgba(201,144,26,0.3)`) overriding default thick Streamlit component borders. Interactive elements (tabs, buttons) feature sharp gold glows on hover.
- **Typography:** 
    - `JetBrains Mono` strictly enforced for numerical indicators, metrics, and data tables.
    - `Rajdhani` used for section headers to maintain an industrial, technical feel.

## Layout & Components

### 1. Navigation & Home Page (`main.py`)
- Minimized sidebar visual weight.
- Current HTML `<div>` Quick Start instructions refactored into clickable, Streamlit metric-style cards resembling a physical control panel.
- Enhanced dataframe rendering for "Loaded Experiments" with custom CSS to appear as a high-end trading ledger instead of default Streamlit white tables.

### 2. High-Density Dashboard Data (The "Summary Ribbon")
- Applied to pages `2_Dashboard.py` and `4_Product_Results.py`.
- **Top Ribbon:** A sticky row of 4-5 core `st.metric()` components positioned above all charts (e.g., Cracking Conversion, Sedimentation).
- **Styling:** CSS overrides on Streamlit's `st.metric()` to remove rounded corners, set pure black backgrounds, and feature bright gold monospaced text for instant readability.

### 3. Charting Architecture (Tabbed Full-Width)
- Utilize `st.tabs(["Cracking", "Catalytic", "Flow"])` to segregate primary data categories.
- Ensures all Plotly charts receive 100% block width (`use_container_width=True`), avoiding squished laptop layouts while retaining terminal-like focus on the active data stream.

### 4. Plotly Chart Styling Upgrades (`utils/charts.py`)
- Removing gridlines.
- Transparent chart and paper backgrounds (`rgba(0,0,0,0)`).
- Applying harsh, high-contrast neon trace colors (Cyber Yellow, Neon Coral) that contrast starkly against the `#0E1117` app background.

## Compatibility & Safety
This design relies exclusively on native Streamlit layout capabilities (`st.columns`, `st.tabs`, `st.metric`) and Plotly Python API (`fig.update_layout`). All "Luxury" aesthetics are achieved entirely through CSS overrides inserted via `st.markdown(..., unsafe_allow_html=True)`, ensuring stability across different environments and monitor sizes without breaking Streamlit's native reactive bindings.
