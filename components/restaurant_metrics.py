import streamlit as st
import plotly.express as px

def display_demand_metrics(data):
    """Display demand forecasting metrics"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_demand = data['demand'].mean()
        st.metric("Average Daily Demand", f"{avg_demand:.0f} orders")
    
    with col2:
        peak_demand = data['demand'].max()
        st.metric("Peak Demand", f"{peak_demand} orders")
    
    with col3:
        demand_variance = data['demand'].std()
        st.metric("Demand Variability", f"{demand_variance:.1f}")

def display_waste_alerts(data):
    """Display waste-related alerts"""
    high_waste_items = data[data['waste_kg'] > data['waste_kg'].quantile(0.8)]
    
    if not high_waste_items.empty:
        st.warning("**High Waste Items Detected:**")
        for _, item in high_waste_items.head(3).iterrows():
            st.write(f"⚠️ {item['dish']}: {item['waste_kg']}kg waste")