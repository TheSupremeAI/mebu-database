# Petroleum Luxury UI Redesign Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform the MEBU Analytics Platform from Deep Field teal/dark to a Petroleum Luxury aesthetic — obsidian backgrounds, molten gold accents, Playfair Display editorial typography, IBM Plex Mono data font, gold shimmer animations, and noise texture depth.

**Architecture:** Single `utils/styles.py` overhaul provides global CSS (fonts, colors, animations, component overrides), then each page file gets a targeted `<style>` block for tabs, sidebar, inputs, and buttons. `utils/charts.py` gets a parallel palette/layout update so charts match the new identity.

**Tech Stack:** Streamlit `st.markdown(unsafe_allow_html=True)`, Plotly `go.Figure`, Google Fonts (Playfair Display + Rajdhani + IBM Plex Mono), CSS custom properties, `@keyframes`

---

## Design Tokens Reference

```
--void:          #05050A
--abyss:         #0A0A0F
--surface:       rgba(14,12,20,0.88)
--surface-2:     rgba(22,18,32,0.92)
--gold:          #C9901A   ← primary accent
--gold-bright:   #E8A82A   ← hover / active
--gold-dim:      rgba(201,144,26,0.12)
--gold-glow:     rgba(201,144,26,0.35)
--gold-border:   rgba(201,144,26,0.22)
--gold-border-b: rgba(201,144,26,0.50)
--platinum:      #E8E4D9   ← h1/h2 text
--text:          #C8C0B0   ← body text
--text-2:        #7A7060   ← secondary
--text-3:        #4A4438   ← tertiary / labels
--border:        rgba(201,144,26,0.18)
--font-display:  'Playfair Display', serif
--font-ui:       'Rajdhani', sans-serif
--font-mono:     'IBM Plex Mono', monospace
--radius:        10px
```

## Plotly Chart Tokens

```python
PAPER_BG   = "#06050A"
PLOT_BG    = "#0C0A12"
GRID_COLOR = "rgba(201,144,26,0.06)"
ZERO_LINE  = "rgba(201,144,26,0.14)"
PALETTE = [
    "#C9901A",  # molten gold      (primary)
    "#E8E4D9",  # platinum
    "#D4793A",  # burnt amber
    "#A87848",  # raw sienna
    "#7A9AAA",  # steel blue-grey
    "#C8A878",  # sand
    "#8A7060",  # dark umber
    "#E8C860",  # pale gold
]
```

---

## Task 1: Overhaul `utils/styles.py`

**File:** Modify `D:\Claude Project\MEBU Database\utils\styles.py`

**Step 1: Replace the entire file contents**

Replace `utils/styles.py` with the following:

