import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Nova Scotia Healthcare Wait Times Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🏥 Nova Scotia Healthcare Wait Times Dashboard")
st.markdown("""
This dashboard analyzes healthcare wait times in Nova Scotia using data from the Fraser Institute (2008-2024) 
and CIHI (2023-2025). Explore trends, patterns, and insights in healthcare accessibility.
""")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('merged_wait_times_nova_scotia.csv')
    df['Year'] = df['Year'].astype(int)
    return df.sort_values('Year')

df = load_data()

# Sidebar filters
st.sidebar.header("📊 Dashboard Filters")

# Year range filter
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=(int(df['Year'].min()), int(df['Year'].max()))
)

# Filter data based on selection
filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

# Main dashboard content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Wait Time Trends")
    
    # Time series chart
    fig = go.Figure()
    
    # Fraser Institute data
    fraser_data = filtered_df.dropna(subset=['Fraser_Wait_Time_Days'])
    if not fraser_data.empty:
        fig.add_trace(go.Scatter(
            x=fraser_data['Year'], 
            y=fraser_data['Fraser_Wait_Time_Days'],
            mode='lines+markers',
            name='Fraser Institute',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        
        # Add trend line
        z = np.polyfit(fraser_data['Year'], fraser_data['Fraser_Wait_Time_Days'], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=fraser_data['Year'], 
            y=p(fraser_data['Year']),
            mode='lines',
            name='Trend Line',
            line=dict(color='red', width=2, dash='dash')
        ))
    
    # CIHI data (if available)
    cihi_data = filtered_df.dropna(subset=['CIHI_Surgery_Median_Days'])
    if not cihi_data.empty:
        fig.add_trace(go.Scatter(
            x=cihi_data['Year'], 
            y=cihi_data['CIHI_Surgery_Median_Days'],
            mode='lines+markers',
            name='CIHI',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title="Healthcare Wait Times Over Time",
        xaxis_title="Year",
        yaxis_title="Wait Time (Days)",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 Key Statistics")
    
    if not fraser_data.empty:
        stats = {
            "Mean Wait Time": f"{fraser_data['Fraser_Wait_Time_Days'].mean():.0f} days",
            "Median Wait Time": f"{fraser_data['Fraser_Wait_Time_Days'].median():.0f} days",
            "Min Wait Time": f"{fraser_data['Fraser_Wait_Time_Days'].min():.0f} days",
            "Max Wait Time": f"{fraser_data['Fraser_Wait_Time_Days'].max():.0f} days",
            "Data Points": f"{len(fraser_data)} years"
        }
        
        for metric, value in stats.items():
            st.metric(metric, value)

# Additional analysis sections
st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.subheader("📊 Decade Analysis")
    
    if not fraser_data.empty:
        fraser_data['Decade'] = (fraser_data['Year'] // 10) * 10
        decade_avg = fraser_data.groupby('Decade')['Fraser_Wait_Time_Days'].mean().reset_index()
        
        fig_decade = px.bar(
            decade_avg, 
            x='Decade', 
            y='Fraser_Wait_Time_Days',
            title="Average Wait Times by Decade",
            labels={'Fraser_Wait_Time_Days': 'Average Wait Time (Days)'}
        )
        fig_decade.update_layout(height=400)
        st.plotly_chart(fig_decade, use_container_width=True)

with col4:
    st.subheader("📈 Year-over-Year Changes")
    
    if len(fraser_data) > 1:
        fraser_data['YoY_Change'] = fraser_data['Fraser_Wait_Time_Days'].diff()
        
        fig_yoy = px.bar(
            x=fraser_data['Year'][1:], 
            y=fraser_data['YoY_Change'][1:],
            title="Year-over-Year Change in Wait Times",
            labels={'x': 'Year', 'y': 'Change in Days'}
        )
        fig_yoy.update_layout(height=400)
        fig_yoy.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_yoy, use_container_width=True)

# Data table
st.markdown("---")
st.subheader("📋 Raw Data")

# Add download button
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 Download filtered data as CSV",
    data=csv,
    file_name=f'wait_times_{year_range[0]}_{year_range[1]}.csv',
    mime='text/csv'
)

# Display data table
st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# Insights section
st.markdown("---")
st.subheader("🔍 Key Insights")

if not fraser_data.empty:
    recent_avg = fraser_data[fraser_data['Year'] >= 2020]['Fraser_Wait_Time_Days'].mean()
    older_avg = fraser_data[fraser_data['Year'] <= 2014]['Fraser_Wait_Time_Days'].mean()
    
    col5, col6, col7 = st.columns(3)
    
    with col5:
        st.info(f"**Recent Trend (2020-2024):** {recent_avg:.0f} days average")
    
    with col6:
        st.info(f"**Historical Average (2010-2014):** {older_avg:.0f} days average")
    
    with col7:
        change_pct = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0
        st.info(f"**Change:** {change_pct:+.1f}%")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Data Sources: Fraser Institute (2008-2024), CIHI (2023-2025)</p>
    <p>Last updated: {}</p>
</div>
""".format(pd.Timestamp.now().strftime("%B %d, %Y")), unsafe_allow_html=True)
