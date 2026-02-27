"""
MEBU Analytics — DEEP FIELD Design System
Futuristic industrial luxury for petroleum engineers.
"""

MEBU_CSS = """
<style>
/* ═══════════════════════════════════════════════════════════════
   FONTS
═══════════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;1,300&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

/* ═══════════════════════════════════════════════════════════════
   DESIGN TOKENS
═══════════════════════════════════════════════════════════════ */
:root {
  --void:          #04060D;
  --abyss:         #080D1A;
  --surface:       #0B1422;
  --surface-2:     #101D35;
  --surface-3:     #162645;
  --plasma:        #00F5D4;
  --plasma-dim:    rgba(0,245,212,0.12);
  --plasma-glow:   rgba(0,245,212,0.35);
  --plasma-faint:  rgba(0,245,212,0.05);
  --gold:          #FFB800;
  --gold-dim:      rgba(255,184,0,0.12);
  --gold-glow:     rgba(255,184,0,0.35);
  --gold-faint:    rgba(255,184,0,0.05);
  --violet:        #7B61FF;
  --coral:         #FF6B6B;
  --success:       #00F5A0;
  --danger:        #FF3D5A;
  --text:          #C8DCF0;
  --text-2:        #6A8CAA;
  --text-3:        #334A62;
  --border:        rgba(0,245,212,0.10);
  --border-2:      rgba(0,245,212,0.20);
  --border-gold:   rgba(255,184,0,0.18);
  --font-display:  'Rajdhani', sans-serif;
  --font-mono:     'JetBrains Mono', monospace;
  --font-body:     'DM Sans', sans-serif;
  --radius:        6px;
  --radius-sm:     3px;
}

/* ═══════════════════════════════════════════════════════════════
   GLOBAL RESET & BASE
═══════════════════════════════════════════════════════════════ */
html, body, [class*="css"], .stApp {
  font-family: var(--font-body) !important;
  background-color: var(--void) !important;
  color: var(--text) !important;
}

/* Animated circuit grid background */
.stApp {
  background-color: var(--void) !important;
  background-image:
    linear-gradient(rgba(0,245,212,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,245,212,0.025) 1px, transparent 1px),
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(0,245,212,0.06) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 90% 100%, rgba(255,184,0,0.04) 0%, transparent 50%) !important;
  background-size: 48px 48px, 48px 48px, 100% 100%, 100% 100% !important;
  background-attachment: fixed !important;
}

/* Scanline overlay */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent 0px,
    transparent 3px,
    rgba(0,0,0,0.04) 3px,
    rgba(0,0,0,0.04) 4px
  );
  pointer-events: none;
  z-index: 9999;
}

/* ═══════════════════════════════════════════════════════════════
   SCROLLBAR
═══════════════════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--abyss); }
::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, var(--plasma), var(--violet));
  border-radius: 2px;
}
::-webkit-scrollbar-thumb:hover { background: var(--plasma); }

/* ═══════════════════════════════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, var(--abyss) 0%, #060B15 100%) !important;
  border-right: 1px solid var(--border) !important;
  box-shadow: 4px 0 40px rgba(0,0,0,0.6) !important;
}
[data-testid="stSidebar"]::before {
  content: '';
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 2px;
  background: linear-gradient(180deg, transparent, var(--plasma), var(--gold), transparent);
  animation: sidebarPulse 4s ease infinite;
}
@keyframes sidebarPulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
  font-family: var(--font-display) !important;
  color: var(--plasma) !important;
  letter-spacing: 2px;
  text-transform: uppercase;
  font-size: 0.8rem !important;
}

/* ═══════════════════════════════════════════════════════════════
   TYPOGRAPHY
═══════════════════════════════════════════════════════════════ */
h1, h2, h3 { font-family: var(--font-display) !important; }

.stMarkdown h1 {
  font-family: var(--font-display) !important;
  font-weight: 700 !important;
  letter-spacing: 3px !important;
  text-transform: uppercase;
  color: var(--text) !important;
  font-size: 2rem !important;
}
.stMarkdown h2 {
  font-family: var(--font-display) !important;
  font-weight: 600 !important;
  letter-spacing: 2px !important;
  text-transform: uppercase;
  color: var(--plasma) !important;
  font-size: 1.1rem !important;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border);
}
.stMarkdown h3 {
  font-family: var(--font-display) !important;
  font-weight: 500 !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase;
  color: var(--text-2) !important;
  font-size: 0.85rem !important;
}
p, li, div { font-family: var(--font-body) !important; }
code, pre, [class*="mono"] { font-family: var(--font-mono) !important; }

/* ═══════════════════════════════════════════════════════════════
   METRIC CARDS
═══════════════════════════════════════════════════════════════ */
@keyframes scanPulse {
  0%   { transform: translateX(-100%); opacity: 0; }
  20%  { opacity: 1; }
  80%  { opacity: 1; }
  100% { transform: translateX(200%); opacity: 0; }
}
@keyframes borderGlow {
  0%, 100% { box-shadow: 0 0 12px var(--plasma-dim), inset 0 0 12px var(--plasma-faint); }
  50% { box-shadow: 0 0 24px var(--plasma-glow), inset 0 0 24px var(--plasma-dim); }
}
[data-testid="stMetric"] {
  background: linear-gradient(135deg, var(--surface) 0%, var(--surface-2) 100%) !important;
  border: 1px solid var(--border) !important;
  border-top: 2px solid var(--plasma) !important;
  border-radius: var(--radius) !important;
  padding: 20px 20px 16px !important;
  position: relative !important;
  overflow: hidden !important;
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease !important;
  cursor: default;
}
[data-testid="stMetric"]::before {
  content: '';
  position: absolute;
  top: 0; left: -60%; width: 60%;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(0,245,212,0.9), transparent);
  animation: scanPulse 3s ease-in-out infinite;
}
[data-testid="stMetric"]::after {
  content: '';
  position: absolute;
  bottom: 0; right: 0;
  width: 40px; height: 40px;
  background: radial-gradient(circle, var(--plasma-dim), transparent 70%);
  border-radius: 50%;
}
[data-testid="stMetric"]:hover {
  transform: translateY(-3px) !important;
  border-color: var(--border-2) !important;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5), 0 0 20px var(--plasma-dim) !important;
}
[data-testid="stMetricLabel"] > div {
  font-family: var(--font-display) !important;
  font-size: 0.72rem !important;
  font-weight: 600 !important;
  letter-spacing: 2px !important;
  text-transform: uppercase !important;
  color: var(--text-2) !important;
}
[data-testid="stMetricValue"] > div {
  font-family: var(--font-mono) !important;
  font-size: 1.7rem !important;
  font-weight: 500 !important;
  color: var(--plasma) !important;
  letter-spacing: -0.5px;
}
[data-testid="stMetricDelta"] {
  font-family: var(--font-mono) !important;
  font-size: 0.75rem !important;
}

/* ═══════════════════════════════════════════════════════════════
   TABS
═══════════════════════════════════════════════════════════════ */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 2px !important;
  padding-bottom: 0 !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
  font-family: var(--font-display) !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  color: var(--text-3) !important;
  background: transparent !important;
  border: none !important;
  padding: 10px 18px !important;
  border-radius: var(--radius-sm) var(--radius-sm) 0 0 !important;
  transition: color 0.2s ease, background 0.2s ease !important;
  position: relative;
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {
  color: var(--text-2) !important;
  background: var(--plasma-faint) !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
  color: var(--plasma) !important;
  background: var(--plasma-faint) !important;
  border-bottom: 2px solid var(--plasma) !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
  background: var(--plasma) !important;
  height: 2px !important;
}

/* ═══════════════════════════════════════════════════════════════
   BUTTONS
═══════════════════════════════════════════════════════════════ */
button[kind="primary"], [data-testid="baseButton-primary"] {
  font-family: var(--font-display) !important;
  font-size: 0.85rem !important;
  font-weight: 700 !important;
  letter-spacing: 2px !important;
  text-transform: uppercase !important;
  background: linear-gradient(135deg, #00D4B8, #00F5D4) !important;
  color: var(--void) !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  padding: 10px 28px !important;
  position: relative !important;
  overflow: hidden !important;
  transition: all 0.25s ease !important;
  box-shadow: 0 4px 20px rgba(0,245,212,0.3) !important;
}
button[kind="primary"]:hover, [data-testid="baseButton-primary"]:hover {
  box-shadow: 0 6px 30px rgba(0,245,212,0.5), 0 0 60px rgba(0,245,212,0.15) !important;
  transform: translateY(-2px) !important;
}
button[kind="secondary"], [data-testid="baseButton-secondary"] {
  font-family: var(--font-display) !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  background: transparent !important;
  color: var(--plasma) !important;
  border: 1px solid var(--border-2) !important;
  border-radius: var(--radius-sm) !important;
  padding: 8px 20px !important;
  transition: all 0.25s ease !important;
}
button[kind="secondary"]:hover, [data-testid="baseButton-secondary"]:hover {
  background: var(--plasma-faint) !important;
  border-color: var(--plasma-glow) !important;
  box-shadow: 0 0 20px var(--plasma-dim) !important;
}

/* ═══════════════════════════════════════════════════════════════
   INPUTS & SELECTS
═══════════════════════════════════════════════════════════════ */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
  font-family: var(--font-mono) !important;
  font-size: 0.9rem !important;
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text) !important;
  padding: 10px 14px !important;
  transition: all 0.2s ease !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
  border-color: var(--plasma) !important;
  box-shadow: 0 0 0 2px var(--plasma-dim), 0 0 20px var(--plasma-faint) !important;
  background: var(--surface-2) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label {
  font-family: var(--font-display) !important;
  font-size: 0.72rem !important;
  font-weight: 600 !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  color: var(--text-2) !important;
}
[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label {
  font-family: var(--font-display) !important;
  font-size: 0.72rem !important;
  font-weight: 600 !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  color: var(--text-2) !important;
}
[data-baseweb="select"] > div {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.88rem !important;
  transition: border-color 0.2s ease !important;
}
[data-baseweb="select"] > div:focus-within {
  border-color: var(--plasma) !important;
  box-shadow: 0 0 0 2px var(--plasma-dim) !important;
}
[data-baseweb="popover"] {
  background: var(--surface-2) !important;
  border: 1px solid var(--border-2) !important;
  border-radius: var(--radius) !important;
  box-shadow: 0 16px 48px rgba(0,0,0,0.8) !important;
}
[data-baseweb="menu"] li {
  font-family: var(--font-mono) !important;
  font-size: 0.85rem !important;
  color: var(--text-2) !important;
  background: transparent !important;
}
[data-baseweb="menu"] li:hover {
  background: var(--plasma-faint) !important;
  color: var(--plasma) !important;
}
[data-baseweb="tag"] {
  background: var(--plasma-dim) !important;
  border: 1px solid var(--border-2) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--plasma) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.78rem !important;
}

/* Textarea */
[data-testid="stTextArea"] textarea {
  font-family: var(--font-mono) !important;
  font-size: 0.85rem !important;
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text) !important;
  transition: all 0.2s ease !important;
}
[data-testid="stTextArea"] textarea:focus {
  border-color: var(--plasma) !important;
  box-shadow: 0 0 0 2px var(--plasma-dim) !important;
}
[data-testid="stTextArea"] label {
  font-family: var(--font-display) !important;
  font-size: 0.72rem !important;
  font-weight: 600 !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  color: var(--text-2) !important;
}

/* ═══════════════════════════════════════════════════════════════
   DATAFRAME / TABLE
═══════════════════════════════════════════════════════════════ */
[data-testid="stDataFrame"] {
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  overflow: hidden !important;
  font-family: var(--font-mono) !important;
  font-size: 0.82rem !important;
}
[data-testid="stDataFrame"] th {
  font-family: var(--font-display) !important;
  font-size: 0.72rem !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  color: var(--plasma) !important;
  background: var(--surface-2) !important;
}

/* ═══════════════════════════════════════════════════════════════
   EXPANDER
═══════════════════════════════════════════════════════════════ */
[data-testid="stExpander"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
}
[data-testid="stExpander"] summary {
  font-family: var(--font-display) !important;
  font-size: 0.82rem !important;
  font-weight: 600 !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  color: var(--text-2) !important;
  padding: 14px 18px !important;
}
[data-testid="stExpander"] summary:hover { color: var(--plasma) !important; }

/* ═══════════════════════════════════════════════════════════════
   ALERTS & INFO BOXES
═══════════════════════════════════════════════════════════════ */
[data-testid="stAlert"] {
  border-radius: var(--radius-sm) !important;
  border: 1px solid var(--border) !important;
  border-left: 3px solid var(--plasma) !important;
  background: var(--plasma-faint) !important;
  font-family: var(--font-body) !important;
  font-size: 0.88rem !important;
}
[data-testid="stAlert"][data-type="warning"] {
  border-left-color: var(--gold) !important;
  background: var(--gold-faint) !important;
}
[data-testid="stAlert"][data-type="error"] {
  border-left-color: var(--danger) !important;
  background: rgba(255,61,90,0.05) !important;
}
[data-testid="stAlert"][data-type="success"] {
  border-left-color: var(--success) !important;
  background: rgba(0,245,160,0.05) !important;
}

/* ═══════════════════════════════════════════════════════════════
   SPINNER
═══════════════════════════════════════════════════════════════ */
[data-testid="stSpinner"] > div {
  border-top-color: var(--plasma) !important;
}

/* ═══════════════════════════════════════════════════════════════
   PLOTLY CHART CONTAINER
═══════════════════════════════════════════════════════════════ */
[data-testid="stPlotlyChart"] {
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  background: var(--surface) !important;
  overflow: hidden !important;
  transition: border-color 0.3s ease !important;
}
[data-testid="stPlotlyChart"]:hover {
  border-color: var(--border-2) !important;
}

/* ═══════════════════════════════════════════════════════════════
   DIVIDER
═══════════════════════════════════════════════════════════════ */
hr {
  border: none !important;
  height: 1px !important;
  background: linear-gradient(90deg, transparent, var(--border-2), transparent) !important;
  margin: 24px 0 !important;
}

/* ═══════════════════════════════════════════════════════════════
   CAPTION / SMALL TEXT
═══════════════════════════════════════════════════════════════ */
[data-testid="stCaptionContainer"] {
  font-family: var(--font-mono) !important;
  font-size: 0.75rem !important;
  color: var(--text-3) !important;
}

/* ═══════════════════════════════════════════════════════════════
   MAIN CONTENT AREA
═══════════════════════════════════════════════════════════════ */
.main .block-container {
  padding-top: 32px !important;
  padding-bottom: 64px !important;
  max-width: 1400px !important;
}

/* ═══════════════════════════════════════════════════════════════
   ANIMATIONS
═══════════════════════════════════════════════════════════════ */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes glowPulse {
  0%, 100% { text-shadow: 0 0 20px var(--plasma-glow); }
  50%       { text-shadow: 0 0 40px var(--plasma-glow), 0 0 80px var(--plasma-dim); }
}
@keyframes borderRotate {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.stApp > .main {
  animation: fadeInUp 0.5s ease both;
}
</style>
"""