```python
"""
MEBU Analytics — Petroleum Luxury Design System (v2.0)
Obsidian backgrounds, molten gold accents, editorial serif typography.
"""

MEBU_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Rajdhani:wght@300;400;500;600;700&family=IBM+Plex+Mono:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
  --void:          #05050A;
  --abyss:         #0A0A0F;
  --surface:       rgba(14,12,20,0.88);
  --surface-2:     rgba(22,18,32,0.92);
  --surface-3:     rgba(30,26,44,0.95);
  --gold:          #C9901A;
  --gold-bright:   #E8A82A;
  --gold-dim:      rgba(201,144,26,0.12);
  --gold-glow:     rgba(201,144,26,0.35);
  --gold-border:   rgba(201,144,26,0.22);
  --gold-border-b: rgba(201,144,26,0.50);
  --platinum:      #E8E4D9;
  --text:          #C8C0B0;
  --text-2:        #7A7060;
  --text-3:        #4A4438;
  --border:        rgba(201,144,26,0.18);
  --font-display:  'Playfair Display', serif;
  --font-ui:       'Rajdhani', sans-serif;
  --font-mono:     'IBM Plex Mono', monospace;
  --radius:        10px;
}

/* ── Reset & Base ─────────────────────────────────────────────────────── */
html, body, [class*="css"], .stApp {
  font-family: var(--font-ui) !important;
  background-color: var(--void) !important;
  color: var(--text) !important;
}

/* ── Background: obsidian + noise + gold radial + dot grid ─────────────── */
.stApp {
  background-color: var(--void) !important;
  background-image:
    url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E"),
    radial-gradient(ellipse 70% 45% at 50% 0%, rgba(201,144,26,0.07) 0%, transparent 65%),
    radial-gradient(circle 2px at center, rgba(201,144,26,0.04) 0%, transparent 100%);
  background-size: 200px 200px, 100% 100%, 38px 38px !important;
  background-attachment: fixed !important;
}

/* ── Page entry animation ──────────────────────────────────────────────── */
.stApp > .main {
  animation: luxReveal 0.9s cubic-bezier(0.16,1,0.3,1) both;
}

@keyframes luxReveal {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Scrollbar ─────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--void); }
::-webkit-scrollbar-thumb { background: rgba(201,144,26,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(201,144,26,0.55); }

/* ── Sidebar ────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: rgba(5,4,9,0.97) !important;
  backdrop-filter: blur(24px) !important;
  border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"]::before {
  content: '';
  display: block;
  height: 3px;
  background: linear-gradient(90deg, var(--gold), var(--gold-bright), transparent);
  margin-bottom: 4px;
}

[data-testid="stSidebar"] h3 {
  font-family: var(--font-display) !important;
  color: var(--platinum) !important;
  font-size: 1.05rem !important;
  letter-spacing: 0.5px !important;
  font-style: italic !important;
}

/* ── Metric cards ───────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
  background: var(--surface) !important;
  backdrop-filter: blur(16px) !important;
  border: 1px solid var(--gold-border) !important;
  border-left: 3px solid var(--gold) !important;
  border-radius: var(--radius) !important;
  padding: 22px 24px !important;
  box-shadow: 0 4px 28px rgba(0,0,0,0.45), inset 0 1px 0 rgba(201,144,26,0.08) !important;
  transition: all 0.35s cubic-bezier(0.16,1,0.3,1) !important;
  animation: cardReveal 0.7s cubic-bezier(0.16,1,0.3,1) both;
}

[data-testid="stMetric"]:nth-child(1) { animation-delay: 0.05s; }
[data-testid="stMetric"]:nth-child(2) { animation-delay: 0.10s; }
[data-testid="stMetric"]:nth-child(3) { animation-delay: 0.15s; }
[data-testid="stMetric"]:nth-child(4) { animation-delay: 0.20s; }

@keyframes cardReveal {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

[data-testid="stMetric"]:hover {
  transform: translateY(-4px) !important;
  border-left-color: var(--gold-bright) !important;
  box-shadow: 0 16px 48px rgba(0,0,0,0.6), 0 0 24px var(--gold-dim) !important;
}

[data-testid="stMetricLabel"] > div {
  font-family: var(--font-ui) !important;
  font-size: 0.72rem !important;
  font-weight: 700 !important;
  letter-spacing: 2.5px !important;
  color: var(--text-2) !important;
  text-transform: uppercase !important;
}

[data-testid="stMetricValue"] > div {
  font-family: var(--font-mono) !important;
  font-size: 2rem !important;
  color: var(--gold-bright) !important;
  letter-spacing: -0.5px !important;
}

/* ── Tabs ───────────────────────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
}

[data-testid="stTabs"] [role="tab"] {
  font-family: var(--font-ui) !important;
  font-weight: 600 !important;
  font-size: 0.78rem !important;
  letter-spacing: 2px !important;
  text-transform: uppercase !important;
  color: var(--text-2) !important;
  border: none !important;
  border-bottom: 2px solid transparent !important;
  padding: 10px 20px !important;
  transition: all 0.25s ease !important;
}

[data-testid="stTabs"] [role="tab"]:hover {
  color: var(--gold) !important;
  border-bottom-color: rgba(201,144,26,0.3) !important;
}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  color: var(--gold-bright) !important;
  border-bottom: 2px solid var(--gold) !important;
  background: linear-gradient(to bottom, rgba(201,144,26,0.05), transparent) !important;
}

/* ── Dataframe ──────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  overflow: hidden !important;
}

/* ── Buttons ────────────────────────────────────────────────────────────── */
[data-testid="stButton"] > button[kind="primary"] {
  background: linear-gradient(135deg, #8A5F10 0%, var(--gold) 50%, var(--gold-bright) 100%) !important;
  border: none !important;
  color: #05050A !important;
  font-family: var(--font-ui) !important;
  font-weight: 700 !important;
  letter-spacing: 2.5px !important;
  text-transform: uppercase !important;
  font-size: 0.8rem !important;
  border-radius: var(--radius) !important;
  box-shadow: 0 4px 20px rgba(201,144,26,0.35) !important;
  transition: all 0.3s ease !important;
}

[data-testid="stButton"] > button[kind="primary"]:hover {
  box-shadow: 0 8px 32px rgba(201,144,26,0.55) !important;
  transform: translateY(-2px) !important;
}

[data-testid="stButton"] > button[kind="secondary"] {
  background: transparent !important;
  border: 1px solid var(--gold-border) !important;
  color: var(--gold) !important;
  font-family: var(--font-ui) !important;
  font-weight: 600 !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  font-size: 0.78rem !important;
  border-radius: var(--radius) !important;
  transition: all 0.25s ease !important;
}

[data-testid="stButton"] > button[kind="secondary"]:hover {
  background: var(--gold-dim) !important;
  border-color: var(--gold) !important;
}

/* ── Inputs & Selects ───────────────────────────────────────────────────── */
[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div {
  background: rgba(14,12,20,0.9) !important;
  border-color: var(--border) !important;
  border-radius: var(--radius) !important;
  font-family: var(--font-mono) !important;
  color: var(--text) !important;
}

[data-baseweb="input"] > div:focus-within,
[data-baseweb="textarea"] > div:focus-within {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 2px var(--gold-dim) !important;
}

[data-baseweb="select"] > div {
  background: rgba(14,12,20,0.9) !important;
  border-color: var(--border) !important;
  border-radius: var(--radius) !important;
  font-family: var(--font-ui) !important;
  color: var(--text) !important;
}

/* ── Expanders ──────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  background: var(--surface) !important;
}

[data-testid="stExpander"] summary {
  font-family: var(--font-ui) !important;
  font-weight: 600 !important;
  letter-spacing: 1px !important;
  color: var(--text) !important;
}

/* ── Alert / info boxes ─────────────────────────────────────────────────── */
[data-testid="stAlert"] {
  border-radius: var(--radius) !important;
  font-family: var(--font-ui) !important;
}

/* ── HR ─────────────────────────────────────────────────────────────────── */
hr {
  border-color: var(--border) !important;
  margin: 32px 0 !important;
}

/* ── Gold shimmer keyframe (applied to header via page_header) ───────────── */
@keyframes goldShimmer {
  0%   { background-position: -200% center; }
  100% { background-position: 200% center; }
}

@keyframes borderGlow {
  0%, 100% { box-shadow: 0 0 12px rgba(201,144,26,0.15); }
  50%       { box-shadow: 0 0 28px rgba(201,144,26,0.35); }
}
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(MEBU_CSS, unsafe_allow_html=True)


def page_header(title, subtitle="", icon=""):
    icon_html = (
        f'<span style="font-size:1.6rem;margin-right:14px;vertical-align:middle;'
        f'opacity:0.85;">{icon}</span>'
    ) if icon else ""

    sub_html = (
        f'<p style="color:var(--text-2);font-size:0.88rem;margin:10px 0 0;'
        f'font-family:var(--font-ui);font-weight:400;letter-spacing:0.5px;">'
        f'{subtitle}</p>'
    ) if subtitle else ""

    return f"""
    <div style="margin-bottom:44px;">
      <h1 style="
        font-family:var(--font-display);
        font-size:2.4rem;
        font-weight:700;
        font-style:italic;
        letter-spacing:0.5px;
        margin:0;
        background: linear-gradient(90deg,
          var(--platinum) 0%,
          var(--gold-bright) 40%,
          var(--platinum) 60%,
          var(--gold) 80%,
          var(--platinum) 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: goldShimmer 5s linear infinite;
      ">{icon_html}{title}</h1>
      {sub_html}
      <div style="
        height:1px;
        background:linear-gradient(90deg, var(--gold), rgba(201,144,26,0.3), transparent);
        margin-top:20px;
        position:relative;
      ">
        <div style="
          position:absolute;left:0;top:-1px;
          width:60px;height:3px;
          background:linear-gradient(90deg, var(--gold-bright), var(--gold));
          border-radius:2px;
        "></div>
      </div>
    </div>
    """


def glass_card(content_html, accent="gold", padding="32px 36px"):
    color = "var(--gold)" if accent == "gold" else "var(--platinum)"
    return f"""
    <div style="
      background:var(--surface);
      backdrop-filter:blur(20px);
      border:1px solid var(--gold-border);
      border-top:3px solid {color};
      border-radius:var(--radius);
      padding:{padding};
      box-shadow:0 12px 48px rgba(0,0,0,0.55), inset 0 1px 0 rgba(201,144,26,0.07);
      position:relative;overflow:hidden;
    ">
      <div style="
        position:absolute;top:0;right:0;
        width:220px;height:220px;
        background:radial-gradient(circle at top right,rgba(201,144,26,0.05),transparent 65%);
        pointer-events:none;
      "></div>
      {content_html}
    </div>
    """


def temp_badge(label, value, unit="°C"):
    if value is None or value == "—":
        return ""
    return (
        f'<span style="'
        f'background:rgba(201,144,26,0.08);'
        f'border:1px solid rgba(201,144,26,0.3);'
        f'border-radius:20px;padding:5px 16px;margin:4px 4px 4px 0;'
        f'color:var(--gold-bright);'
        f'font-family:var(--font-mono);font-size:0.82rem;'
        f'display:inline-block;'
        f'">{label}: <b>{value}</b>{unit}</span>'
    )


def section_label(text):
    return (
        f'<div style="'
        f'font-family:var(--font-ui);font-size:0.68rem;font-weight:700;'
        f'letter-spacing:3px;text-transform:uppercase;'
        f'color:var(--text-3);margin-bottom:14px;'
        f'border-bottom:1px solid rgba(201,144,26,0.12);'
        f'padding-bottom:8px;'
        f'">{text}</div>'
    )


def gold_badge(text, color="gold"):
    c = "var(--gold-bright)" if color == "gold" else "var(--platinum)"
    bg = "rgba(201,144,26,0.1)" if color == "gold" else "rgba(232,228,217,0.08)"
    border = "rgba(201,144,26,0.3)" if color == "gold" else "rgba(232,228,217,0.2)"
    return (
        f'<span style="'
        f'background:{bg};border:1px solid {border};'
        f'border-radius:4px;padding:3px 10px;'
        f'color:{c};font-family:var(--font-ui);'
        f'font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;'
        f'">{text}</span>'
    )
```

