"""
MEBU Analytics — DEEP FIELD Chart Factory
Plotly charts tuned to the Deep Field design system.
"""
import plotly.graph_objects as go

# ── Palette (mirrors CSS design tokens) ───────────────────────────────────────
PALETTE = [
    "#C9901A",  # molten gold
    "#FFB800",  # bright neon gold
    "#FF6B6B",  # bright neon pink/red
    "#7B61FF",  # neon purple
    "#00D2D3",  # cyan
    "#FF9F43",  # orange
    "#C8A2C8",  # lilac
    "#A8C878",  # lime
]

PAPER_BG   = "rgba(0,0,0,0)"
PLOT_BG    = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(201,144,26,0.06)"
ZERO_LINE  = "rgba(201,144,26,0.14)"

BASE_LAYOUT = dict(
    paper_bgcolor=PAPER_BG,
    plot_bgcolor=PLOT_BG,
    font=dict(
        color="#A89C8C",
        family="'IBM Plex Mono', monospace",
        size=11,
    ),
    xaxis=dict(
        gridcolor=GRID_COLOR,
        zerolinecolor=ZERO_LINE,
        zerolinewidth=1,
        tickfont=dict(size=11, color="#C8B8A8", family="'IBM Plex Mono', monospace"),
        title_font=dict(size=12, color="#D0C4B4", family="'Rajdhani', sans-serif"),
        linecolor="rgba(201,144,26,0.1)",
        linewidth=1,
        showgrid=False,
    ),
    yaxis=dict(
        gridcolor=GRID_COLOR,
        zerolinecolor=ZERO_LINE,
        zerolinewidth=1,
        tickfont=dict(size=11, color="#C8B8A8", family="'IBM Plex Mono', monospace"),
        title_font=dict(size=12, color="#D0C4B4", family="'Rajdhani', sans-serif"),
        linecolor="rgba(201,144,26,0.1)",
        linewidth=1,
        showgrid=False,
    ),
    legend=dict(
        bgcolor="rgba(6,5,10,0.88)",
        bordercolor="rgba(201,144,26,0.2)",
        borderwidth=1,
        font=dict(size=10, color="#A89C8C", family="'IBM Plex Mono', monospace"),
        orientation="h",
        yanchor="bottom", y=1.02,
        xanchor="right", x=1,
    ),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="#100E18",
        bordercolor="rgba(201,144,26,0.45)",
        font=dict(color="#DDD8CE", size=11, family="'IBM Plex Mono', monospace"),
    ),
    margin=dict(l=54, r=20, t=52, b=44),
)


def _base_fig(title="", y_title="", x_title="DAY ON STREAM"):
    fig = go.Figure()
    layout = dict(**BASE_LAYOUT)
    layout["title"] = dict(
        text=title.upper(),
        font=dict(
            size=15, color="#E8DDD0",
            family="'Rajdhani', sans-serif",
        ),
        x=0.01, y=0.97,
    )
    layout["xaxis"] = dict(**BASE_LAYOUT["xaxis"], title=x_title)
    layout["yaxis"] = dict(**BASE_LAYOUT["yaxis"], title=y_title)
    fig.update_layout(**layout)
    return fig


def _add_art_band(fig, art_low, art_high, n_days=28):
    """Shaded ART acceptance band — gold fill, dotted border."""
    if art_low is None or art_high is None:
        return
    days = list(range(0, n_days + 3))
    # Fill band
    fig.add_trace(go.Scatter(
        x=days + days[::-1],
        y=[art_high] * len(days) + [art_low] * len(days),
        fill="toself",
        fillcolor="rgba(201,144,26,0.05)",
        line=dict(color="rgba(201,144,26,0.22)", width=1, dash="dot"),
        name="ART ACCEPTANCE",
        hoverinfo="skip",
        showlegend=True,
    ))
    # Top limit line
    fig.add_trace(go.Scatter(
        x=days,
        y=[art_high] * len(days),
        mode="lines",
        line=dict(color="rgba(201,144,26,0.18)", width=1, dash="dot"),
        showlegend=False,
        hoverinfo="skip",
    ))
    # Bottom limit line
    fig.add_trace(go.Scatter(
        x=days,
        y=[art_low] * len(days),
        mode="lines",
        line=dict(color="rgba(201,144,26,0.18)", width=1, dash="dot"),
        showlegend=False,
        hoverinfo="skip",
    ))


# ── Phase band colors ─────────────────────────────────────────────────────────
PHASE_COLORS = [
    "rgba(201,144,26,0.08)",   # gold
    "rgba(0,212,255,0.08)",    # cyan
    "rgba(123,97,255,0.08)",   # purple
    "rgba(255,107,107,0.08)",  # pink
    "rgba(0,245,160,0.08)",    # green
    "rgba(255,159,67,0.08)",   # orange
]

PHASE_BORDER_COLORS = [
    "rgba(201,144,26,0.25)",
    "rgba(0,212,255,0.25)",
    "rgba(123,97,255,0.25)",
    "rgba(255,107,107,0.25)",
    "rgba(0,245,160,0.25)",
    "rgba(255,159,67,0.25)",
]

