import pandas as pd

# Inspect CSV file
print("=== INSPECTING CSV FILE ===")
try:
    csv_df = pd.read_csv('Surgical_Wait_Times.csv')
    print("CSV Columns:", list(csv_df.columns))
    print("CSV Shape:", csv_df.shape)
    print("\nCSV First 3 rows:")
    print(csv_df.head(3))
    print("\nCSV Data types:")
    print(csv_df.dtypes)
    print("\nCSV Info:")
    print(csv_df.info())
except Exception as e:
    print(f"Error reading CSV: {e}")

print("\n" + "="*50 + "\n")

# Inspect Excel file
print("=== INSPECTING EXCEL FILE ===")
try:
    excel_df = pd.read_excel('wait-times-priority-procedures-in-canada-2025-data-tables-en.xlsx')
    print("Excel Columns:", list(excel_df.columns))
    print("Excel Shape:", excel_df.shape)
    print("\nExcel First 3 rows:")
    print(excel_df.head(3))
    print("\nExcel Data types:")
    print(excel_df.dtypes)
    print("\nExcel Info:")
    print(excel_df.info())
except Exception as e:
    print(f"Error reading Excel: {e}")

# If Excel has multiple sheets, let's check
try:
    excel_file = pd.ExcelFile('wait-times-priority-procedures-in-canada-2025-data-tables-en.xlsx')
    print(f"\nExcel sheets: {excel_file.sheet_names}")
    
    # Check first sheet specifically
    if excel_file.sheet_names:
        first_sheet = pd.read_excel('wait-times-priority-procedures-in-canada-2025-data-tables-en.xlsx', sheet_name=0)
        print(f"\nFirst sheet '{excel_file.sheet_names[0]}' columns:", list(first_sheet.columns))
        print(f"First sheet shape: {first_sheet.shape}")
        print("\nFirst sheet first 3 rows:")
        print(first_sheet.head(3))
except Exception as e:
    print(f"Error reading Excel sheets: {e}") 