**Step 2: Verify the app loads without errors**

```bash
cd "D:\Claude Project\MEBU Database"
streamlit run main.py
```

Expected: App loads at `http://localhost:8501` with gold shimmer header, obsidian background, gold metric cards — no Python errors in terminal.

---

## Task 2: Update `utils/charts.py` palette and layout

**File:** Modify `D:\Claude Project\MEBU Database\utils\charts.py`

**Step 1: Replace PALETTE, PAPER_BG, PLOT_BG, GRID_COLOR, ZERO_LINE, and BASE_LAYOUT**

Replace lines 8–68 (everything from `PALETTE = [` through the closing `)`  of `BASE_LAYOUT = dict(...)`) with:

```python
PALETTE = [
    "#C9901A",  # molten gold      (primary)
    "#E8E4D9",  # platinum
    "#D4793A",  # burnt amber
    "#A87848",  # raw sienna
    "#7A9AAA",  # steel blue-grey
    "#C8A878",  # sand
    "#8A7060",  # dark umber
    "#E8C860",  # pale gold
]

PAPER_BG   = "#06050A"
PLOT_BG    = "#0C0A12"
GRID_COLOR = "rgba(201,144,26,0.06)"
ZERO_LINE  = "rgba(201,144,26,0.14)"

BASE_LAYOUT = dict(
    paper_bgcolor=PAPER_BG,
    plot_bgcolor=PLOT_BG,
    font=dict(
        color="#7A7060",
        family="'IBM Plex Mono', monospace",
        size=11,
    ),
    xaxis=dict(
        gridcolor=GRID_COLOR,
        zerolinecolor=ZERO_LINE,
        zerolinewidth=1,
        tickfont=dict(size=10, color="#5A4A38", family="'IBM Plex Mono', monospace"),
        title_font=dict(size=11, color="#7A6A50", family="'Rajdhani', sans-serif"),
        linecolor="rgba(201,144,26,0.1)",
        linewidth=1,
        showgrid=True,
    ),
    yaxis=dict(
        gridcolor=GRID_COLOR,
        zerolinecolor=ZERO_LINE,
        zerolinewidth=1,
        tickfont=dict(size=10, color="#5A4A38", family="'IBM Plex Mono', monospace"),
        title_font=dict(size=11, color="#7A6A50", family="'Rajdhani', sans-serif"),
        linecolor="rgba(201,144,26,0.1)",
        linewidth=1,
        showgrid=True,
    ),
    legend=dict(
        bgcolor="rgba(6,5,10,0.88)",
        bordercolor="rgba(201,144,26,0.2)",
        borderwidth=1,
        font=dict(size=10, color="#7A7060", family="'IBM Plex Mono', monospace"),
        orientation="h",
        yanchor="bottom", y=1.02,
        xanchor="right", x=1,
    ),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="#100E18",
        bordercolor="rgba(201,144,26,0.45)",
        font=dict(color="#C8C0B0", size=11, family="'IBM Plex Mono', monospace"),
    ),
    margin=dict(l=54, r=20, t=52, b=44),
)
```