def inject_css():
    """Call this at the top of every page to apply the MEBU Deep Field design system."""
    import streamlit as st
    st.markdown(MEBU_CSS, unsafe_allow_html=True)


# ── Reusable HTML components ──────────────────────────────────────────────────

def page_header(title: str, subtitle: str = "", icon: str = ""):
    """Render a styled page header."""
    icon_html = f'<span style="font-size:1.6rem;margin-right:14px;vertical-align:middle;">{icon}</span>' if icon else ""
    sub_html = f'<p style="color:var(--text-2);font-family:var(--font-body);font-size:0.92rem;margin:6px 0 0;font-weight:300;">{subtitle}</p>' if subtitle else ""
    return f"""
    <div style="margin-bottom:28px;">
      <h1 style="
        font-family:var(--font-display);font-weight:700;font-size:1.8rem;
        letter-spacing:3px;text-transform:uppercase;color:var(--text);
        margin:0;line-height:1.2;
      ">{icon_html}{title}</h1>
      {sub_html}
      <div style="height:2px;background:linear-gradient(90deg,var(--plasma),var(--gold),transparent);
                  margin-top:14px;border-radius:1px;"></div>
    </div>
    """


def stat_card(label: str, value: str, unit: str = "", accent: str = "plasma"):
    """Render an inline stat card (use inside st.markdown)."""
    color = "var(--plasma)" if accent == "plasma" else "var(--gold)"
    return f"""
    <div style="
      background:var(--surface);border:1px solid var(--border);
      border-top:2px solid {color};border-radius:var(--radius);
      padding:16px 20px;position:relative;overflow:hidden;
    ">
      <div style="font-family:var(--font-display);font-size:0.68rem;font-weight:600;
                  letter-spacing:2px;text-transform:uppercase;color:var(--text-2);
                  margin-bottom:8px;">{label}</div>
      <div style="font-family:var(--font-mono);font-size:1.5rem;font-weight:500;
                  color:{color};">{value}<span style="font-size:0.8rem;color:var(--text-2);
                  margin-left:6px;">{unit}</span></div>
    </div>
    """


