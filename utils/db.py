"""
SQLite database layer for MEBU Analytics Platform.
Two tables: experiments (run-level metadata) and measurements (daily data).
"""
import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "mebu_analytics.sqlite"


def get_conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            exp_name    TEXT NOT NULL,
            exp_type    TEXT,
            start_date  TEXT,
            file_path   TEXT,
            vr_blend    TEXT DEFAULT '[]',
            rx1_temp    REAL,
            rx2_temp    REAL,
            rx3_temp    REAL,
            notes       TEXT,
            created_at  TEXT DEFAULT (datetime('now')),
            UNIQUE(exp_name)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            exp_id      INTEGER REFERENCES experiments(id) ON DELETE CASCADE,
            day         INTEGER,
            op_date     TEXT,
            lab_date    TEXT,
            category    TEXT,
            parameter   TEXT,
            unit        TEXT,
            value       REAL,
            art_low     REAL,
            art_high    REAL,
            within_spec TEXT,
            UNIQUE(exp_id, day, parameter)
        )
    """)

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

    conn.commit()
    conn.close()
    _migrate_existing_to_phases()


# ── Experiments ──────────────────────────────────────────────────────────────

def upsert_experiment(exp_name, exp_type="", start_date="", file_path="",
                      vr_blend=None, rx1_temp=None, rx2_temp=None, rx3_temp=None,
                      notes=""):
    """Insert or update experiment. Returns exp_id."""
    vr_json = json.dumps(vr_blend or [])
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO experiments (exp_name, exp_type, start_date, file_path,
                                  vr_blend, rx1_temp, rx2_temp, rx3_temp, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(exp_name) DO UPDATE SET
            exp_type   = excluded.exp_type,
            start_date = excluded.start_date,
            file_path  = excluded.file_path,
            notes      = excluded.notes
    """, (exp_name, exp_type, start_date, file_path,
          vr_json, rx1_temp, rx2_temp, rx3_temp, notes))
    conn.commit()
    exp_id = c.execute("SELECT id FROM experiments WHERE exp_name=?", (exp_name,)).fetchone()[0]
    conn.close()
    return exp_id


def update_experiment_meta(exp_id, vr_blend=None, rx1_temp=None, rx2_temp=None,
                           rx3_temp=None, notes=None):
    """Update only the editable metadata fields."""
    conn = get_conn()
    c = conn.cursor()
    if vr_blend is not None:
        c.execute("UPDATE experiments SET vr_blend=? WHERE id=?",
                  (json.dumps(vr_blend), exp_id))
    if rx1_temp is not None:
        c.execute("UPDATE experiments SET rx1_temp=? WHERE id=?", (rx1_temp, exp_id))
    if rx2_temp is not None:
        c.execute("UPDATE experiments SET rx2_temp=? WHERE id=?", (rx2_temp, exp_id))
    if rx3_temp is not None:
        c.execute("UPDATE experiments SET rx3_temp=? WHERE id=?", (rx3_temp, exp_id))
    if notes is not None:
        c.execute("UPDATE experiments SET notes=? WHERE id=?", (notes, exp_id))
    conn.commit()
    conn.close()


