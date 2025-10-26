import streamlit as st
import pandas as pd

def display_expiry_alerts(data, days_threshold=7):
    """Display expiry alerts for products"""
    today = pd.Timestamp.now()
    expiring_soon = data[data['days_until_expiry'] <= days_threshold]
    
    if not expiring_soon.empty:
        st.error(f"**Products Expiring in {days_threshold} days:**")
        for _, product in expiring_soon.iterrows():
            st.write(f"🔴 {product['product']} - {product['days_until_expiry']} days left")
    else:
        st.success("✅ No expiry alerts")

def display_promotion_effectiveness(data):
    """Analyze promotion effectiveness"""
    promoted = data[data['promotion_discount'] > 0]
    regular = data[data['promotion_discount'] == 0]
    
    if not promoted.empty and not regular.empty:
        promo_sales = promoted['sold_today'].mean()
        regular_sales = regular['sold_today'].mean()
        
        effectiveness = ((promo_sales - regular_sales) / regular_sales) * 100
        
        st.metric("Promotion Effectiveness", f"{effectiveness:.1f}%", 
                 delta=f"{promo_sales - regular_sales:.1f} units")