Also update `_base_fig` title font (line ~78):
```python
    layout["title"] = dict(
        text=title.upper(),
        font=dict(
            size=12, color="#7A6A50",
            family="'Rajdhani', sans-serif",
        ),
        x=0.01, y=0.97,
    )
```

Also update `_add_art_band` fill and line colors (replace all `rgba(0,245,212,…)` references):
```python
    fig.add_trace(go.Scatter(
        ...
        fillcolor="rgba(201,144,26,0.05)",
        line=dict(color="rgba(201,144,26,0.22)", width=1, dash="dot"),
        name="ART ACCEPTANCE",
        ...
    ))
    # Top limit line
    fig.add_trace(go.Scatter(
        ...
        line=dict(color="rgba(201,144,26,0.18)", width=1, dash="dot"),
        ...
    ))
    # Bottom limit line
    fig.add_trace(go.Scatter(
        ...
        line=dict(color="rgba(201,144,26,0.18)", width=1, dash="dot"),
        ...
    ))
```

Also update `vr_blend_donut` center annotation and text font (replace all `#00F5D4` references):
```python
    fig.update_layout(
        ...
        font=dict(color="#C8C0B0", family="'IBM Plex Mono', monospace"),
        ...
        annotations=[dict(
            text="<b>VR<br>BLEND</b>",
            x=0.5, y=0.5,
            font=dict(
                size=12, color="#C9901A",
                family="'Rajdhani', sans-serif",
            ),
            showarrow=False,
        )],
    )
```

