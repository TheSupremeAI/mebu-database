# MEBU Analytics Platform

**Version:** 1.1.0
**Last Updated:** 2026-02-27
**Status:** ✅ Production-ready — System re-mapped to HPS/Product properties

---

## Quick Start

```bash
cd "D:\Claude Project\MEBU Database"
streamlit run main.py
```

Open browser at `http://localhost:8501`

---

## Version History

### v1.1.0 — 2026-02-27 (Current)
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

### v1.0.0 — 2026-02-27
**Initial build — Multi-page Streamlit + SQLite platform**

- Replaced single Excel workflow with centralized SQLite database.
- Built 4-page Streamlit app (Import, Dashboard, History, Settings).
- Smart name-based Excel extractor works across all experiment files.

---

## Project Structure

```
D:\Claude Project\MEBU Database\
│
├── MEBU_Analytics.exe              ← Double-click to launch
├── main.py                         ← Streamlit entry point
├── launcher.py                     ← Source code for .exe
│
├── pages/
│   ├── 1_Import.py                 ← Load Excel files (Header-aware sync)
│   ├── 2_Dashboard.py              ← Single experiment — Streamlined 3-tab view
│   ├── 3_History.py                ← Cross-experiment overlay (Synced)
│   ├── 4_Product_Results.py        ← Daily HPS, LTO, ISV & Gas results
│   └── 5_Settings.py               ← Edit metadata & database cleanup

│
├── utils/
│   ├── db.py                       ← SQLite CRUD layer
│   ├── extractor.py                ← Exact-match, header-aware extractor
│   └── charts.py                   ← Deep Field Plotly factory
│
├── mebu_analytics.sqlite           ← ⚠️ Central database
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
1. Go to **⚙️ Settings** → **Delete** all old experiments.
2. Go to **📥 Import** → **Re-import** the 4 Master Excel files.
3. This ensures all charts use the most accurate, synchronized data.

---

## Tech Stack

- **Python 3.x** (Pandas, Plotly, OpenPyxl, SQLite3)
- **Streamlit** (Multi-page UI)
- **Design System**: Deep Field Dark Luxury (JetBrains Mono + Rajdhani fonts)
