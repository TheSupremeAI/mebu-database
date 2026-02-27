"""
Excel -> SQLite extractor for MEBU Master Template and Product sheets.
Header-aware extraction handles variable column ranges across files.
"""
import pandas as pd
from pathlib import Path

# ── Column Helpers ────────────────────────────────────────────────────────────

def excel_col_to_idx(col_str):
    """Convert Excel column string (e.g. 'A', 'BP') to 0-based index."""
    exp = 0
    idx = 0
    for char in reversed(col_str.upper()):
        idx += (ord(char) - ord('A') + 1) * (26 ** exp)
        exp += 1
    return idx - 1

def _norm(s):
    return str(s).strip().lower()

def _safe_float(val):
    try:
        if pd.isna(val): return None
        f = float(val)
        return None if f != f else f
    except (ValueError, TypeError):
        return None

def _safe_date(val):
    try:
        if pd.isna(val): return ""
        d = pd.to_datetime(val, errors="coerce")
        if pd.isna(d): return ""
        return d.strftime("%d-%b-%y")
    except:
        return ""

def _matches_any(cell_val, search_strings):
    n = _norm(cell_val)
    return any(_norm(s) in n for s in search_strings)

# ── Parameter catalogues ──────────────────────────────────────────────────────

PARAM_CATALOGUE = {
    "560plus_wt":  (["560 plus", "560plus", "560 Plus"], "Product Distribution", "wt%", None, None, (5, 32)),
    "360_500_wt":  (["360-500"],  "Product Distribution", "wt%", None, None, (5, 32)),
    "250_360_wt":  (["250-360"],  "Product Distribution", "wt%", None, None, (5, 32)),
    "160_250_wt":  (["160-250"],  "Product Distribution", "wt%", None, None, (5, 32)),
    "90_160_wt":   (["90-160"],   "Product Distribution", "wt%", None, None, (5, 32)),
    "IBP_90_wt":   (["IBP-90"],   "Product Distribution", "wt%", None, None, (5, 32)),
    "Ni_ppm":  (["Ni, ppm"],  "Metals in Product", "ppm", None, None, None),
    "V_ppm":   (["V, ppm"],   "Metals in Product", "ppm", None, None, None),
    "Fe_ppm":  (["Fe, ppm"],  "Metals in Product", "ppm", None, None, None),
    "S_wt": (["S, wt% (ASTM D4294)", "S, wt%"],      "Impurities", "wt%", None, None, None),
    "N_wt": (["N, wt% (ASTM D5762)", "N, wt%"],      "Impurities", "wt%", None, None, None),
    "C5_Asph": (["C5 Asphaltene, wt%"], "Stability", "wt%", None, None, None),
    "C7_Asph": (["C7 Asphaltene, wt%"], "Stability", "wt%", None, None, None),
    "MCRT":    (["MCRT, wt%"],          "Stability", "wt%", None, None, None),
    "HC_ratio": (["H/C Ratio, wt/wt"], "Composition", "wt/wt", None, None, None),
    "LHSV_actual": (["MEBU LHSV, Actual"], "Operating", "hr-1", None, None, None),
    "Total_rate":  (["Total rate, g/h"],   "Operating", "g/h",  None, None, None),
    "560plus_ART": (["560 plus, ART, acceptance", "560plus, ART"], "Reference", "wt%", None, None, (5, 32)),
    "Ni_ART":      (["Ni, ppm, ART, Acceptance"],  "Reference", "ppm",    None, None, None),
    "V_ART":       (["V, ppm, ART, Acceptance"],   "Reference", "ppm",    None, None, None),
    "S_ART":       (["S, wt%, ART Acceptance", "S, wt%, ART"], "Reference", "wt%", None, None, None),
    "N_ART":       (["N, ppm, ART, Acceptance"],   "Reference", "ppm",    None, None, None),
    "C7_ART":      (["C7 Asphaltene, wt%, ART, Acceptance"], "Reference", "wt%", None, None, None),
    "MCRT_ART":    (["MCRT, wt%, ART, Acceptance"], "Reference", "wt%",   None, None, None),
    "HC_ART":      (["H/C Ratio, wt/wt, ART"],     "Reference", "wt/wt",  None, None, None),
    "LHSV_target": (["MEBU Target LHSV"],           "Reference", "hr-1",   None, None, None),
}