**Step 2: Verify charts render**

Open Dashboard page and check that charts show gold grid lines, gold palette first series, and platinum/amber secondary series. No console errors.

---

## Task 3: Update `main.py` — home page cards and version badge

**File:** Modify `D:\Claude Project\MEBU Database\main.py`

**Step 1: Fix version badge** (line 38)

Change:
```python
col4.metric("Platform Version", "v1.0")
```
To:
```python
col4.metric("Platform Version", "v1.1")
```

**Step 2: Update the Quick Start Guide card colors**

In the inline HTML block (lines 42–107), replace all `var(--plasma)` references with `var(--gold)`, replace `var(--plasma-faint)` with `var(--gold-dim)`, replace `var(--border-2)` with `var(--gold-border)`, replace `var(--violet)` and `rgba(123,97,255,…)` with `var(--text-2)` and `rgba(122,112,96,0.12)` / `rgba(122,112,96,0.2)`.

Specifically replace these strings across the main.py inline HTML:
- `color:var(--plasma)` → `color:var(--gold)`
- `background:var(--plasma-faint)` → `background:var(--gold-dim)`
- `border:1px solid var(--border-2)` → `border:1px solid var(--gold-border)`
- `color:var(--violet)` → `color:var(--text-2)`
- `background:rgba(123,97,255,0.08)` → `background:rgba(122,112,96,0.1)`
- `border:1px solid rgba(123,97,255,0.2)` → `border:1px solid rgba(122,112,96,0.2)`
- `border-top:2px solid var(--plasma)` → `border-top:2px solid var(--gold)`
- `radial-gradient(circle at top right,rgba(0,245,212,0.06)` → `radial-gradient(circle at top right,rgba(201,144,26,0.06)`

