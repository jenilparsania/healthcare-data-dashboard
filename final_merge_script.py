import pandas as pd
import numpy as np

print("=== FINAL MERGE: CIHI AND FRASER INSTITUTE WAIT TIMES ===\n")

# 1. Load and clean CIHI data
print("1. LOADING CIHI DATA")
print("-" * 50)
cihi_df = pd.read_csv('Surgical_Wait_Times.csv')

# Clean CIHI data - focus on meaningful rows
cihi_clean = cihi_df.dropna(subset=['Specialty', 'Procedure'])
print(f"CIHI original shape: {cihi_df.shape}")
print(f"CIHI cleaned shape: {cihi_clean.shape}")

# Show sample of cleaned CIHI data
print("\nSample CIHI data:")
print(cihi_clean[['Period', 'Specialty', 'Procedure', 'Zone', 'Year', 'Surgery_Median']].head())

print("\n" + "="*100 + "\n")

# 2. Load and clean Fraser Institute data
print("2. LOADING FRASER INSTITUTE DATA")
print("-" * 50)

# Read raw data to find the actual data rows
fraser_raw = pd.read_excel('wait-times-priority-procedures-in-canada-2025-data-tables-en.xlsx', 
                          sheet_name=1, header=None)

# Find the row that contains the actual column headers
header_row = None
for i in range(len(fraser_raw)):
    row = fraser_raw.iloc[i]
    if any(str(cell).strip() == 'Province' for cell in row if pd.notna(cell)):
        header_row = i
        break

if header_row is not None:
    print(f"Found header at row {header_row}")
    
    # Read with proper header
    fraser_df = pd.read_excel('wait-times-priority-procedures-in-canada-2025-data-tables-en.xlsx', 
                             sheet_name=1, header=header_row)
    
    print(f"Fraser Institute data shape: {fraser_df.shape}")
    print(f"Fraser Institute columns: {list(fraser_df.columns)}")
    
    # Clean the data - remove rows with missing province
    fraser_clean = fraser_df.dropna(subset=['Province'])
    print(f"Fraser Institute cleaned shape: {fraser_clean.shape}")
    
    print("\nSample Fraser Institute data:")
    print(fraser_clean.head())
    
    # Show unique provinces
    print(f"\nFraser Institute provinces: {fraser_clean['Province'].unique()}")
    
    # Handle year column properly
    year_col = 'Data year'
    print(f"\nYear column: {year_col}")
    
    # Convert year to numeric and handle mixed types
    fraser_clean[year_col] = pd.to_numeric(fraser_clean[year_col], errors='coerce')
    valid_years = fraser_clean[year_col].dropna().unique()
    print(f"Fraser Institute years: {sorted(valid_years)}")
    
    # Show data structure
    print(f"\nFraser Institute data types:")
    print(fraser_clean.dtypes)
    
    print(f"\nFraser Institute sample values by column:")
    for col in fraser_clean.columns:
        unique_vals = fraser_clean[col].dropna().unique()[:3]
        print(f"{col}: {unique_vals}")
    
else:
    print("Could not find proper header row")
    fraser_clean = None

print("\n" + "="*100 + "\n")

# 3. Data standardization and merging
print("3. DATA STANDARDIZATION AND MERGING")
print("-" * 50)

