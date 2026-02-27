"""
MEBU Analytics — DEEP FIELD Design System (v1.2.0 - Ultra-Premium Edition)
Futuristic industrial luxury for petroleum engineers.
"""

MEBU_CSS = """
<style>
/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   FONTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;1,300&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&family=Inter:wght@300;400;500;600;700&display=swap');

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   DESIGN TOKENS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
:root {
  --void:          #030509;
  --abyss:         #070B14;
  --surface:       rgba(11, 20, 34, 0.7);
  --surface-opaque:#0B1422;
  --surface-2:     rgba(16, 29, 53, 0.8);
  --surface-3:     rgba(22, 38, 69, 0.85);
  --plasma:        #00F5D4;
  --plasma-dim:    rgba(0, 245, 212, 0.12);
  --plasma-glow:   rgba(0, 245, 212, 0.45);
  --plasma-faint:  rgba(0, 245, 212, 0.05);
  --gold:          #FFB800;
  --gold-dim:      rgba(255, 184, 0, 0.12);
  --gold-glow:     rgba(255, 184, 0, 0.45);
  --gold-faint:    rgba(255, 184, 0, 0.05);
  --violet:        #7B61FF;
  --coral:         #FF6B6B;
  --success:       #00F5A0;
  --danger:        #FF3D5A;
  --text:          #E2EAF3;
  --text-2:        #8AA4B8;
  --text-3:        #4A6278;
  --border:        rgba(0, 245, 212, 0.15);
  --border-2:      rgba(0, 245, 212, 0.25);
  --border-gold:   rgba(255, 184, 0, 0.22);
  --font-display:  'Rajdhani', sans-serif;
  --font-mono:     'JetBrains Mono', monospace;
  --font-body:     'Inter', sans-serif;
  --radius:        12px;
  --radius-sm:     4px;
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   GLOBAL RESET & BASE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
html, body, [class*="css"], .stApp {
  font-family: var(--font-body) !important;
  background-color: var(--void) !important;
  color: var(--text) !important;
}

/* Enhanced Animated Grid Background */
.stApp {
  background-color: var(--void) !important;
  background-image:
    linear-gradient(rgba(0,245,212,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,245,212,0.03) 1px, transparent 1px),
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(0,245,212,0.08) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 90% 100%, rgba(255,184,0,0.05) 0%, transparent 50%),
    radial-gradient(circle at 10% 20%, rgba(123, 97, 255, 0.03) 0%, transparent 40%) !important;
  background-size: 64px 64px, 64px 64px, 100% 100%, 100% 100%, 100% 100% !important;
  background-attachment: fixed !important;
}

/* Subtle moving noise texture */
.stApp::after {
  content: '';
  position: fixed;
  inset: -200%;
  background-image: url("https://www.transparenttextures.com/patterns/carbon-fibre.png");
  opacity: 0.03;
  pointer-events: none;
  z-index: 10000;
  animation: drift 60s linear infinite;
}

@keyframes drift {
  from { transform: translate(0,0); }
  to { transform: translate(10%, 10%); }
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   SIDEBAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
[data-testid="stSidebar"] {
  background: rgba(4, 7, 13, 0.95) !important;
  backdrop-filter: blur(20px) !important;
  border-right: 1px solid var(--border) !important;
  box-shadow: 10px 0 50px rgba(0,0,0,0.7) !important;
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   TYPOGRAPHY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
h1, h2, h3 { font-family: var(--font-display) !important; }

/* Custom "Glitch" Title Effect */
.glitch-title {
  position: relative;
  display: inline-block;
  font-family: var(--font-display) !important;
  text-transform: uppercase;
  letter-spacing: 4px;
  font-weight: 800;
  color: var(--text);
  text-shadow: 0 0 20px var(--plasma-glow);
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   METRIC CARDS (ULTRA REDESIGN)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
[data-testid="stMetric"] {
  background: var(--surface) !important;
  backdrop-filter: blur(12px) !important;
  border: 1px solid var(--border) !important;
  border-top: 3px solid var(--plasma) !important;
  border-radius: var(--radius) !important;
  padding: 24px 24px 20px !important;
  box-shadow: 0 4px 24px rgba(0,0,0,0.3) !important;
  transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
}

[data-testid="stMetric"]:hover {
  transform: translateY(-5px) !important;
  border-color: var(--plasma-glow) !important;
  box-shadow: 0 12px 40px rgba(0,0,0,0.5), 0 0 30px var(--plasma-dim) !important;
}

[data-testid="stMetricLabel"] > div {
  font-family: var(--font-display) !important;
  font-size: 0.8rem !important;
  font-weight: 700 !important;
  letter-spacing: 2.5px !important;
  color: var(--text-2) !important;
}

[data-testid="stMetricValue"] > div {
  font-family: var(--font-mono) !important;
  font-size: 2.2rem !important;
  font-weight: 600 !important;
  color: var(--plasma) !important;
  margin-top: 8px !important;
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ANIMATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
.stApp > .main {
  animation: reveal 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) both;
}

@keyframes reveal {
  from { opacity: 0; filter: blur(10px); transform: translateY(20px); }
  to { opacity: 1; filter: blur(0); transform: translateY(0); }
}

</style>
"""

