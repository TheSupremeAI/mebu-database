import pandas as pd

file_path = r"D:\Claude Project\MEBU Database\EXPERIMENT DATA\04_Master_MEBU Result (Repeat Acceptance Test)_Feb-Mar'26.xlsx"
df = pd.read_excel(file_path, sheet_name="Lab Results Summary")
df.dropna(how='all', inplace=True)
df.to_csv(r"D:\Claude Project\MEBU Database\lab_results_sample.csv", index=False)
print("CSV saved successfully. Shape:", df.shape)