def glass_card(content_html: str, accent: str = "plasma", padding: str = "24px 28px"):
    """Render a glassmorphism card."""
    border_color = "var(--border-2)" if accent == "plasma" else "var(--border-gold)"
    top_color = "var(--plasma)" if accent == "plasma" else "var(--gold)"
    return f"""
    <div style="
      background:linear-gradient(135deg,var(--surface) 0%,var(--surface-2) 100%);
      border:1px solid {border_color};border-top:2px solid {top_color};
      border-radius:var(--radius);padding:{padding};
      box-shadow:0 8px 32px rgba(0,0,0,0.4);
      position:relative;overflow:hidden;
      transition:box-shadow 0.3s ease;
    ">
      <div style="
        position:absolute;top:0;right:0;width:120px;height:120px;
        background:radial-gradient(circle at top right,
          {'var(--plasma-faint)' if accent=='plasma' else 'var(--gold-faint)'},transparent 70%);
        pointer-events:none;
      "></div>
      {content_html}
    </div>
    """


def temp_badge(label: str, value, unit: str = "°C"):
    """Render a reactor temperature badge."""
    if value is None or value == "—":
        return ""
    return f"""
    <span style="
      display:inline-flex;align-items:center;gap:6px;
      background:var(--surface-2);border:1px solid var(--border-gold);
      border-radius:20px;padding:5px 16px;margin-right:8px;margin-bottom:6px;
      font-family:var(--font-mono);font-size:0.8rem;color:var(--gold);
    ">
      <span style="width:6px;height:6px;background:var(--gold);
                   border-radius:50%;display:inline-block;
                   box-shadow:0 0 8px var(--gold-glow);"></span>
      {label}: {value} {unit}
    </span>
    """


def section_label(text: str):
    """Render a section label in all-caps mono style."""
    return f"""
    <div style="
      font-family:var(--font-display);font-size:0.7rem;font-weight:700;
      letter-spacing:3px;text-transform:uppercase;color:var(--text-3);
      margin-bottom:12px;padding-bottom:8px;
      border-bottom:1px solid var(--border);
    ">{text}</div>
    """