**Step 3: Verify home page looks correct**

Open `http://localhost:8501` — metrics show gold left-border, quick-start guide shows gold step numbers, all teal remnants gone.

---

## Task 4: Update `pages/1_Import.py` — replace plasma with gold

**File:** Modify `D:\Claude Project\MEBU Database\pages\1_Import.py`

**Step 1: Update glass_card call** (line 58–76)

In the "HOW TO IMPORT" glass card HTML, replace:
- `color:var(--plasma)` → `color:var(--gold)`
- `color:var(--plasma);font-family` → `color:var(--gold);font-family`

**Step 2: Add targeted tab + input CSS after `inject_css()`** (after line 19)

Add immediately after `inject_css()`:

```python
st.markdown("""
<style>
[data-testid="stFileUploader"] {
  border: 1px solid var(--gold-border) !important;
  border-radius: var(--radius) !important;
  background: var(--surface) !important;
}
label[data-testid="stWidgetLabel"] > div > p {
  font-family: var(--font-ui) !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  color: var(--text-2) !important;
}
</style>
""", unsafe_allow_html=True)
```

---

## Task 5: Update `pages/2_Dashboard.py` — replace plasma with gold

**File:** Modify `D:\Claude Project\MEBU Database\pages\2_Dashboard.py`

**Step 1: Update experiment record card** (lines 56–101)

In the experiment record card HTML, replace:
- `border-top:2px solid var(--plasma)` → `border-top:2px solid var(--gold)`
- `color:var(--plasma);margin-bottom:12px` → `color:var(--gold);margin-bottom:12px`
- `radial-gradient(circle at top right,var(--plasma-faint)` → `radial-gradient(circle at top right,var(--gold-dim)`
- `color:var(--plasma);">` (the measurements count line) → `color:var(--gold);">`

**Step 2: Update "NO VR BLEND SET" card** (lines 109–117)

No teal references here — leave as is.

---

## Task 6: Update `pages/3_History.py` — experiment legend cards

**File:** Modify `D:\Claude Project\MEBU Database\pages\3_History.py`

