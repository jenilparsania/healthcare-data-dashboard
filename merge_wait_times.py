import pandas as pd
import numpy as np

print("=== MERGING CIHI AND FRASER INSTITUTE WAIT TIMES ===\n")

# 1. Load and clean CIHI data
print("1. LOADING CIHI DATA")
print("-" * 40)
cihi_df = pd.read_csv('Surgical_Wait_Times.csv')

# Clean CIHI data - focus on meaningful rows
cihi_clean = cihi_df.dropna(subset=['Specialty', 'Procedure'])
print(f"CIHI original shape: {cihi_df.shape}")
print(f"CIHI cleaned shape: {cihi_clean.shape}")

# Show sample of cleaned CIHI data
print("\nSample CIHI data:")
print(cihi_clean[['Period', 'Specialty', 'Procedure', 'Zone', 'Year', 'Surgery_Median']].head())

print("\n" + "="*80 + "\n")

# 2. Load and clean Fraser Institute data
print("2. LOADING FRASER INSTITUTE DATA")
print("-" * 40)

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
    
    # Show unique provinces and years
    print(f"\nFraser Institute provinces: {fraser_clean['Province'].unique()}")
    print(f"Fraser Institute years: {sorted(fraser_clean['Year'].unique())}")
    
else:
    print("Could not find proper header row")
    fraser_clean = None

print("\n" + "="*80 + "\n")

# 3. Data standardization and merging
print("3. DATA STANDARDIZATION AND MERGING")
print("-" * 40)

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
    
    # Standardize wait time units (both appear to be in days)
    print("\nStandardizing wait time units...")
    
    # Fraser Institute data appears to be in days
    # CIHI data appears to be in days
    # No conversion needed, but let's verify
    
    # Create summary statistics for comparison
    print("\nCIHI Nova Scotia Summary:")
    cihi_summary = cihi_ns.groupby('Year')['Surgery_Median'].agg(['mean', 'median', 'count']).round(1)
    print(cihi_summary)
    
    print("\nFraser Institute Nova Scotia Summary:")
    fraser_ns = fraser_clean[fraser_clean['Province'] == 'Nova Scotia'].copy()
    if not fraser_ns.empty:
        fraser_summary = fraser_ns.groupby('Year').agg({
            '50th Percentile': ['mean', 'median', 'count']
        }).round(1)
        print(fraser_summary)
    else:
        print("No Nova Scotia data found in Fraser Institute dataset")
    
    # Merge the datasets
    print("\nMerging datasets...")
    
    # Prepare CIHI data for merging
    cihi_merge = cihi_ns.groupby(['Province', 'Year']).agg({
        'Surgery_Median': 'mean',
        'Surgery_90th': 'mean'
    }).reset_index()
    cihi_merge.columns = ['Province', 'Year', 'CIHI_Surgery_Median_Days', 'CIHI_Surgery_90th_Days']
    
    # Prepare Fraser Institute data for merging
    if not fraser_ns.empty:
        fraser_merge = fraser_ns.groupby(['Province', 'Year']).agg({
            '50th Percentile': 'mean',
            '90th Percentile': 'mean'
        }).reset_index()
        fraser_merge.columns = ['Province', 'Year', 'Fraser_50th_Percentile_Days', 'Fraser_90th_Percentile_Days']
        
        # Merge the datasets
        merged_data = pd.merge(cihi_merge, fraser_merge, on=['Province', 'Year'], how='outer')
        
        print(f"Merged data shape: {merged_data.shape}")
        print("\nMerged data:")
        print(merged_data)
        
        # Save merged data
        merged_data.to_csv('merged_wait_times_nova_scotia.csv', index=False)
        print("\nMerged data saved to 'merged_wait_times_nova_scotia.csv'")
        
        # Create comparison analysis
        print("\n" + "="*80)
        print("4. COMPARISON ANALYSIS")
        print("-" * 40)
        
        # Compare wait times where both datasets have data
        comparison = merged_data.dropna()
        if not comparison.empty:
            print("Wait Time Comparison (where both datasets have data):")
            print(comparison)
            
            # Calculate correlation
            correlation = comparison['CIHI_Surgery_Median_Days'].corr(comparison['Fraser_50th_Percentile_Days'])
            print(f"\nCorrelation between CIHI and Fraser Institute wait times: {correlation:.3f}")
            
            # Calculate differences
            comparison['Difference_Days'] = comparison['CIHI_Surgery_Median_Days'] - comparison['Fraser_50th_Percentile_Days']
            comparison['Percent_Difference'] = (comparison['Difference_Days'] / comparison['Fraser_50th_Percentile_Days']) * 100
            
            print(f"\nAverage difference: {comparison['Difference_Days'].mean():.1f} days")
            print(f"Average percent difference: {comparison['Percent_Difference'].mean():.1f}%")
        else:
            print("No overlapping data found for comparison")
    else:
        print("No Fraser Institute data available for Nova Scotia")
else:
    print("Could not process Fraser Institute data")

print("\n" + "="*80)
print("MERGE COMPLETE")
print("="*80) 