def get_all_experiments():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM experiments ORDER BY start_date").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_experiment(exp_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM experiments WHERE id=?", (exp_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def delete_experiment(exp_id):
    conn = get_conn()
    conn.execute("DELETE FROM experiments WHERE id=?", (exp_id,))
    conn.commit()
    conn.close()


# ── VR Feeds ─────────────────────────────────────────────────────────────────

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


# ── Phases ───────────────────────────────────────────────────────────────────

def save_phases(exp_id, phases_list):
    """Replace all phases for an experiment.
    phases_list: [{"phase_name", "from_day", "to_day", "feed_id", "rx1_temp", "rx2_temp", "rx3_temp"}]
    """
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


# ── Measurements ─────────────────────────────────────────────────────────────

def bulk_insert_measurements(records):
    """Insert list of measurement dicts, ignoring duplicates. Returns count inserted."""
    if not records:
        return 0
    conn = get_conn()
    c = conn.cursor()
    inserted = 0
    for r in records:
        try:
            c.execute("""
                INSERT OR IGNORE INTO measurements
                    (exp_id, day, op_date, lab_date, category, parameter,
                     unit, value, art_low, art_high, within_spec)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (r["exp_id"], r["day"], r.get("op_date", ""), r.get("lab_date", ""),
                  r["category"], r["parameter"], r.get("unit", ""),
                  r["value"], r.get("art_low"), r.get("art_high"),
                  r.get("within_spec", "N/A")))
            inserted += c.rowcount
        except Exception:
            pass
    conn.commit()
    conn.close()
    return inserted


def get_measurements(exp_id, parameters=None):
    """Return measurements for one experiment as list of dicts."""
    conn = get_conn()
    if parameters:
        placeholders = ",".join("?" * len(parameters))
        rows = conn.execute(
            f"SELECT * FROM measurements WHERE exp_id=? AND parameter IN ({placeholders}) ORDER BY day",
            [exp_id] + list(parameters)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM measurements WHERE exp_id=? ORDER BY day",
            (exp_id,)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_multi_experiment_measurements(exp_ids, parameters=None):
    """Return measurements for multiple experiments as list of dicts."""
    if not exp_ids:
        return []
    conn = get_conn()
    placeholders = ",".join("?" * len(exp_ids))
    if parameters:
        pphs = ",".join("?" * len(parameters))
        rows = conn.execute(
            f"SELECT m.*, e.exp_name FROM measurements m "
            f"JOIN experiments e ON m.exp_id=e.id "
            f"WHERE m.exp_id IN ({placeholders}) AND m.parameter IN ({pphs}) "
            f"ORDER BY m.exp_id, m.day",
            list(exp_ids) + list(parameters)
        ).fetchall()
    else:
        rows = conn.execute(
            f"SELECT m.*, e.exp_name FROM measurements m "
            f"JOIN experiments e ON m.exp_id=e.id "
            f"WHERE m.exp_id IN ({placeholders}) ORDER BY m.exp_id, m.day",
            list(exp_ids)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_available_parameters(exp_id=None):
    """List all unique parameter names in DB (or for one experiment)."""
    conn = get_conn()
    if exp_id:
        rows = conn.execute(
            "SELECT DISTINCT parameter, category, unit FROM measurements WHERE exp_id=? ORDER BY category, parameter",
            (exp_id,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT DISTINCT parameter, category, unit FROM measurements ORDER BY category, parameter"
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_measurement_count(exp_id):
    conn = get_conn()
    n = conn.execute("SELECT COUNT(*) FROM measurements WHERE exp_id=?", (exp_id,)).fetchone()[0]
    conn.close()
    return n


# ── Migration ────────────────────────────────────────────────────────────────

def _migrate_existing_to_phases():
    """One-time migration: convert old vr_blend + temps into a single phase per experiment."""
    conn = get_conn()
    c = conn.cursor()
    experiments = c.execute("SELECT * FROM experiments").fetchall()
    for exp in experiments:
        exp = dict(exp)
        existing = c.execute("SELECT COUNT(*) FROM phases WHERE exp_id=?", (exp["id"],)).fetchone()[0]
        if existing > 0:
            continue
        vr_blend = json.loads(exp.get("vr_blend") or "[]")
        if not vr_blend and not exp.get("rx1_temp"):
            continue
        max_day_row = c.execute("SELECT MAX(day) FROM measurements WHERE exp_id=?", (exp["id"],)).fetchone()
        max_day = max_day_row[0] if max_day_row and max_day_row[0] else 28
        feed_id = None
        if vr_blend:
            feed_name = f"{exp['exp_name']}_blend"
            comp_json = json.dumps(vr_blend)
            c.execute("INSERT OR IGNORE INTO vr_feeds (feed_name, composition) VALUES (?, ?)",
                      (feed_name, comp_json))
            feed_row = c.execute("SELECT id FROM vr_feeds WHERE feed_name=?", (feed_name,)).fetchone()
            feed_id = feed_row[0] if feed_row else None
        c.execute("""
            INSERT INTO phases (exp_id, phase_name, from_day, to_day, feed_id, rx1_temp, rx2_temp, rx3_temp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (exp["id"], "Default", 1, max_day, feed_id,
              exp.get("rx1_temp"), exp.get("rx2_temp"), exp.get("rx3_temp")))
    conn.commit()
    conn.close()
