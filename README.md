# MEBU Analytics Platform

**Version:** 1.2.0
**Last Updated:** 2026-02-27
**Status:** ✅ Production-ready — Multi-phase VR Feed tracking + HPS/Product mapping
**GitHub Repository:** [TheSupremeAI/mebu-database](https://github.com/TheSupremeAI/mebu-database)
**Developer:** [TheSupremeAI](https://github.com/TheSupremeAI)

---

## Quick Start

```bash
cd "D:\Claude Project\MEBU Database"
streamlit run main.py
```

Open browser at `http://localhost:8501`

---

## Version History

### v1.2.0 — 2026-02-27 (Current)
**Multi-Phase VR Feed Tracking**

- **VR Feed Library**: New reusable feed recipe catalog — define named blends (e.g., ABQ3358 = Basrah Heavy 55% + Arab Medium 10% + Arab Light 35%) and reuse across experiments.
- **Phase Timeline Editor**: Each experiment can now have multiple phases with independent day ranges, VR feeds, and reactor temperatures (Rx-1/Rx-2/Rx-3). Replaces the old single VR blend + temperature editor.
- **Phase Bands on Charts**: When 2+ phases exist, colored vertical bands with neon labels appear on all Dashboard and Product Results charts showing feed boundaries.
- **Phase Summary Panel**: Dashboard now shows a phase card panel instead of the old VR blend donut.
- **CSV Export**: New export function in Settings — download phase data (VR names, compositions, temperatures) as CSV with preview table.
- **Chart Readability**: Larger chart titles (15px), brighter axis values, full-opacity neon phase labels.
- **Auto-Migration**: Existing experiments automatically converted to single-phase format on first run.

### v1.1.1 Hotfix — 2026-02-27
**Streamlit Cloud Deployment Fixes**
- **BOM Removal**: Stripped invisible UTF-8 BOM characters from `.streamlit/config.toml` to prevent `TomlDecodeError` during cloud server spin-ups.
- **Entry Point Reset**: Reverted application entry point back to strict lowercase `main.py` to satisfy Streamlit Cloud's default expectations.

### v1.1.0 UI — 2026-02-27
**Focused Storyteller luxury design**

- **New design identity**: Pure matte black (`#0E1117`) background with sharp `1px` high-contrast gold (`#C9901A`) borders.

- **Redesigned Quick Start**: Consolidated the monolithic gradient block into sleek, functional horizontal metric cards.
- **Chart refinement**: Stripped out grid lines and made Plotly chart backgrounds completely transparent. Brightened the trace palette with stark, neon colors (Molten Gold, Neon Pink, Cyan) for maximum readability against pure black.
- **Removed gradient noise**: Cleaned up the background CSS, eliminating the intrusive gold radial gradients for a stricter, professional data-dense look.

### v1.1.0 â€” 2026-02-27
**Header-Aware Mapping & Streamlined UI**

- **Synchronized Extraction**: Updated `utils/extractor.py` to be header-aware. It now validates "Day on stream" headers before pulling data, correctly handling early experiment stops.
- **HPS/Product Re-mapping**: Shifted all Product Distribution and Conversion parameters to strictly use the **F-AG** column range (HPS Properties) instead of Feed properties.
- **Precise Matching**: Search logic now prioritizes exact label matches (e.g., `"C7 AsConv,wt%"` and `"C5 AsConc, wt%"`) to prevent accidental overlap with reference rows.
- **Consolidated Dashboard**:
    - Merged all conversion metrics into a single **"CATALYTIC CONVERSION"** tab with a clean 2-column layout.
    - Simplified navigation to 3 core data tabs: `Cracking Conversion`, `CATALYTIC CONVERSION`, and `Flow & LHSV`.
    - Added **Total Sedimentation** to the primary Cracking tab.
- **Deep Field Styling**: Enhanced chart aesthetics with distinct colors (Molten Gold for Cracking, Coral for Sedimentation, etc.) and removed ART acceptance noise for a cleaner view.
- **History Sync**: Fully synchronized the History comparison page with the new Dashboard structure.
- **Database Reset**: Wiped old/duplicate records to allow for a clean re-import using the corrected 1.1.0 logic.

### v1.0.0 â€” 2026-02-27
**Initial build â€” Multi-page Streamlit + SQLite platform**

- Replaced single Excel workflow with centralized SQLite database.
- Built 4-page Streamlit app (Import, Dashboard, History, Settings).
- Smart name-based Excel extractor works across all experiment files.

---

## Project Structure

```
D:\Claude Project\MEBU Database\
â”‚
â”œâ”€â”€ MEBU_Analytics.exe              â† Double-click to launch
â”œâ”€â”€ main.py                         â† Streamlit entry point
â”œâ”€â”€ launcher.py                     â† Source code for .exe
â”‚
â”œâ”€â”€ pages/
â”‚   â”œâ”€â”€ 1_Import.py                 â† Load Excel files (Header-aware sync)
â”‚   â”œâ”€â”€ 2_Dashboard.py              â† Single experiment â€” Streamlined 3-tab view
â”‚   â”œâ”€â”€ 3_History.py                â† Cross-experiment overlay (Synced)
â”‚   â”œâ”€â”€ 4_Product_Results.py        â† Daily HPS, LTO, ISV & Gas results
â”‚   â””â”€â”€ 5_Settings.py               â† Edit metadata & database cleanup

â”‚
â”œâ”€â”€ utils/
â”‚   â”œâ”€â”€ db.py                       â† SQLite CRUD layer
â”‚   â”œâ”€â”€ extractor.py                â† Exact-match, header-aware extractor
â”‚   â””â”€â”€ charts.py                   â† Deep Field Plotly factory
â”‚
â”œâ”€â”€ mebu_analytics.sqlite           â† âš ï¸ Central database
...
```

---

## Parameter Keys Reference (v1.1.0)

| Key | Excel Label (Column C) | Range | Description |
|---|---|---|---|
| `CrkConv` | `CrkConv, wt%, As is` | F-AG | Primary Cracking Conversion |
| `Sedimentation` | `Sedimentation, ppm` | F-AG | Total Sedimentation |
| `NiConv` | `NiConv, wt%` | F-AG | Nickel Conversion |
| `VConv` | `VConv, wt%` | F-AG | Vanadium Conversion |
| `NiV_Conv` | `(Ni+V)Conv, wt%` | F-AG | Combined Ni+V Conversion |
| `SConv` | `SConv, wt%` | F-AG | Sulfur Conversion |
| `NConv` | `NConv, wt%` | F-AG | Nitrogen Conversion |
| `MCRConv` | `MCRConv, wt%` | F-AG | MCRT Conversion |
| `C7_AsphConv` | `C7 AsConv,wt%` | F-AG | C7 Asphaltenes Conversion |
| `C5_AsphConv` | `C5 AsConc, wt%` | F-AG | C5 Asphaltenes Conversion |
| `560plus_wt` | `560 plus` | F-AG | HPS Property: 560+ Result |

---

## Maintenance & Re-importing

**IMPORTANT:** Whenever the mapping logic in `utils/extractor.py` is updated, existing data should be refreshed:
1. Go to **âš™ï¸ Settings** â†’ **Delete** all old experiments.
2. Go to **ðŸ“¥ Import** â†’ **Re-import** the 4 Master Excel files.
3. This ensures all charts use the most accurate, synchronized data.

---

## Tech Stack

- **Python 3.x** (Pandas, Plotly, OpenPyxl, SQLite3)
- **Streamlit** (Multi-page UI)
- **Design System**: Deep Field Dark Luxury (JetBrains Mono + Rajdhani fonts)
