# Forecasting Financial Inclusion in Ethiopia

## 📋 Project Overview
A comprehensive time-series forecasting system to predict Ethiopia's progress in financial inclusion for 2025-2027. This project analyzes account ownership (Access) and digital payment adoption (Usage) while modeling the impact of policy changes, product launches, and infrastructure investments.

**Challenge Period**: 28 Jan 2026 - 03 Feb 2026  
**Organization**: 10 Academy - Artificial Intelligence Mastery (Week 10 Challenge)

## 🎯 Business Context
Ethiopia is undergoing rapid digital financial transformation with Telebirr (54M+ users) and M-Pesa (10M+ users), yet only 49% of adults have financial accounts (Global Findex 2024). Stakeholders including the National Bank of Ethiopia, mobile money operators, and development finance institutions need to understand:
- What drives financial inclusion in Ethiopia
- How events affect inclusion outcomes  
- Future trajectories for 2026-2027

## 📊 Key Metrics
- **Access**: Account ownership rate (% adults with financial/mobile money account)
- **Usage**: Digital payment adoption rate (% adults making/receiving digital payments)

## 🗂️ Project Structure
```bash
ethiopia-fi-forecast/
├── data/                    # Data storage
│   ├── raw/                # Original datasets
│   └── processed/          # Enriched and cleaned data
├── notebooks/              # Jupyter notebooks for each task
├── src/                    # Python source code
├── dashboards/             # Interactive dashboard files
├── reports/                # Analysis reports and documentation
├── scripts/                # Utility scripts
└── tests/                  # Test files
```


## 📈 Tasks Overview
1. **Data Exploration & Enrichment** - Understand schema, add relevant observations/events
2. **EDA & Insight Generation** - Analyze trends, gaps, correlations
3. **Event Impact Modeling** - Quantify how events affect indicators  
4. **Forecasting** - Predict Access and Usage rates (2025-2027)
5. **Dashboard Development** - Interactive Streamlit app for stakeholders

## 🔧 Technology Stack
- **Python**: pandas, numpy, statsmodels, scikit-learn
- **Visualization**: matplotlib, seaborn, plotly
- **Dashboard**: Streamlit
- **Version Control**: Git, GitHub
- **Methodology**: Time series analysis, regression modeling, event impact estimation

## 📁 Core Datasets
- `ethiopia_fi_unified_data.csv` - Unified financial inclusion records
- `reference_codes.csv` - Valid values for categorical fields
- **Enriched with**: IMF FAS, GSMA, NBE reports, ITU indicators, Findex microdata

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.8+
Git
```

### Installation
```bash
# Clone repository
git clone https://github.com/Jaki77/ethiopia-fi-forecast.git
cd ethiopia-fi-forecast

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

