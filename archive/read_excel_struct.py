import pandas as pd
import json
import sys

# Try to read the master file
file_path = r"D:\Claude Project\MEBU Database\EXPERIMENT DATA\04_Master_MEBU Result (Repeat Acceptance Test)_Feb-Mar'26.xlsx"
try:
    xl = pd.ExcelFile(file_path)
    sheets = xl.sheet_names
    print("Sheets available:", sheets)
    
    # Try looking for a Lab Result Summary sheet
    target_sheet = None
    for s in sheets:
        if "lab" in s.lower() and "summary" in s.lower() or "lab result summary" in s.lower():
            target_sheet = s
            break
            
    if not target_sheet:
        for s in sheets:
            if "lab" in s.lower():
                target_sheet = s
                break

    if target_sheet:
        print(f"Reading sheet: {target_sheet}")
        df = pd.read_excel(file_path, sheet_name=target_sheet, header=None, nrows=10)
        print("Data sample:")
        for row in df.values.tolist():
            print(row)
    else:
        print("Could not find a Lab result sheet.")

except Exception as e:
    print("Error:", e)
