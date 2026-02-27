import pandas as pd
import openpyxl

file_path = r"D:\Claude Project\MEBU Database\EXPERIMENT DATA\04_Master_MEBU Result (Repeat Acceptance Test)_Feb-Mar'26.xlsx"
wb = openpyxl.load_workbook(file_path, data_only=True)
sheet = wb['Lab Results Summary']

print("Extracting values from Lab Results Summary sheet to understand graph data...")
# Look at rows where data might be
# We know from before that there are only a few populated rows in this sheet
for row in sheet.iter_rows(min_row=1, max_row=40, values_only=True):
    if any(row):
        print(row)
        
# Try to find chart objects
if sheet._charts:
    print("\nFound Charts in Lab Results Summary:")
    for chart in sheet._charts:
        print(f"Chart Type: {type(chart)}")
        print(f"Title: {chart.title.tx.rich.p[0].r[0].t if chart.title else 'No Title'}")
        print("Series:")
        for series in chart.series:
            try:
                # Try to get the name of the series
                name = series.tx.strRef.f if series.tx and getattr(series.tx, 'strRef', None) else (series.tx.v if series.tx else "Unknown")
                print(f"  - {name}")
            except Exception as e:
                print(f"  - Could not parse series name: {e}")
else:
    print("\nNo charts found via openpyxl.")
