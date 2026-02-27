"""
MEBU Analytics — DEEP FIELD Chart Factory
Plotly charts tuned to the Deep Field design system.
"""
import plotly.graph_objects as go

# ── Palette (mirrors CSS design tokens) ───────────────────────────────────────
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


def _base_fig(title="", y_title="", x_title="DAY ON STREAM"):
    fig = go.Figure()
    layout = dict(**BASE_LAYOUT)
    layout["title"] = dict(
        text=title.upper(),
        font=dict(
            size=12, color="#7A6A50",
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