CONVERSION_PARAMS = {
    "CrkConv":      (["CrkConv, wt%, As is"], "Conversion", "wt%", 70.0, 78.0, (5, 32)),
    "NiConv":       (["NiConv, wt%"],  "Conversion", "wt%", 88.0, 100.0, (5, 32)),
    "VConv":        (["VConv, wt%"],   "Conversion", "wt%", 98.0, 100.0, (5, 32)),
    "NiV_Conv":     (["(Ni+V)Conv, wt%"], "Conversion", "wt%", 96.0, 100.0, (5, 32)),
    "FeConv":       (["FeConv, wt%"],  "Conversion", "wt%", None, None, (5, 32)),
    "SConv":        (["SConv, wt%"],   "Conversion", "wt%", 80.0, 100.0, (5, 32)),
    "NConv":        (["NConv, wt%"],   "Conversion", "wt%", None, None, (5, 32)),
    "MCRConv":      (["MCRConv, wt%"], "Conversion", "wt%", 70.0, 100.0, (5, 32)),
    "C7_AsphConv":  (["C7 AsConv,wt%"], "Conversion", "wt%", None, None, (5, 32)),
    "C5_AsphConv":  (["C5 AsConc, wt%"], "Conversion", "wt%", None, None, (5, 32)),
    "Sedimentation":(["Sedimentation, ppm"], "Sedimentation", "ppm", 0.0, 1500.0, (5, 32)),
}

HPS_CATALOGUE = {
    "HPS_API":     (["API @ 15.6 degC"], "HPS Product", "API", None, None, None),
    "HPS_Density": (["Density @ 15.6 degC"], "HPS Product", "g/cm3", None, None, None),
    "HPS_Sulfur":  (["Sulfur"], "HPS Product", "wt%", None, None, None),
    "HPS_Nitrogen":(["ASTM D5762"], "HPS Product", "ppmw", None, None, None),
    "HPS_CCR":     (["CCR"], "HPS Product", "wt%", None, None, None),
    "HPS_Sediment":(["Total Sediment"], "HPS Product", "wt%", None, None, None),
}

LTO_CATALOGUE = {
    "LTO_API":     (["API"], "LTO Product", "API", None, None, None),
    "LTO_Density": (["Density"], "LTO Product", "g/cm3", None, None, None),
    "LTO_Sulfur":  (["Sulfur"], "LTO Product", "wt%", None, None, None),
    "LTO_Nitrogen":(["ASTM D5762"], "LTO Product", "ppmw", None, None, None),
}

ISV_CATALOGUE = {
    "ISV_Sulfur":  (["Sulfur"], "ISV Product", "wt%", None, None, None),
    "ISV_560plus": (["560+"], "ISV Product", "wt%", None, None, None),
    "ISV_Ni":      (["Nickle (Ni)", "Ni"], "ISV Product", "ppm", None, None, None),
    "ISV_V":       (["Vanadium (V)", "V"], "ISV Product", "ppm", None, None, None),
    "ISV_NiV":     (["Ni+V"], "ISV Product", "ppm", None, None, None),
    "ISV_MCRT":    (["CCR", "MCRT"], "ISV Product", "wt%", None, None, None),
    "ISV_Nitrogen":(["ASTM D5762"], "ISV Product", "ppmw", None, None, None),
}


HIGH_GAS_CATALOGUE = {
    "HG_H2":  (["Hydrogen"], "High Gas", "mol%", None, None, None),
    "HG_C1":  (["C1"], "High Gas", "mol%", None, None, None),
    "HG_C2":  (["C2"], "High Gas", "mol%", None, None, None),
    "HG_C3":  (["C3"], "High Gas", "mol%", None, None, None),
    "HG_C4":  (["C4(Total)"], "High Gas", "mol%", None, None, None),
    "HG_C5":  (["C5"], "High Gas", "mol%", None, None, None),
    "HG_C6plus": (["C6 Plus"], "High Gas", "mol%", None, None, None),
    "HG_CO":  (["CO"], "High Gas", "mol%", None, None, None),
    "HG_CO2": (["CO2"], "High Gas", "mol%", None, None, None),
    "HG_H2S": (["H2S"], "High Gas", "mol%", None, None, None),
    "HG_N2":  (["N2"], "High Gas", "mol%", None, None, None),
}

