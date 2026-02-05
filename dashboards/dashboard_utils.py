"""
Utility functions for the Ethiopia Financial Inclusion Dashboard
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
from pathlib import Path

def load_forecast_data(data_dir="../data/processed"):
    """Load forecast data with error handling."""
    try:
        account_forecast = pd.read_csv(Path(data_dir) / "forecast_table_ACC_OWNERSHIP.csv")
        payment_forecast = pd.read_csv(Path(data_dir) / "forecast_table_USG_DIGITAL_PAYMENT.csv")
        return account_forecast, payment_forecast
    except FileNotFoundError:
        # Return sample data if files don't exist
        account_forecast = pd.DataFrame({
            'Year': [2025, 2026, 2027],
            'Base Forecast (%)': [52.5, 55.8, 58.2],
            '80% CI Lower (%)': [50.1, 52.8, 54.9],
            '80% CI Upper (%)': [54.9, 58.8, 61.5],
            'Optimistic Scenario (%)': [54.2, 58.1, 62.3],
            'Pessimistic Scenario (%)': [50.8, 53.5, 56.1]
        })
        
        payment_forecast = pd.DataFrame({
            'Year': [2025, 2026, 2027],
            'Base Forecast (%)': [40.2, 44.5, 48.3],
            '80% CI Lower (%)': [38.1, 41.8, 45.2],
            '80% CI Upper (%)': [42.3, 47.2, 51.4],
            'Optimistic Scenario (%)': [42.5, 47.8, 53.2],
            'Pessimistic Scenario (%)': [38.1, 41.2, 44.5]
        })
        
        return account_forecast, payment_forecast

def create_forecast_chart(historical_data, forecast_data, title, target_line=None):
    """Create a forecast chart with historical and forecast data."""
    fig = go.Figure()
    
    # Add historical data
    if historical_data is not None and not historical_data.empty:
        fig.add_trace(go.Scatter(
            x=historical_data['Year'],
            y=historical_data['Value'],
            mode='lines+markers',
            name='Historical',
            line=dict(color='black', width=2),
            marker=dict(size=8)
        ))
    
    # Add forecast
    if forecast_data is not None and not forecast_data.empty:
        fig.add_trace(go.Scatter(
            x=forecast_data['Year'],
            y=forecast_data['Base Forecast (%)'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='blue', width=3),
            marker=dict(size=10)
        ))
        
        # Add confidence interval if available
        if '80% CI Lower (%)' in forecast_data.columns and '80% CI Upper (%)' in forecast_data.columns:
            fig.add_trace(go.Scatter(
                x=forecast_data['Year'].tolist() + forecast_data['Year'].tolist()[::-1],
                y=forecast_data['80% CI Upper (%)'].tolist() + forecast_data['80% CI Lower (%)'].tolist()[::-1],
                fill='toself',
                fillcolor='rgba(0, 100, 255, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='80% Confidence Interval',
                showlegend=True
            ))
    
    # Add target line if provided
    if target_line is not None:
        fig.add_hline(y=target_line, line_dash="dash", line_color="red",
                     annotation_text=f"Target: {target_line}%", 
                     annotation_position="top right")
    
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="Percentage (%)",
        height=400,
        hovermode="x unified",
        template="plotly_white"
    )
    
    return fig

def calculate_growth_metrics(current_value, forecast_values, years):
    """Calculate growth metrics from forecast."""
    if len(forecast_values) < 2:
        return {}
    
    total_growth = forecast_values[-1] - current_value
    annual_growth = total_growth / len(years)
    cagr = ((forecast_values[-1] / current_value) ** (1/len(years)) - 1) * 100
    
    return {
        'total_growth_pp': total_growth,
        'annual_growth_pp': annual_growth,
        'cagr_percent': cagr,
        'doubling_time': 72 / cagr if cagr > 0 else None
    }

def generate_scenario_data(base_forecast, optimistic_multiplier=1.2, pessimistic_multiplier=0.8):
    """Generate optimistic and pessimistic scenarios from base forecast."""
    optimistic = base_forecast.copy()
    pessimistic = base_forecast.copy()
    
    if 'Base Forecast (%)' in base_forecast.columns:
        optimistic['Base Forecast (%)'] = base_forecast['Base Forecast (%)'] * optimistic_multiplier
        pessimistic['Base Forecast (%)'] = base_forecast['Base Forecast (%)'] * pessimistic_multiplier
    
    return optimistic, pessimistic

def format_percentage(value, decimals=1):
    """Format a value as percentage string."""
    return f"{value:.{decimals}f}%"

def create_metric_card(title, value, delta=None, delta_color="normal"):
    """Create HTML for a metric card."""
    delta_html = ""
    if delta:
        delta_sign = "+" if delta > 0 else ""
        delta_class = "delta-positive" if delta_color == "normal" else "delta-negative"
        delta_html = f'<div class="{delta_class}">{delta_sign}{delta}</div>'
    
    return f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """

def save_dashboard_state(state, filename="dashboard_state.json"):
    """Save dashboard state to JSON file."""
    with open(filename, 'w') as f:
        json.dump(state, f)

def load_dashboard_state(filename="dashboard_state.json"):
    """Load dashboard state from JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}