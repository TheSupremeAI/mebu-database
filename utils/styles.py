"""
MEBU Analytics — DEEP FIELD Design System (v1.2.2)
High-end industrial luxury for petroleum engineers.
"""

MEBU_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;1,300&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --void:          #030509;
  --abyss:         #070B14;
  --surface:       rgba(11, 20, 34, 0.7);
  --surface-2:     rgba(16, 29, 53, 0.8);
  --plasma:        #00F5D4;
  --plasma-dim:    rgba(0, 245, 212, 0.12);
  --plasma-glow:   rgba(0, 245, 212, 0.45);
  --gold:          #FFB800;
  --gold-glow:     rgba(255, 184, 0, 0.45);
  --text:          #E2EAF3;
  --text-2:        #8AA4B8;
  --text-3:        #4A6278;
  --border:        rgba(0, 245, 212, 0.15);
  --font-display:  'Rajdhani', sans-serif;
  --font-mono:     'JetBrains Mono', monospace;
  --font-body:     'Inter', sans-serif;
  --radius:        12px;
}

html, body, [class*="css"], .stApp {
  font-family: var(--font-body) !important;
  background-color: var(--void) !important;
  color: var(--text) !important;
}

.stApp {
  background-image:
    linear-gradient(rgba(0,245,212,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,245,212,0.03) 1px, transparent 1px),
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(0,245,212,0.08) 0%, transparent 60%) !important;
  background-size: 64px 64px, 64px 64px, 100% 100% !important;
  background-attachment: fixed !important;
}

[data-testid="stSidebar"] {
  background: rgba(4, 7, 13, 0.95) !important;
  backdrop-filter: blur(20px) !important;
  border-right: 1px solid var(--border) !important;
}

[data-testid="stMetric"] {
  background: var(--surface) !important;
  backdrop-filter: blur(12px) !important;
  border: 1px solid var(--border) !important;
  border-top: 3px solid var(--plasma) !important;
  border-radius: var(--radius) !important;
  padding: 24px !important;
  box-shadow: 0 4px 24px rgba(0,0,0,0.3) !important;
  transition: all 0.3s ease !important;
}

[data-testid="stMetric"]:hover {
  transform: translateY(-5px) !important;
  box-shadow: 0 12px 40px rgba(0,0,0,0.5), 0 0 20px var(--plasma-dim) !important;
}

[data-testid="stMetricLabel"] > div {
  font-family: var(--font-display) !important;
  font-size: 0.8rem !important;
  font-weight: 700 !important;
  letter-spacing: 2px !important;
  color: var(--text-2) !important;
  text-transform: uppercase !important;
}

[data-testid="stMetricValue"] > div {
  font-family: var(--font-mono) !important;
  font-size: 2.2rem !important;
  color: var(--plasma) !important;
}

.stApp > .main {
  animation: reveal 0.8s ease both;
}

@keyframes reveal {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
"""

def inject_css():
    import streamlit as st
    st.markdown(MEBU_CSS, unsafe_allow_html=True)

def page_header(title, subtitle="", icon=""):
    icon_html = f'<span style="font-size:1.8rem;margin-right:16px;vertical-align:middle;">{icon}</span>' if icon else ""
    sub_html = f'<p style="color:var(--text-2);font-size:0.95rem;margin:8px 0 0;">{subtitle}</p>' if subtitle else ""
    return f"""
    <div style="margin-bottom:40px;">
      <h1 style="font-family:var(--font-display);letter-spacing:3px;text-transform:uppercase;margin:0;font-size:2.2rem;">{icon_html}{title}</h1>
      {sub_html}
      <div style="height:3px;background:linear-gradient(90deg, var(--plasma), #7B61FF, transparent);margin-top:20px;"></div>
    </div>
    """

def glass_card(content_html, accent="plasma", padding="32px 36px"):
    color = "var(--plasma)" if accent == "plasma" else "var(--gold)"
    return f"""
    <div style="
      background:var(--surface);
      backdrop-filter:blur(20px);
      border:1px solid var(--border);
      border-top:4px solid {color};
      border-radius:var(--radius);
      padding:{padding};
      box-shadow:0 12px 40px rgba(0,0,0,0.5);
    ">
      {content_html}
    </div>
    """

def temp_badge(label, value, unit="°C"):
    if value is None or value == "—": return ""
    return f'<span style="background:rgba(255,184,0,0.1);border:1px solid var(--gold);border-radius:20px;padding:5px 15px;margin:5px;color:var(--gold);font-family:var(--font-mono);font-size:0.85rem;">{label}: <b>{value}</b>{unit}</span>'

def section_label(text):
    return f'<div style="font-family:var(--font-display);font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--text-3);margin-bottom:15px;border-bottom:1px solid var(--border);">{text}</div>'
