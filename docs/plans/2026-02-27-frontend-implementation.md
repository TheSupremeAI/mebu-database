# Frontend Redesign Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Implement the "Focused Storyteller" design upgrade across the MEBU Analytics Streamlit app, improving data density, contrast, and layout.

**Architecture:** 
- Update global CSS in `utils/styles.py` to use pure matte black and sharp 1px gold borders instead of gradients.
- Redesign the `main.py` quick start instructions using Streamlit columns and styled HTML cards.
- Refactor `pages/2_Dashboard.py` and `pages/4_Product_Results.py` to include a top "Summary Ribbon" of `st.metric` components.
- Update `utils/charts.py` to strip gridlines and use stark, high-contrast Plotly trace colors over a transparent background.

**Tech Stack:** Python, Streamlit, Plotly, HTML/CSS

---

### Task 1: Update Global CSS and Design Tokens

**Files:**
- Modify: `utils/styles.py`

**Step 1: Write minimal implementation**
Modify `utils/styles.py` to change the CSS variables for the color palette, metric cards, and layout elements to the new pure black/sharp gold aesthetic.
- Update `--surface` to `rgba(14,17,23,1.0)`
- Eliminate rounded thick borders in favor of `border: 1px solid var(--gold-border)`
- Remove the gradient and replace with pure matte black in `.stApp`
- Adjust `stMetric` styling to pure black, no rounding

**Step 2: Run test to verify it passes**
Run: `streamlit run main.py` in the background and manually verify the app loads without Python syntax errors.
Expected: PASS (No Crash)
*Note: We cannot write conventional unit tests for Streamlit UI CSS injection.*

**Step 3: Commit**
```bash
git add utils/styles.py
git commit -m "style: update global CSS tokens to pure black and sharp gold borders"
```

---

### Task 2: Redesign Navigation & Home Page

**Files:**
- Modify: `main.py`

**Step 1: Write minimal implementation**
Refactor the "QUICK START GUIDE" in `main.py` (lines 41-107). Instead of the large gradient box, split it into two horizontal rows of two `st.columns()` each, displaying sleek HTML boxes for Import, Dashboard, History, and Settings.
Apply custom HTML/CSS to the "Loaded Experiments" table to give it a high-end trading ledger style or rely on the new global CSS.

**Step 2: Run test to verify it passes**
Run: `python -m py_compile main.py`
Expected: PASS (No Syntax Errors)

**Step 3: Commit**
```bash
git add main.py
git commit -m "feat: redesign main page quick start guide to horizontal metric cards"
```

---

### Task 3: Upgrade Plotly Charts

**Files:**
- Modify: `utils/charts.py`

**Step 1: Write minimal implementation**
Modify `utils/charts.py`:
- Set `PAPER_BG` and `PLOT_BG` to `"rgba(0,0,0,0)"`.
- In `BASE_LAYOUT`, set `xaxis.showgrid=False` and `yaxis.showgrid=False`.
- Update `PALETTE` to use high-contrast neon colors to stand out against black.

**Step 2: Run test to verify it passes**
Run: `python -m py_compile utils/charts.py`
Expected: PASS

**Step 3: Commit**
```bash
git add utils/charts.py
git commit -m "style: remove chart gridlines and make backgrounds transparent"
```

---

### Task 4: Add Summary Ribbon to Dashboard

**Files:**
- Modify: `pages/2_Dashboard.py`

**Step 1: Write minimal implementation**
In `pages/2_Dashboard.py`, directly beneath the Run Metadata (around line 122), add a `st.columns(4)` ribbon displaying the most critical metrics using `st.metric()`:
- Cracking Conversion (wt%)
- Total Sedimentation (ppm)
- Sulfur Conversion (wt%)
- LHSV Actual (hr⁻¹)
Calculate these values by grabbing the most recent measurement value (highest `day`) for each parameter.

**Step 2: Run test to verify it passes**
Run: `python -m py_compile pages/2_Dashboard.py`
Expected: PASS

**Step 3: Commit**
```bash
git add pages/2_Dashboard.py
git commit -m "feat: add top summary ribbon to dashboard page"
```

---

### Task 5: Add Summary Ribbon to Product Results

**Files:**
- Modify: `pages/4_Product_Results.py`

**Step 1: Write minimal implementation**
In `pages/4_Product_Results.py` (around line 52), add a similar `st.columns(4)` ribbon displaying key product metrics:
- HPS API
- HPS Sulfur
- LTO Density
- ISV 560+
Calculate these by grabbing the most recent measurement value for those keys.

**Step 2: Run test to verify it passes**
Run: `python -m py_compile pages/4_Product_Results.py`
Expected: PASS

**Step 3: Commit**
```bash
git add pages/4_Product_Results.py
git commit -m "feat: add top summary ribbon to product results page"
```
