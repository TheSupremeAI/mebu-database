# Multi-Phase VR Feed Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Add multi-phase VR feed support with a feed library, phase timeline editor in Settings, and colored phase bands on Dashboard/Product Results charts.

**Architecture:** Two new SQLite tables (`vr_feeds`, `phases`) store reusable feed recipes and per-experiment day-range phases. The Settings page gets a phase editor replacing the old single blend/temp fields. Charts get vertical background bands showing phase boundaries.

**Tech Stack:** Python, SQLite3, Streamlit, Plotly

---

### Task 1: Add New Tables and CRUD Functions to `utils/db.py`

**Files:**
- Modify: `utils/db.py`

**Step 1: Add `vr_feeds` and `phases` table creation to `init_db()`**

Add after the existing `measurements` table creation:

```python
c.execute("""
    CREATE TABLE IF NOT EXISTS vr_feeds (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        feed_name   TEXT NOT NULL UNIQUE,
        composition TEXT DEFAULT '[]'
    )
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS phases (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        exp_id      INTEGER REFERENCES experiments(id) ON DELETE CASCADE,
        phase_name  TEXT DEFAULT '',
        from_day    INTEGER NOT NULL,
        to_day      INTEGER NOT NULL,
        feed_id     INTEGER REFERENCES vr_feeds(id),
        rx1_temp    REAL,
        rx2_temp    REAL,
        rx3_temp    REAL
    )
""")
```

**Step 2: Add VR Feed CRUD functions**

```python
def upsert_vr_feed(feed_name, composition):
    """Insert or update a VR feed recipe. Returns feed_id."""
    comp_json = json.dumps(composition or [])
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO vr_feeds (feed_name, composition)
        VALUES (?, ?)
        ON CONFLICT(feed_name) DO UPDATE SET composition = excluded.composition
    """, (feed_name, comp_json))
    conn.commit()
    feed_id = c.execute("SELECT id FROM vr_feeds WHERE feed_name=?", (feed_name,)).fetchone()[0]
    conn.close()
    return feed_id

def get_all_vr_feeds():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM vr_feeds ORDER BY feed_name").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_vr_feed(feed_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM vr_feeds WHERE id=?", (feed_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def delete_vr_feed(feed_id):
    conn = get_conn()
    conn.execute("DELETE FROM vr_feeds WHERE id=?", (feed_id,))
    conn.commit()
    conn.close()
```

**Step 3: Add Phase CRUD functions**

```python
def save_phases(exp_id, phases_list):
    """Replace all phases for an experiment. phases_list: [{"phase_name", "from_day", "to_day", "feed_id", "rx1_temp", "rx2_temp", "rx3_temp"}]"""
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM phases WHERE exp_id=?", (exp_id,))
    for p in phases_list:
        c.execute("""
            INSERT INTO phases (exp_id, phase_name, from_day, to_day, feed_id, rx1_temp, rx2_temp, rx3_temp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (exp_id, p.get("phase_name", ""), p["from_day"], p["to_day"],
              p.get("feed_id"), p.get("rx1_temp"), p.get("rx2_temp"), p.get("rx3_temp")))
    conn.commit()
    conn.close()

def get_phases(exp_id):
    """Return phases for one experiment, joined with feed name."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT p.*, f.feed_name, f.composition
        FROM phases p
        LEFT JOIN vr_feeds f ON p.feed_id = f.id
        WHERE p.exp_id=?
        ORDER BY p.from_day
    """, (exp_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
```

**Step 4: Add auto-migration function**

```python
def migrate_existing_to_phases():
    """One-time migration: convert old vr_blend + temps into a single phase per experiment."""
    conn = get_conn()
    c = conn.cursor()
    experiments = c.execute("SELECT * FROM experiments").fetchall()
    for exp in experiments:
        exp = dict(exp)
        existing_phases = c.execute("SELECT COUNT(*) FROM phases WHERE exp_id=?", (exp["id"],)).fetchone()[0]
        if existing_phases > 0:
            continue  # already has phases
        vr_blend = json.loads(exp.get("vr_blend") or "[]")
        if not vr_blend and not exp.get("rx1_temp"):
            continue  # no data to migrate
        # Find max day for this experiment
        max_day_row = c.execute("SELECT MAX(day) FROM measurements WHERE exp_id=?", (exp["id"],)).fetchone()
        max_day = max_day_row[0] if max_day_row and max_day_row[0] else 28
        feed_id = None
        if vr_blend:
            # Create a feed entry from the old blend
            feed_name = f"{exp['exp_name']}_blend"
            comp_json = json.dumps(vr_blend)
            c.execute("""
                INSERT OR IGNORE INTO vr_feeds (feed_name, composition) VALUES (?, ?)
            """, (feed_name, comp_json))
            feed_row = c.execute("SELECT id FROM vr_feeds WHERE feed_name=?", (feed_name,)).fetchone()
            feed_id = feed_row[0] if feed_row else None
        c.execute("""
            INSERT INTO phases (exp_id, phase_name, from_day, to_day, feed_id, rx1_temp, rx2_temp, rx3_temp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (exp["id"], "Default", 1, max_day, feed_id,
              exp.get("rx1_temp"), exp.get("rx2_temp"), exp.get("rx3_temp")))
    conn.commit()
    conn.close()
```

**Step 5: Call migration in `init_db()`**

Add at the end of `init_db()`, before `conn.close()`:
```python
conn.commit()
conn.close()
migrate_existing_to_phases()
```

**Step 6: Verify syntax**

Run: `python -m py_compile utils/db.py`
Expected: exit code 0, no output

**Step 7: Commit**

```bash
git add utils/db.py
git commit -m "feat: add vr_feeds and phases tables with CRUD and migration"
```