PHASE_TEXT_COLORS = [
    "rgba(255,200,50,1.0)",
    "rgba(0,230,255,1.0)",
    "rgba(160,130,255,1.0)",
    "rgba(255,130,130,1.0)",
    "rgba(0,255,180,1.0)",
    "rgba(255,180,90,1.0)",
]


def add_phase_bands(fig, phases):
    """Add vertical colored bands to a chart showing experiment phases.
    phases: [{"from_day": int, "to_day": int, "feed_name": str, ...}]
    """
    if not phases or len(phases) < 2:
        return  # No bands needed for single-phase experiments
    for i, p in enumerate(phases):
        color = PHASE_COLORS[i % len(PHASE_COLORS)]
        border = PHASE_BORDER_COLORS[i % len(PHASE_BORDER_COLORS)]
        text_color = PHASE_TEXT_COLORS[i % len(PHASE_TEXT_COLORS)]
        feed_label = p.get("feed_name") or p.get("phase_name") or f"Phase {i+1}"
        fig.add_vrect(
            x0=p["from_day"] - 0.5,
            x1=p["to_day"] + 0.5,
            fillcolor=color,
            line=dict(color=border, width=1, dash="dot"),
            layer="below",
        )
        fig.add_annotation(
            x=(p["from_day"] + p["to_day"]) / 2,
            y=1.0,
            yref="paper",
            text=f"<b>{feed_label}</b>",
            showarrow=False,
            font=dict(size=12, color=text_color,
                      family="'Rajdhani', sans-serif"),
            yshift=12,
        )


def line_chart(title, y_title, series_list, art_low=None, art_high=None):
    """
    Generic line chart with Deep Field styling.
    series_list: [{"name": str, "x": list, "y": list, "color"?: str, "dash"?: str}]
    """
    fig = _base_fig(title=title, y_title=y_title)
    max_day = max((max(s["x"]) for s in series_list if s.get("x")), default=28)

    if art_low is not None and art_high is not None:
        _add_art_band(fig, art_low, art_high, n_days=max_day)

    for i, s in enumerate(series_list):
        color = s.get("color", PALETTE[i % len(PALETTE)])
        is_ref = s.get("dash") == "dot" or "ref" in s.get("name", "").lower() or "art" in s.get("name", "").lower() or "acceptance" in s.get("name", "").lower()

        fig.add_trace(go.Scatter(
            x=s["x"],
            y=s["y"],
            mode="lines+markers",
            name=s["name"],
            line=dict(
                color=color,
                width=1.5 if is_ref else 2,
                dash="dot" if is_ref else "solid",
            ),
            marker=dict(
                size=4 if is_ref else 6,
                color=color,
                line=dict(color=PAPER_BG, width=1.5),
                symbol="circle",
            ),
            opacity=0.55 if is_ref else 1.0,
            connectgaps=False,
            hovertemplate=(
                f"<b style='color:{color}'>{s['name']}</b><br>"
                f"Day %{{x}} → %{{y:.3f}}<extra></extra>"
            ),
        ))

    return fig


def multi_experiment_chart(title, y_title, exp_data_list, art_low=None, art_high=None):
    """
    Overlay chart for multiple experiments, each with a distinct palette color.
    exp_data_list: [{"exp_name": str, "x": list, "y": list}]
    """
    series = [
        {
            "name": e["exp_name"],
            "x": e["x"],
            "y": e["y"],
            "color": PALETTE[i % len(PALETTE)],
        }
        for i, e in enumerate(exp_data_list)
    ]
    return line_chart(title, y_title, series, art_low=art_low, art_high=art_high)


def vr_blend_donut(vr_blend):
    """
    Donut chart for VR feed blend — Deep Field styled.
    vr_blend: [{"name": str, "pct": float}]
    """
    if not vr_blend:
        return None

    labels = [v["name"] for v in vr_blend]
    values = [v["pct"] for v in vr_blend]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.60,
        marker=dict(
            colors=PALETTE[:len(labels)],
            line=dict(color=PAPER_BG, width=3),
        ),
        textfont=dict(
            color="#C8C0B0",
            size=10,
            family="'IBM Plex Mono', monospace",
        ),
        textposition="outside",
        texttemplate="%{label}<br><b>%{percent}</b>",
        hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PAPER_BG,
        font=dict(color="#C8C0B0", family="'IBM Plex Mono', monospace"),
        showlegend=False,
        margin=dict(l=20, r=20, t=28, b=20),
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
    return fig


def build_param_series(measurements, param_key, exp_name=None):
    """Extract x, y, art_low, art_high from measurement records for one parameter."""
    rows = sorted([m for m in measurements if m["parameter"] == param_key],
                  key=lambda r: r["day"])
    x = [r["day"] for r in rows]
    y = [r["value"] for r in rows]
    art_low  = rows[0]["art_low"]  if rows else None
    art_high = rows[0]["art_high"] if rows else None
    return {"name": exp_name or param_key, "x": x, "y": y}, art_low, art_high
