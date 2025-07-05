import pandas as pd
import numpy as np

print("=== DETAILED DATA INSPECTION AND CLEANING ===\n")

# 1. CIHI Data (CSV)
print("1. CIHI SURGICAL WAIT TIMES DATA")
print("-" * 50)
cihi_df = pd.read_csv('Surgical_Wait_Times.csv')
print(f"Shape: {cihi_df.shape}")
print(f"Columns: {list(cihi_df.columns)}")

# Show more detailed info about CIHI data
print(f"\nYears available: {sorted(cihi_df['Year'].unique())}")
print(f"Zones available: {cihi_df['Zone'].unique()}")
print(f"Periods available: {cihi_df['Period'].unique()}")

# Show sample of actual data (not NaN)
print("\nSample CIHI data (non-NaN rows):")
non_nan_cihi = cihi_df.dropna(subset=['Specialty', 'Procedure'])
print(non_nan_cihi.head(10))

print("\n" + "="*80 + "\n")

# 2. Fraser Institute Data (Excel)
print("2. FRASER INSTITUTE DATA")
print("-" * 50)

# Read Excel with different approaches
try:
    # Try reading with header=None to see raw data
    fraser_raw = pd.read_excel('wait-times-priority-procedures-in-canada-2025-data-tables-en.xlsx', 
                              sheet_name=1, header=None)
    print(f"Raw Excel shape: {fraser_raw.shape}")
    print("First 10 rows of raw data:")
    print(fraser_raw.head(10))
    
    # Look for the actual data rows (skip header rows)
    print("\nLooking for data patterns...")
    for i in range(min(20, len(fraser_raw))):
        row = fraser_raw.iloc[i]
        if any(str(cell).strip() in ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 
                                    'Newfoundland and Labrador', 'Nova Scotia', 'Ontario', 
                                    'Prince Edward Island', 'Quebec', 'Saskatchewan'] for cell in row if pd.notna(cell)):
            print(f"Row {i}: {list(row)}")
            break
    
    # Try to find the header row and data
    print("\nAttempting to find proper header...")
    for i in range(min(50, len(fraser_raw))):
        row = fraser_raw.iloc[i]
        if any('province' in str(cell).lower() for cell in row if pd.notna(cell)):
            print(f"Potential header at row {i}: {list(row)}")
            # Try reading with this as header
            try:
                fraser_clean = pd.read_excel('wait-times-priority-procedures-in-canada-2025-data-tables-en.xlsx', 
                                           sheet_name=1, header=i)
                print(f"Successfully read with header row {i}")
                print(f"Cleaned shape: {fraser_clean.shape}")
                print("Cleaned columns:", list(fraser_clean.columns))
                print("First 5 rows of cleaned data:")
                print(fraser_clean.head())
                break
            except:
                continue
                
except Exception as e:
    print(f"Error processing Excel: {e}")

print("\n" + "="*80 + "\n")

# 3. Summary for merging
print("3. MERGING ANALYSIS")
print("-" * 50)
print("CIHI Data:")
print(f"- Has 'Year' column: {cihi_df['Year'].unique()}")
print(f"- Has 'Zone' column (provinces): {cihi_df['Zone'].unique()}")
print(f"- Wait time columns: Consult_Median, Consult_90th, Surgery_Median, Surgery_90th")
print(f"- Units: Likely days (based on typical surgical wait times)")

print("\nFraser Institute Data:")
print("- Need to identify province and year columns")
print("- Need to identify wait time columns")
print("- Need to determine units")

print("\nNext steps:")
print("1. Clean Fraser Institute data to identify proper columns")
print("2. Standardize province names between datasets")
print("3. Standardize wait time units")
print("4. Merge on province and year") 