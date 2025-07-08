import pandas as pd

# Inspect CSV file (CIHI data)
print("=== CIHI SURGICAL WAIT TIMES (CSV) ===")
csv_df = pd.read_csv('Surgical_Wait_Times.csv')
print("Columns:", list(csv_df.columns))
print("Shape:", csv_df.shape)
print("\nSample data (first 5 rows):")
print(csv_df.head())
print("\nUnique values in key columns:")
print("Period:", csv_df['Period'].unique()[:10])  # First 10 unique periods
print("Year:", sorted(csv_df['Year'].unique()))
print("Zone:", csv_df['Zone'].unique())
print("Specialty:", csv_df['Specialty'].unique()[:10])  # First 10 specialties

print("\n" + "="*80 + "\n")

# Inspect Excel file - Table 1 (Fraser Institute data)
print("=== FRASER INSTITUTE DATA (Excel - Table 1) ===")
try:
    # Read the actual data table (sheet 1, which is "Table 1")
    fraser_df = pd.read_excel('wait-times-priority-procedures-in-canada-2025-data-tables-en.xlsx', sheet_name=1)
    print("Columns:", list(fraser_df.columns))
    print("Shape:", fraser_df.shape)
    print("\nSample data (first 5 rows):")
    print(fraser_df.head())
    print("\nData types:")
    print(fraser_df.dtypes)
    
    # Check for province and year columns
    print("\nLooking for province/region columns:")
    province_cols = [col for col in fraser_df.columns if any(word in col.lower() for word in ['province', 'region', 'jurisdiction', 'location'])]
    print("Potential province columns:", province_cols)
    
    print("\nLooking for year columns:")
    year_cols = [col for col in fraser_df.columns if any(word in col.lower() for word in ['year', 'date', 'period'])]
    print("Potential year columns:", year_cols)
    
    print("\nLooking for wait time columns:")
    wait_cols = [col for col in fraser_df.columns if any(word in col.lower() for word in ['wait', 'time', 'median', 'days', 'weeks'])]
    print("Potential wait time columns:", wait_cols)
    
except Exception as e:
    print(f"Error reading Excel Table 1: {e}")

print("\n" + "="*80 + "\n")

# Also check if there are any other relevant sheets
print("=== CHECKING OTHER EXCEL SHEETS ===")
excel_file = pd.ExcelFile('wait-times-priority-procedures-in-canada-2025-data-tables-en.xlsx')
print("Available sheets:", excel_file.sheet_names)

# Check methodology notes for any useful information
try:
    methodology = pd.read_excel('wait-times-priority-procedures-in-canada-2025-data-tables-en.xlsx', sheet_name=2)
    print(f"\nMethodology sheet shape: {methodology.shape}")
    print("Methodology first few rows:")
    print(methodology.head(3))
except Exception as e:
    print(f"Error reading methodology sheet: {e}") 