LOW_GAS_CATALOGUE = {
    "LG_H2":  (["Hydrogen"], "Low Gas", "mol%", None, None, None),
    "LG_C1":  (["C1"], "Low Gas", "mol%", None, None, None),
    "LG_C2":  (["C2"], "Low Gas", "mol%", None, None, None),
    "LG_C3":  (["C3"], "Low Gas", "mol%", None, None, None),
    "LG_C4":  (["C4(Total)"], "Low Gas", "mol%", None, None, None),
    "LG_C5":  (["C5"], "Low Gas", "mol%", None, None, None),
    "LG_C6plus": (["C6  Plus", "C6 Plus"], "Low Gas", "mol%", None, None, None),
    "LG_CO":  (["CO"], "Low Gas", "mol%", None, None, None),
    "LG_CO2": (["CO2"], "Low Gas", "mol%", None, None, None),
    "LG_H2S": (["H2S"], "Low Gas", "mol%", None, None, None),
    "LG_N2":  (["N2"], "Low Gas", "mol%", None, None, None),
}

# ── Extraction Logic ──────────────────────────────────────────────────────────

def _find_param_rows(df, catalogue, col_idx=2):
    found = {}
    col = df.iloc[:, col_idx].fillna("").astype(str)
    # 1. Exact match
    for key, (searches, *_) in catalogue.items():
        for i, val in col.items():
            if any(_norm(val.strip()) == _norm(s) for s in searches):
                found[key] = i; break
    # 2. Substring match for remaining
    for key, (searches, *_) in catalogue.items():
        if key in found: continue
        for i, val in col.items():
            if _matches_any(val, searches):
                found[key] = i; break
    return found

def _find_day_columns(df):
    day_row_idx = op_row_idx = lab_row_idx = None
    for r in range(min(15, len(df))):
        row_vals = df.iloc[r].fillna("").astype(str)
        for c, val in enumerate(row_vals):
            v = _norm(val)
            if day_row_idx is None and "day on stream" in v: day_row_idx = r
            if op_row_idx is None and "pilot plant operation" in v: op_row_idx = r
            if lab_row_idx is None and ("lab date" in v or "date" == v): lab_row_idx = r

    if day_row_idx is None:
        for r in range(min(15, len(df))):
            row = df.iloc[r]
            nums = [idx for idx, x in enumerate(row) if isinstance(x, (int, float)) and 0 < x < 100]
            if len(nums) > 5:
                day_row_idx = r; break

    if day_row_idx is None: return []
    day_row = df.iloc[day_row_idx]
    op_row = df.iloc[op_row_idx] if op_row_idx is not None else None
    lab_row = df.iloc[lab_row_idx] if lab_row_idx is not None else None

    results = []
    for col_idx in range(len(day_row)):
        try:
            val = day_row.iloc[col_idx]
            if pd.isna(val): continue
            day = int(float(val))
            if day < 1 or day > 100: continue
            results.append({
                "col": col_idx, "day": day,
                "op_date": _safe_date(op_row.iloc[col_idx]) if (op_row is not None and col_idx < len(op_row)) else "",
                "lab_date": _safe_date(lab_row.iloc[col_idx]) if (lab_row is not None and col_idx < len(lab_row)) else "",
            })
        except: continue

    seen, unique = set(), []
    for r in results:
        if r["day"] not in seen:
            seen.add(r["day"]); unique.append(r)
    return sorted(unique, key=lambda x: x["day"])