if fraser_clean is not None:
    # Standardize province names
    print("Standardizing province names...")
    
    # Create province mapping for CIHI zones to standard province names
    # Based on the zones we saw: Zone 1, Zone 2, Zone 3, Zone 4, IWK, Total
    # These appear to be Nova Scotia health zones
    zone_to_province = {
        'Zone 1': 'Nova Scotia',
        'Zone 2': 'Nova Scotia', 
        'Zone 3': 'Nova Scotia',
        'Zone 4': 'Nova Scotia',
        'IWK': 'Nova Scotia',
        'Total': 'Nova Scotia'
    }
    
    # Add province column to CIHI data
    cihi_clean['Province'] = cihi_clean['Zone'].map(zone_to_province)
    
    # Filter to only include Nova Scotia data for comparison
    cihi_ns = cihi_clean[cihi_clean['Province'] == 'Nova Scotia'].copy()
    
    print(f"CIHI Nova Scotia data shape: {cihi_ns.shape}")
    
    # Create summary statistics for CIHI
    print("\nCIHI Nova Scotia Summary by Year:")
    cihi_summary = cihi_ns.groupby('Year')['Surgery_Median'].agg(['mean', 'median', 'count']).round(1)
    print(cihi_summary)
    
    # Create summary statistics for Fraser Institute
    print("\nFraser Institute Nova Scotia Summary:")
    fraser_ns = fraser_clean[fraser_clean['Province'] == 'Nova Scotia'].copy()
    if not fraser_ns.empty:
        # Find the indicator result column (actual wait time values)
        result_col = 'Indicator result'
        
        # Convert result to numeric
        fraser_ns[result_col] = pd.to_numeric(fraser_ns[result_col], errors='coerce')
        
        # Filter out invalid data
        fraser_ns_clean = fraser_ns.dropna(subset=[result_col, year_col])
        
        if not fraser_ns_clean.empty:
            fraser_summary = fraser_ns_clean.groupby(year_col)[result_col].agg(['mean', 'median', 'count']).round(1)
            print(fraser_summary)
            
            # Show sample of Fraser Institute Nova Scotia data
            print(f"\nSample Fraser Institute Nova Scotia data:")
            print(fraser_ns_clean[['Province', year_col, 'Indicator', 'Metric', result_col]].head(10))
        else:
            print("No valid wait time data found in Fraser Institute Nova Scotia data")
    else:
        print("No Nova Scotia data found in Fraser Institute dataset")
    
    # Merge the datasets
    print("\n" + "="*100)
    print("4. MERGING DATASETS")
    print("-" * 50)
    
    # Prepare CIHI data for merging
    cihi_merge = cihi_ns.groupby(['Province', 'Year']).agg({
        'Surgery_Median': 'mean',
        'Surgery_90th': 'mean'
    }).reset_index()
    cihi_merge.columns = ['Province', 'Year', 'CIHI_Surgery_Median_Days', 'CIHI_Surgery_90th_Days']
    
    print("CIHI data prepared for merging:")
    print(cihi_merge)
    
    # Prepare Fraser Institute data for merging
    if not fraser_ns.empty and not fraser_ns_clean.empty:
        fraser_merge = fraser_ns_clean.groupby(['Province', year_col]).agg({
            result_col: 'mean'
        }).reset_index()
        fraser_merge.columns = ['Province', 'Year', 'Fraser_Wait_Time_Days']
        
        print("\nFraser Institute data prepared for merging:")
        print(fraser_merge)
        
        # Merge the datasets
        merged_data = pd.merge(cihi_merge, fraser_merge, on=['Province', 'Year'], how='outer')
        
        print(f"\nMerged data shape: {merged_data.shape}")
        print("\nMerged data:")
        print(merged_data)
        
        # Save merged data
        merged_data.to_csv('merged_wait_times_nova_scotia.csv', index=False)
        print("\nMerged data saved to 'merged_wait_times_nova_scotia.csv'")
        
        # Create comparison analysis
        print("\n" + "="*100)
        print("5. COMPARISON ANALYSIS")
        print("-" * 50)
        
        # Compare wait times where both datasets have data
        comparison = merged_data.dropna()
        if not comparison.empty:
            print("Wait Time Comparison (where both datasets have data):")
            print(comparison)
            
            # Calculate correlation
            correlation = comparison['CIHI_Surgery_Median_Days'].corr(comparison['Fraser_Wait_Time_Days'])
            print(f"\nCorrelation between CIHI and Fraser Institute wait times: {correlation:.3f}")
            
            # Calculate differences
            comparison['Difference_Days'] = comparison['CIHI_Surgery_Median_Days'] - comparison['Fraser_Wait_Time_Days']
            comparison['Percent_Difference'] = (comparison['Difference_Days'] / comparison['Fraser_Wait_Time_Days']) * 100
            
            print(f"\nAverage difference: {comparison['Difference_Days'].mean():.1f} days")
            print(f"Average percent difference: {comparison['Percent_Difference'].mean():.1f}%")
            
            # Save comparison data
            comparison.to_csv('wait_time_comparison.csv', index=False)
            print("\nComparison data saved to 'wait_time_comparison.csv'")
        else:
            print("No overlapping data found for comparison")
    else:
        print("No Fraser Institute data available for Nova Scotia")
else:
    print("Could not process Fraser Institute data")

print("\n" + "="*100)
print("MERGE COMPLETE")
print("="*100) 