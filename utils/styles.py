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
  --surface:       #0E1117;
  --surface-2:     #131722;
  --surface-3:     #1B202F;
  --gold:          #C9901A;
  --gold-bright:   #E8A82A;
  --gold-dim:      rgba(201,144,26,0.12);
  --gold-glow:     rgba(201,144,26,0.35);
  --gold-border:   rgba(201,144,26,0.3);
  --gold-border-b: rgba(201,144,26,0.50);
  --platinum:      #F0EDE6;
  --text:          #DDD8CE;
  --text-2:        #A89C8C;
  --text-3:        #706050;
  --border:        rgba(201,144,26,0.3);
  --font-display:  'Playfair Display', serif;
  --font-ui:       'Rajdhani', sans-serif;
  --font-mono:     'IBM Plex Mono', monospace;
  --radius:        2px;
}

/* ── Reset & Base ─────────────────────────────────────────────────────── */
html, body, [class*="css"], .stApp {
  font-family: var(--font-ui) !important;
  background-color: var(--void) !important;
  color: var(--text) !important;
}

/* ── Background: obsidian + noise + dot grid ─────────────── */
.stApp {
  background-color: var(--void) !important;
  background-image:
    url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E"),
    radial-gradient(circle 2px at center, rgba(201,144,26,0.04) 0%, transparent 100%);
  background-size: 200px 200px, 38px 38px !important;
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
  border: 1px solid var(--gold-border) !important;
  border-radius: var(--radius) !important;
  padding: 16px 20px !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.45) !important;
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
/* ── Multiselect tags — dark background, readable text ────────────────────── */
span[data-baseweb="tag"] {
  background-color: rgba(201,144,26,0.2) !important;
  border: 1px solid rgba(201,144,26,0.35) !important;
  color: #E8DDD0 !important;
}
span[data-baseweb="tag"] span { color: #E8DDD0 !important; }
span[data-baseweb="tag"] svg { fill: #C9901A !important; }

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