def _extract_sheet_data(df, catalogue, day_cols, exp_id):
    param_rows = {}
    for c in [2, 3, 4]:
        remaining = {k: v for k, v in catalogue.items() if k not in param_rows}
        if not remaining: break
        found = _find_param_rows(df, remaining, col_idx=c)
        param_rows.update(found)

    records = []
    for key, row_idx in param_rows.items():
        info = catalogue[key]
        fixed = info[5] if len(info) > 5 else None
        target_cols = day_cols
        if fixed: target_cols = [dc for dc in day_cols if fixed[0] <= dc["col"] <= fixed[1]]

        for dc in target_cols:
            val = _safe_float(df.iloc[row_idx, dc["col"]])
            if val is None: continue
            if val == 0.0 and info[1] not in ("High Gas", "Low Gas"): continue
            records.append({
                "exp_id":      exp_id, "day": dc["day"], "op_date": dc["op_date"], "lab_date": dc["lab_date"],
                "category":    info[1], "parameter": key, "unit": info[2], "value": round(val, 5),
                "art_low": info[3], "art_high": info[4], "within_spec": "N/A"
            })
    return records

def extract_from_file(file_path, exp_id, exp_name=""):
    all_records = []
    # 1. Master Template
    try:
        df = pd.read_excel(str(file_path), sheet_name="Master Template", header=None)
        all_records.extend(_extract_sheet_data(df, {**PARAM_CATALOGUE, **CONVERSION_PARAMS}, _find_day_columns(df), exp_id))
    except: pass

    # 2. HPS DAILY (HPS + Gas)
    try:
        df = pd.read_excel(str(file_path), sheet_name="HPS DAILY", header=None)
        days = _find_day_columns(df)
        if days:
            all_records.extend(_extract_sheet_data(df, HPS_CATALOGUE, days, exp_id))
            
            # Find Gas sections
            hg_header_idx = lg_header_idx = None
            for r in range(len(df)):
                row_vals = df.iloc[r, 0:11].fillna("").astype(str)
                for val in row_vals:
                    v = val.lower()
                    if "high gas" in v: hg_header_idx = r
                    if "low gas" in v: lg_header_idx = r
                if hg_header_idx is not None and lg_header_idx is not None: break

            if hg_header_idx is not None:
                hg_rows = _find_param_rows(df.iloc[hg_header_idx:hg_header_idx+15], HIGH_GAS_CATALOGUE, col_idx=3)
                for k, abs_r_idx in hg_rows.items():
                    for dc in days:
                        val = _safe_float(df.iloc[abs_r_idx, dc["col"]])
                        if val is not None:
                            all_records.append({
                                "exp_id": exp_id, "day": dc["day"], "op_date": dc["op_date"], "lab_date": dc["lab_date"],
                                "category": "High Gas", "parameter": k, "unit": "mol%", "value": round(val, 5),
                                "art_low": None, "art_high": None, "within_spec": "N/A"
                            })

            if lg_header_idx is not None:
                lg_rows = _find_param_rows(df.iloc[lg_header_idx:lg_header_idx+15], LOW_GAS_CATALOGUE, col_idx=3)
                for k, abs_r_idx in lg_rows.items():
                    for dc in days:
                        val = _safe_float(df.iloc[abs_r_idx, dc["col"]])
                        if val is not None:
                            all_records.append({
                                "exp_id": exp_id, "day": dc["day"], "op_date": dc["op_date"], "lab_date": dc["lab_date"],
                                "category": "Low Gas", "parameter": k, "unit": "mol%", "value": round(val, 5),
                                "art_low": None, "art_high": None, "within_spec": "N/A"
                            })

    except: pass

    # 3. LTO DAILY
    try:
        df = pd.read_excel(str(file_path), sheet_name="LTO DAILY", header=None)
        all_records.extend(_extract_sheet_data(df, LTO_CATALOGUE, _find_day_columns(df), exp_id))
    except: pass

    # 4. ISV
    try:
        df = pd.read_excel(str(file_path), sheet_name="ISV", header=None)
        all_records.extend(_extract_sheet_data(df, ISV_CATALOGUE, _find_day_columns(df), exp_id))
    except: pass

    return all_records, None if all_records else "No data found."
