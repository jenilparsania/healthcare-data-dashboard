import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("=== HEALTHCARE WAIT TIMES DASHBOARD ===\n")

# Load the merged data
df = pd.read_csv('merged_wait_times_nova_scotia.csv')
print(f"Loaded data shape: {df.shape}")
print(f"Data columns: {list(df.columns)}")

# Clean and prepare data
df['Year'] = df['Year'].astype(int)
df = df.sort_values('Year')

print(f"\nData range: {df['Year'].min()} - {df['Year'].max()}")
print(f"Available data sources:")
print(f"- Fraser Institute: {df['Fraser_Wait_Time_Days'].notna().sum()} years")
print(f"- CIHI: {df['CIHI_Surgery_Median_Days'].notna().sum()} years")

# Create comprehensive dashboard
def create_dashboard():
    """Create a comprehensive dashboard with multiple visualizations"""
    
    # 1. Time Series Analysis
    fig1 = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Fraser Institute Wait Times (2008-2024)', 
                       'Wait Time Trends by Decade',
                       'Year-over-Year Changes',
                       'Data Availability'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Fraser Institute wait times
    fraser_data = df.dropna(subset=['Fraser_Wait_Time_Days'])
    fig1.add_trace(
        go.Scatter(x=fraser_data['Year'], y=fraser_data['Fraser_Wait_Time_Days'],
                  mode='lines+markers', name='Fraser Institute',
                  line=dict(color='blue', width=3),
                  marker=dict(size=8)),
        row=1, col=1
    )
    
    # Add trend line
    z = np.polyfit(fraser_data['Year'], fraser_data['Fraser_Wait_Time_Days'], 1)
    p = np.poly1d(z)
    fig1.add_trace(
        go.Scatter(x=fraser_data['Year'], y=p(fraser_data['Year']),
                  mode='lines', name='Trend Line',
                  line=dict(color='red', width=2, dash='dash')),
        row=1, col=1
    )
    
    # Decade analysis
    fraser_data['Decade'] = (fraser_data['Year'] // 10) * 10
    decade_avg = fraser_data.groupby('Decade')['Fraser_Wait_Time_Days'].mean().reset_index()
    fig1.add_trace(
        go.Bar(x=decade_avg['Decade'], y=decade_avg['Fraser_Wait_Time_Days'],
               name='Decade Average', marker_color='lightblue'),
        row=1, col=2
    )
    
    # Year-over-year changes
    fraser_data['YoY_Change'] = fraser_data['Fraser_Wait_Time_Days'].diff()
    fig1.add_trace(
        go.Bar(x=fraser_data['Year'][1:], y=fraser_data['YoY_Change'][1:],
               name='Year-over-Year Change', marker_color='orange'),
        row=2, col=1
    )
    
    # Data availability
    availability = df[['Year', 'Fraser_Wait_Time_Days', 'CIHI_Surgery_Median_Days']].notna().sum(axis=1)
    fig1.add_trace(
        go.Bar(x=df['Year'], y=availability,
               name='Data Sources Available', marker_color='green'),
        row=2, col=2
    )
    
    fig1.update_layout(height=800, title_text="Nova Scotia Healthcare Wait Times Analysis")
    fig1.show()
    
    # 2. Statistical Summary
    print("\n" + "="*60)
    print("STATISTICAL SUMMARY")
    print("="*60)
    
    print("\nFraser Institute Wait Times (2008-2024):")
    print(f"Mean: {fraser_data['Fraser_Wait_Time_Days'].mean():.1f} days")
    print(f"Median: {fraser_data['Fraser_Wait_Time_Days'].median():.1f} days")
    print(f"Standard Deviation: {fraser_data['Fraser_Wait_Time_Days'].std():.1f} days")
    print(f"Min: {fraser_data['Fraser_Wait_Time_Days'].min():.1f} days")
    print(f"Max: {fraser_data['Fraser_Wait_Time_Days'].max():.1f} days")
    
    # 3. Trend Analysis
    print("\nTrend Analysis:")
    recent_5y = fraser_data[fraser_data['Year'] >= 2020]
    older_5y = fraser_data[fraser_data['Year'] <= 2014]
    
    print(f"Recent 5 years (2020-2024) average: {recent_5y['Fraser_Wait_Time_Days'].mean():.1f} days")
    print(f"Previous 5 years (2010-2014) average: {older_5y['Fraser_Wait_Time_Days'].mean():.1f} days")
    print(f"Change: {((recent_5y['Fraser_Wait_Time_Days'].mean() - older_5y['Fraser_Wait_Time_Days'].mean()) / older_5y['Fraser_Wait_Time_Days'].mean() * 100):.1f}%")
    
    # 4. Create comparison chart (if CIHI data becomes available)
    if df['CIHI_Surgery_Median_Days'].notna().any():
        fig2 = go.Figure()
        
        cihi_data = df.dropna(subset=['CIHI_Surgery_Median_Days'])
        
        fig2.add_trace(go.Scatter(
            x=fraser_data['Year'], y=fraser_data['Fraser_Wait_Time_Days'],
            mode='lines+markers', name='Fraser Institute',
            line=dict(color='blue', width=3)
        ))
        
        fig2.add_trace(go.Scatter(
            x=cihi_data['Year'], y=cihi_data['CIHI_Surgery_Median_Days'],
            mode='lines+markers', name='CIHI',
            line=dict(color='red', width=3)
        ))
        
        fig2.update_layout(
            title="Wait Time Comparison: Fraser Institute vs CIHI",
            xaxis_title="Year",
            yaxis_title="Wait Time (Days)",
            height=500
        )
        fig2.show()
    
    # 5. Save summary statistics
    summary_stats = {
        'Metric': ['Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Recent 5Y Avg', 'Previous 5Y Avg'],
        'Value': [
            fraser_data['Fraser_Wait_Time_Days'].mean(),
            fraser_data['Fraser_Wait_Time_Days'].median(),
            fraser_data['Fraser_Wait_Time_Days'].std(),
            fraser_data['Fraser_Wait_Time_Days'].min(),
            fraser_data['Fraser_Wait_Time_Days'].max(),
            recent_5y['Fraser_Wait_Time_Days'].mean(),
            older_5y['Fraser_Wait_Time_Days'].mean()
        ]
    }
    
    summary_df = pd.DataFrame(summary_stats)
    summary_df.to_csv('wait_times_summary_stats.csv', index=False)
    print(f"\nSummary statistics saved to 'wait_times_summary_stats.csv'")

if __name__ == "__main__":
    create_dashboard()
