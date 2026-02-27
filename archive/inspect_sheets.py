import pandas as pd

file_path = r"D:\Claude Project\MEBU Database\EXPERIMENT DATA\04_Master_MEBU Result (Repeat Acceptance Test)_Feb-Mar'26.xlsx"
xl = pd.ExcelFile(file_path)

for sheet in ["Master Template", "HPS DAILY", "Condition"]:
    try:
        print(f"--- Sheet: {sheet} ---")
        df = pd.read_excel(xl, sheet_name=sheet, nrows=5)
        print("Columns:", df.columns.tolist()[:15])  # print up to 15 cols
        print("Sample data:")
        for row in df.values.tolist():
            print(row[:15])
        print("\n")
    except Exception as e:
        print(f"Error reading {sheet}: {e}")