---

### Task 2: Add Phase Band Function to `utils/charts.py`

**Files:**
- Modify: `utils/charts.py`

**Step 1: Add `add_phase_bands()` function**

Add after `_add_art_band`:

```python
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

def add_phase_bands(fig, phases):
    """Add vertical colored bands to a chart showing experiment phases.
    phases: [{"from_day": int, "to_day": int, "feed_name": str, ...}]
    """
    if not phases:
        return
    for i, p in enumerate(phases):
        color = PHASE_COLORS[i % len(PHASE_COLORS)]
        border = PHASE_BORDER_COLORS[i % len(PHASE_BORDER_COLORS)]
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
            font=dict(size=9, color=border.replace("0.25", "0.7"),
                      family="'Rajdhani', sans-serif"),
            yshift=10,
        )
```

**Step 2: Verify syntax**

Run: `python -m py_compile utils/charts.py`
Expected: exit code 0

**Step 3: Commit**

```bash
git add utils/charts.py
git commit -m "feat: add phase band overlay function to charts"
```

---

### Task 3: Rebuild Settings Page (`pages/5_Settings.py`)

**Files:**
- Modify: `pages/5_Settings.py`

**Step 1: Replace the VR Blend + Temperature editor with Phase Timeline Editor**

Replace the entire VR Blend editor section and Temperatures section with:
1. A **VR Feed Library** (expandable) to create/edit named feed recipes
2. A **Phase Timeline Editor** with rows: Phase Name, From Day, To Day, VR Feed (selectbox from library), Rx-1, Rx-2, Rx-3

**Step 2: Update imports**

Add `get_all_vr_feeds, upsert_vr_feed, delete_vr_feed, save_phases, get_phases` to the import from `utils.db`.

**Step 3: Build VR Feed Library section**

Inside an `st.expander("📚 VR Feed Library")`:
- Show existing feeds in a loop with editable composition rows
- "➕ Add New Feed" button
- Each feed: Name, composition table (VR Name + %), delete button

**Step 4: Build Phase Editor section**

- Show existing phases in editable rows
- Each row: Phase Name, From Day (number_input), To Day (number_input), VR Feed (selectbox), Rx-1, Rx-2, Rx-3
- "➕ Add Phase" button, "✕" delete per row
- "💾 Save Changes" button at the bottom

**Step 5: Remove old VR Blend Preview section**

Remove the donut-preview section since phases replace it.

**Step 6: Verify syntax**

Run: `python -m py_compile pages/5_Settings.py`
Expected: exit code 0

**Step 7: Commit**

```bash
git add pages/5_Settings.py
git commit -m "feat: replace VR blend editor with phase timeline editor"
```

---

### Task 4: Update Dashboard to Show Phase Bands (`pages/2_Dashboard.py`)

**Files:**
- Modify: `pages/2_Dashboard.py`

**Step 1: Import `get_phases` and `add_phase_bands`**

```python
from utils.db import init_db, get_all_experiments, get_measurements, get_experiment, get_phases
from utils.charts import line_chart, vr_blend_donut, PALETTE, add_phase_bands
```

**Step 2: Load phases for the selected experiment**

After `avail_params = ...`:
```python
phases = get_phases(exp_id)
```

**Step 3: Replace VR Blend donut with Phase Summary Table**

Replace the `donut_col` content with an `st.dataframe` showing phase data (Phase Name, Days, VR Feed, Rx-1, Rx-2, Rx-3).

**Step 4: Add phase bands to all charts**

Modify `chart_or_info` function to accept and use `phases`:
```python
def chart_or_info(title, y_title, param_pairs, color=None, phases=None):
    # ... existing code to build fig ...
    if phases:
        add_phase_bands(fig, phases)
    st.plotly_chart(fig, use_container_width=True)
```

Pass `phases=phases` in all `chart_or_info()` calls.

**Step 5: Verify syntax**

Run: `python -m py_compile pages/2_Dashboard.py`
Expected: exit code 0

**Step 6: Commit**

```bash
git add pages/2_Dashboard.py
git commit -m "feat: add phase bands and phase table to dashboard"
```

---

### Task 5: Update Product Results to Show Phase Bands (`pages/4_Product_Results.py`)

**Files:**
- Modify: `pages/4_Product_Results.py`

**Step 1: Import `get_phases` and `add_phase_bands`**

**Step 2: Load phases and pass to `product_chart()`**

Modify `product_chart` to accept a `phases` parameter and call `add_phase_bands(fig, phases)`.

**Step 3: Pass `phases=phases` in all `product_chart()` calls**

**Step 4: Verify syntax**

Run: `python -m py_compile pages/4_Product_Results.py`
Expected: exit code 0

**Step 5: Commit**

```bash
git add pages/4_Product_Results.py
git commit -m "feat: add phase bands to product results charts"
```

---

### Task 6: Local Testing and Final Commit

**Step 1: Run the app locally**

```bash
cd "D:\Claude Project\MEBU Database"
streamlit run main.py
```

**Step 2: Manual verification checklist**

1. Open ⚙️ Settings → create a VR Feed in the library (e.g., ABQ3358 with Basrah Heavy 55%, Arab Medium 10%, Arab Light 35%)
2. Add 2–3 phases to an experiment with different day ranges, feeds, and temps → Save
3. Go to 📊 Dashboard → verify colored bands appear on all charts
4. Verify the Phase Summary Table appears with correct data
5. Go to 🧪 Product Results → verify colored bands appear on all tabs
6. Go back to ⚙️ Settings → verify phases are correctly loaded when re-opening

**Step 3: Push to GitHub**

```bash
git push origin main
```