def inject_css():
    """Call this at the top of every page to apply the MEBU Deep Field design system."""
    import streamlit as st
    st.markdown(MEBU_CSS, unsafe_allow_html=True)

def page_header(title: str, subtitle: str = "", icon: str = ""):
    """Render a styled page header."""
    icon_html = f'<span style="font-size:1.8rem;margin-right:16px;vertical-align:middle;filter:drop-shadow(0 0 10px var(--plasma-glow));">{icon}</span>' if icon else ""  
    sub_html = f'<p style="color:var(--text-2);font-family:var(--font-body);font-size:0.95rem;margin:8px 0 0;font-weight:400;letter-spacing:0.5px;">{subtitle}</p>' if subtitle else ""
    return f"""
    <div style="margin-bottom:40px; animation: reveal 0.6s ease both;">
      <h1 class="glitch-title" style="margin:0;line-height:1.2;font-size:2.2rem;">{icon_html}{title}</h1>
      {sub_html}
      <div style="height:3px;background:linear-gradient(90deg, var(--plasma), var(--violet), transparent);
                  margin-top:20px;border-radius:2px;box-shadow:0 0 15px var(--plasma-dim);"></div>
    </div>
    """

def glass_card(content_html: str, accent: str = "plasma", padding: str = "32px 36px"):
    """Render a glassmorphism card with high-end effects."""
    border_color = "var(--border-2)" if accent == "plasma" else "var(--border-gold)"
    top_color = "var(--plasma)" if accent == "plasma" else "var(--gold)"
    glow = "var(--plasma-glow)" if accent == "plasma" else "var(--gold-glow)"
    
    return f"""
    <div style="
      background:var(--surface);
      backdrop-filter:blur(20px);
      -webkit-backdrop-filter:blur(20px);
      border:1px solid {border_color};
      border-top:4px solid {top_color};
      border-radius:var(--radius);
      padding:{padding};
      box-shadow:0 12px 40px rgba(0,0,0,0.5);
      position:relative;
      overflow:hidden;
      transition:all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    " onmouseover="this.style.transform='translateY(-5px)';this.style.boxShadow='0 20px 60px rgba(0,0,0,0.6), 0 0 20px {glow}';"
      onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 12px 40px rgba(0,0,0,0.5)';"
    >
      <div style="
        position:absolute;top:0;right:0;width:150px;height:150px;
        background:radial-gradient(circle at top right,
          {'var(--plasma-dim)' if accent=='plasma' else 'var(--gold-dim)'},transparent 70%);
        pointer-events:none;
      "></div>
      <div style="position:absolute; top:12px; right:16px;">
        <div style="width:8px; height:8px; border-radius:50%; background:{top_color}; 
                    box-shadow:0 0 10px {top_color}; animation: blink 2s infinite;"></div>
      </div>
      {content_html}
    </div>
    <style>
      @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
    </style>
    """

def gradient_card(title: str, value: str, subtitle: str = "", accent: str = "plasma"):
    """Render a special high-emphasis card with a full gradient background."""
    grad = "linear-gradient(135deg, #004D44 0%, #001A16 100%)" if accent == "plasma" else "linear-gradient(135deg, #4D3800 0%, #1A1300 100%)"
    text_color = "var(--plasma)" if accent == "plasma" else "var(--gold)"
    
    return f"""
    <div style="
      background:{grad};
      border:1px solid {text_color}44;
      border-radius:var(--radius);
      padding:28px;
      box-shadow:0 10px 30px rgba(0,0,0,0.4);
      position:relative;
    ">
      <div style="font-family:var(--font-display);font-size:0.8rem;font-weight:700;
                  letter-spacing:3px;text-transform:uppercase;color:{text_color};
                  margin-bottom:10px;opacity:0.8;">{title}</div>
      <div style="font-family:var(--font-mono);font-size:2.4rem;font-weight:700;
                  color:white;text-shadow:0 0 15px {text_color}88;">{value}</div>
      <div style="font-family:var(--font-body);font-size:0.85rem;color:rgba(255,255,255,0.6);
                  margin-top:6px;">{subtitle}</div>
    </div>
    """

def temp_badge(label: str, value, unit: str = "°C"):
    """Render a reactor temperature badge."""
    if value is None or value == "—":
        return ""
    return f"""
    <span style="
      display:inline-flex;align-items:center;gap:8px;
      background:rgba(255, 184, 0, 0.08);border:1px solid var(--border-gold);
      border-radius:30px;padding:6px 18px;margin-right:10px;margin-bottom:8px;
      font-family:var(--font-mono);font-size:0.85rem;color:var(--gold);
      box-shadow:0 4px 12px rgba(0,0,0,0.2);
    ">
      <span style="width:8px;height:8px;background:var(--gold);
                   border-radius:50%;display:inline-block;
                   box-shadow:0 0 10px var(--gold-glow); animation: blink 3s infinite;"></span>
      {label}: <b style="font-weight:600;">{value}</b> {unit}
    </span>
    """

def section_label(text: str):
    """Render a section label in all-caps mono style."""
    return f"""
    <div style="
      font-family:var(--font-display);font-size:0.75rem;font-weight:700;
      letter-spacing:4px;text-transform:uppercase;color:var(--text-3);
      margin-bottom:16px;padding-bottom:10px;
      border-bottom:1px solid var(--border);
    ">⚡ {text}</div>
    """
