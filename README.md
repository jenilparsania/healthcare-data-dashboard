# 🏥 Nova Scotia Healthcare Wait Times Dashboard

A comprehensive analysis and visualization tool for healthcare wait times in Nova Scotia, combining data from the Fraser Institute (2008-2024) and CIHI (2023-2025).

## 📊 Project Overview

This project analyzes healthcare accessibility in Nova Scotia by examining wait times for surgical procedures. The analysis combines two major data sources:

- **Fraser Institute Data**: Comprehensive wait time data from 2008-2024
- **CIHI Data**: Surgical wait times from 2023-2025

## 🗂️ Project Structure

```
healthcare dashboard/
├── 📁 Data Files
│   ├── Surgical_Wait_Times.csv          # CIHI surgical wait times
│   ├── wait-times-priority-procedures-in-canada-2025-data-tables-en.xlsx  # Fraser Institute data
│   ├── merged_wait_times_nova_scotia.csv # Final merged dataset
│   └── waiting-your-turn-2024.pdf       # Fraser Institute report
│
├── 🐍 Analysis Scripts
│   ├── final_merge_script.py            # Main data merging script
│   ├── merge_wait_times_fixed.py        # Alternative merge approach
│   ├── clean_and_inspect.py             # Data cleaning utilities
│   ├── inspect_data.py                  # Data inspection tools
│   └── inspect_data_detailed.py         # Detailed data analysis
│
├── 📈 Dashboard Files
│   ├── create_dashboard.py              # Static dashboard with Plotly
│   ├── web_dashboard.py                 # Interactive Streamlit dashboard
│   └── requirements.txt                 # Python dependencies
│
└── 📝 Documentation
    ├── README.md                        # This file
    └── notes.txt                        # Project notes and findings
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Interactive Dashboard

```bash
streamlit run web_dashboard.py
```

This will open a web-based dashboard in your browser with interactive visualizations and filters.

### 3. Run Static Analysis

```bash
python create_dashboard.py
```

This generates static charts and saves summary statistics.

## 📈 Key Features

### Interactive Dashboard
- **Time Series Analysis**: Visualize wait time trends over 17 years
- **Statistical Summary**: Key metrics and insights
- **Decade Analysis**: Compare wait times across different periods
- **Year-over-Year Changes**: Track annual variations
- **Data Filtering**: Interactive year range selection
- **Data Export**: Download filtered data as CSV

### Data Analysis
- **Multi-source Integration**: Combines Fraser Institute and CIHI data
- **Trend Analysis**: Identifies patterns and changes over time
- **Statistical Modeling**: Linear regression and trend lines
- **Data Quality Checks**: Comprehensive data validation

## 📊 Key Findings

### Fraser Institute Data (2008-2024)
- **Average Wait Time**: ~1,200 days
- **Peak Wait Time**: 2,637 days (2012)
- **Recent Trend**: 939-1,045 days (2022-2024)
- **Data Coverage**: 17 years of continuous data

### Data Gaps and Limitations
- **No Overlapping Years**: CIHI (2023-2025) and Fraser Institute (2008-2024) don't overlap
- **Different Metrics**: Each source uses different measurement methodologies
- **Geographic Scope**: Focus on Nova Scotia health zones

## 🔧 Technical Details

### Data Sources
1. **Fraser Institute**: Annual wait time surveys across Canadian provinces
2. **CIHI**: Canadian Institute for Health Information surgical data
3. **Geographic Focus**: Nova Scotia health zones (Zone 1-4, IWK, Total)

### Data Processing
- **Cleaning**: Removed missing values and standardized formats
- **Standardization**: Unified province names and time periods
- **Merging**: Combined datasets by province and year
- **Validation**: Cross-checked data quality and consistency

### Technologies Used
- **Python**: Core data processing and analysis
- **Pandas**: Data manipulation and cleaning
- **Plotly**: Interactive visualizations
- **Streamlit**: Web dashboard framework
- **NumPy**: Statistical calculations
- **Matplotlib/Seaborn**: Static visualizations

## 📋 Usage Instructions

### For Data Analysts
1. Run `python final_merge_script.py` to regenerate merged data
2. Use `create_dashboard.py` for detailed statistical analysis
3. Export results using the provided CSV files

### For Stakeholders
1. Launch the Streamlit dashboard: `streamlit run web_dashboard.py`
2. Use the sidebar filters to explore specific time periods
3. Download filtered data for further analysis
4. Review key insights and trends

### For Developers
1. Install dependencies: `pip install -r requirements.txt`
2. Modify analysis scripts as needed
3. Add new data sources to the merge process
4. Extend dashboard functionality

## 🔍 Analysis Capabilities

### Trend Analysis
- Long-term wait time patterns (2008-2024)
- Decade-by-decade comparisons
- Year-over-year change tracking
- Statistical trend modeling

### Comparative Analysis
- Multi-source data comparison (when available)
- Geographic variations within Nova Scotia
- Temporal pattern identification
- Benchmark analysis

### Predictive Insights
- Trend projection capabilities
- Seasonal pattern identification
- Anomaly detection
- Performance forecasting

## 📈 Future Enhancements

### Planned Features
- [ ] Real-time data updates
- [ ] Additional data sources integration
- [ ] Machine learning predictions
- [ ] Comparative analysis with other provinces
- [ ] Procedure-specific analysis
- [ ] Interactive mapping features

### Data Expansion
- [ ] Historical CIHI data (pre-2023)
- [ ] Provincial health authority data
- [ ] Patient satisfaction metrics
- [ ] Resource allocation data
- [ ] Demographic breakdowns

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and research purposes. Please ensure proper attribution when using the data or analysis.

## 📞 Contact

For questions or collaboration opportunities, please refer to the project documentation or create an issue in the repository.

---

**Last Updated**: December 2024  
**Data Sources**: Fraser Institute, CIHI  
**Analysis Period**: 2008-2024
