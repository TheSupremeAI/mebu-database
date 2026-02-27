import pandas as pd

file_path = r"D:\Claude Project\MEBU Database\EXPERIMENT DATA\04_Master_MEBU Result (Repeat Acceptance Test)_Feb-Mar'26.xlsx"
df = pd.read_excel(file_path, sheet_name="Master Template")
# Save the first 100 rows and first 6 columns to see the variable names and the first day of data
df.iloc[0:150, 0:6].to_csv(r"D:\Claude Project\MEBU Database\master_vars.csv", index=False)
print("Saved master_vars.csv")