**Step 1: The legend cards** already use `color` from `PALETTE` (which will now be gold-toned) — no changes needed to color references. The cards use `{color}25`, `{color}10`, etc. which will auto-update.

**Step 2: Verify overlay**

Open History page, select 2+ experiments — legend cards should show gold/amber palette per run.

---

## Task 7: Update `pages/4_Product_Results.py` — chart colors

**File:** Modify `D:\Claude Project\MEBU Database\pages\4_Product_Results.py`

**Step 1: Replace all hardcoded `"#00F5D4"` color values** with `"#C9901A"` (gold).

Replace in file (there are ~8 occurrences across product_chart calls):
```python
color="#00F5D4"  →  color="#C9901A"
```

Replace section headers (lines 99, 113, 127, 142):
```python
st.markdown("### HPS Daily Properties")
```
With luxury styled version using `section_label`:
```python
from utils.styles import inject_css, page_header, section_label
# (already imported)
st.markdown(section_label("HPS Daily Properties"), unsafe_allow_html=True)
st.markdown(section_label("LTO Daily Properties"), unsafe_allow_html=True)
st.markdown(section_label("ISV Daily Properties"), unsafe_allow_html=True)
```

For the Gas tab, replace:
```python
st.markdown("#### High Gas")
st.markdown("#### Low Gas")
```
With:
```python
st.markdown(section_label("High Gas"), unsafe_allow_html=True)
st.markdown(section_label("Low Gas"), unsafe_allow_html=True)
```

---

## Task 8: Update `pages/5_Settings.py` — replace plasma with gold

**File:** Modify `D:\Claude Project\MEBU Database\pages\5_Settings.py`

**Step 1: Update database records badge** (lines 37–46)

Replace:
```python
  <span style="font-family:var(--font-display);font-size:0.68rem;font-weight:600;
    letter-spacing:2px;text-transform:uppercase;color:var(--text-2);">Database records</span>
  <span style="font-family:var(--font-mono);font-size:1rem;color:var(--plasma);
    font-weight:500;">{n_meas:,}</span>
```
With:
```python
  <span style="font-family:var(--font-ui);font-size:0.68rem;font-weight:700;
    letter-spacing:2px;text-transform:uppercase;color:var(--text-2);">Database records</span>
  <span style="font-family:var(--font-mono);font-size:1rem;color:var(--gold-bright);
    font-weight:500;">{n_meas:,}</span>
```

**Step 2: Danger zone section label** (line 156)

Change:
```python
st.markdown(section_label("⚠ Danger Zone"), unsafe_allow_html=True)
```
No change needed — `section_label` will render with gold styling automatically.

---

## Task 9: Final verification — full app walkthrough

**Step 1: Run the app**

```bash
cd "D:\Claude Project\MEBU Database"
streamlit run main.py
```

**Checklist:**
- [ ] Home: gold shimmer on "MEBU Analytics Platform" header, obsidian background with noise, gold metric cards with left-border
- [ ] Import: gold accent section labels, gold primary button glow
- [ ] Dashboard: gold experiment record card, charts use gold/amber palette, tabs have gold underline on active
- [ ] History: legend cards use gold/amber per experiment
- [ ] Product Results: gold chart accents, section labels styled
- [ ] Settings: gold badge on record count, gold VR blend preview cards

**Step 2: Update README.md version notes**

Add a `### v2.0` entry to the README noting the design system change:
```
### v1.1.0 UI — 2026-02-27 (Design)
**Petroleum Luxury Design System**
- Replaced Deep Field teal with Obsidian + Molten Gold palette
- New fonts: Playfair Display (headers) + IBM Plex Mono (data)
- Gold shimmer animation on page headers
- Updated chart palette to gold/amber tones
```

---

## Execution Notes

- No git repository — save before each task, test after each file change
- Streamlit auto-reloads on file save — watch the browser for errors
- If a page shows a Python error, check for unterminated strings in the HTML blocks
- CSS changes in `styles.py` apply globally — test all pages after Task 1
