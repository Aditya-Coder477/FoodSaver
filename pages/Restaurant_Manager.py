import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import numpy as np

st.title("🍽️ Restaurant Manager")

# Generate sample data WITH CACHING
@st.cache_data(ttl=3600)
def generate_restaurant_data():
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    dishes = ['Pasta', 'Burger', 'Pizza', 'Salad', 'Steak', 'Chicken', 'Fish', 'Soup']
    
    data = []
    for date in dates:
        for dish in dishes:
            data.append({
                'date': date,
                'dish': dish,
                'demand': random.randint(10, 50),
                'waste_kg': round(random.uniform(0.1, 5.0), 2),
                'inventory_level': random.randint(20, 100),
                'cost': round(random.uniform(5, 25), 2),
                'category': random.choice(['Main', 'Appetizer', 'Dessert'])
            })
    return pd.DataFrame(data)

# Generate donation data
@st.cache_data(ttl=3600)
def generate_donation_data():
    ngos = ['Food Bank Tokyo', 'Second Harvest Japan', 'Hunger Free Japan', 'Local Community Center']
    food_items = ['Prepared Meals', 'Fresh Vegetables', 'Bread & Bakery', 'Dairy Products', 'Fruits']
    
    data = []
    for i in range(20):
        data.append({
            'donation_id': f'DON_{1000 + i}',
            'date': datetime(2024, 1, 1) + timedelta(days=random.randint(1, 30)),
            'ngo_name': random.choice(ngos),
            'food_item': random.choice(food_items),
            'quantity_kg': round(random.uniform(5, 25), 1),
            'status': random.choice(['Completed', 'Scheduled', 'In Transit']),
            'impact_score': random.randint(80, 100),
            'carbon_saved': round(random.uniform(10, 50), 1)
        })
    return pd.DataFrame(data)

# Generate voice log data for restaurant
@st.cache_data(ttl=3600)
def generate_voice_logs_restaurant():
    commands = [
        "Add 20kg pasta to inventory",
        "Report 5kg vegetable waste",
        "Schedule donation for excess bread",
        "Update steak inventory to 15kg",
        "Log 3kg fish spoilage",
        "Order 50kg chicken stock",
        "Record 10kg salad preparation",
        "Mark burger as low inventory"
    ]
    
    data = []
    for i in range(25):
        data.append({
            'timestamp': datetime.now() - timedelta(hours=random.randint(1, 168)),
            'command': random.choice(commands),
            'status': random.choice(['Completed', 'Processing', 'Failed']),
            'confidence': round(random.uniform(0.7, 0.98), 2),
            'user': random.choice(['Chef Yamada', 'Manager Tanaka', 'Staff Sato']),
            'action_type': random.choice(['Inventory Update', 'Waste Report', 'Donation', 'Order'])
        })
    return pd.DataFrame(data)

# Load data
restaurant_data = generate_restaurant_data()
donation_data = generate_donation_data()
voice_logs_restaurant = generate_voice_logs_restaurant()

# Create tabs - ADDED DONATE FOOD TAB
tab1, tab2, tab3, tab4,tab5 = st.tabs([
    "📊 Predictive Demand Analytics",
    "📦 Real-time Inventory Tracking", 
    "🗑️ Waste Tracking & Analytics",
    "❤️ Donate Food",
    "🎤 Voice Log"
])

with tab1:
    st.header("🔮 Predictive Demand Analytics")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Demand Forecast (Next 7 Days)")
        
        @st.cache_data(ttl=1800)
        def generate_forecast_data():
            forecast_dates = pd.date_range(start='2024-02-01', periods=7, freq='D')
            forecast_data = []
            
            for date in forecast_dates:
                for dish in restaurant_data['dish'].unique():
                    forecast_data.append({
                        'date': date,
                        'dish': dish,
                        'predicted_demand': random.randint(15, 60),
                        'confidence': round(random.uniform(0.7, 0.95), 2)
                    })
            return pd.DataFrame(forecast_data)
        
        forecast_df = generate_forecast_data()
        
        fig_forecast = px.line(forecast_df, x='date', y='predicted_demand', color='dish',
                              title="7-Day Demand Forecast by Dish")
        st.plotly_chart(fig_forecast, use_container_width=True)
        # === ADD DELLIT RESTAURANT EXAMPLE HERE ===
        
        st.markdown("---")
        st.subheader("🏢 Dellit Restaurant Example")
        
        # Historical Data Table
        st.markdown("#### Historical Data (3 months)")
        
        historical_data = {
            "Period": ["Monday", "Friday", "Diwali Week", "Monsoon"],
            "Butter Chicken Demand": ["50 kg", "80 kg", "120 kg", "50 kg"]
        }
        
        historical_df = pd.DataFrame(historical_data)
        
        # Display as styled table
        st.markdown(
            """
            <style>
            .historical-table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            .historical-table th, .historical-table td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }
            .historical-table th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
            .historical-table tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        st.table(historical_df)
        
        # AI Prediction Details
        st.markdown("---")
        st.subheader("🤖 AI Prediction for Butter Chicken")
        
        pred_col1, pred_col2 = st.columns(2)
        
        with pred_col1:
            st.markdown(
                """
                <div style='background-color: blue; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;'>
                    <h4 style='margin-top: 0; color: #333;'>Prediction Details</h4>
                    <p><strong>Date:</strong> October 25, 2025 (Friday before Diwali)</p>
                    <p><strong>Base:</strong> 80 kg (Friday average)</p>
                    <p><strong>Diwali Factor:</strong> +35% = 108 kg</p>
                    <p><strong>Weather:</strong> Clear (no reduction)</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with pred_col2:
            st.markdown(
                """
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 10px; color: white; text-align: center;'>
                    <h3 style='margin: 0 0 10px 0; color: white;'>Final AI Prediction</h3>
                    <h1 style='font-size: 2.5rem; margin: 10px 0; color: white;'>110 kg ± 8 kg</h1>
                    <p style='margin: 0; font-size: 0.9rem;'>Confidence: 94%</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Prediction Factors Breakdown
        st.markdown("#### 📊 Prediction Factors Breakdown")
        
        factors_col1, factors_col2, factors_col3 = st.columns(3)
        
        with factors_col1:
            st.metric("Base Demand", "80 kg", "+0%")
        
        with factors_col2:
            st.metric("Festival Impact", "28 kg", "+35%")
        
        with factors_col3:
            st.metric("Weather Impact", "2 kg", "+2.5%")
        
    
    with col2:
        st.subheader("Demand Insights")
        
        top_dishes = forecast_df.groupby('dish')['predicted_demand'].mean().nlargest(3)
        st.write("**Top 3 Predicted Dishes:**")
        for dish, demand in top_dishes.items():
            st.metric(f"🍽️ {dish}", f"{demand:.0f} orders")
        
        st.divider()

        st.write("**📈 Demand Alerts:**")
        high_demand_dishes = forecast_df[forecast_df['predicted_demand'] > 45]['dish'].unique()
        for dish in high_demand_dishes[:3]:
            st.success(f"High demand expected for {dish}")

    # Restaurant Action & Results Section
    st.markdown("---")
    st.header("📊 Restaurant Action & Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            """
            <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 10px; color: white;'>
                <p style='margin: 0; font-size: 1.1rem;'>Prepared</p>
                <h1 style='font-size: 2.5rem; margin: 10px 0;'>115 kg</h1>
                <p style='margin: 0; font-size: 0.9rem;'>(5% buffer)</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
            border-radius: 10px; color: white;'>
                <p style='margin: 0; font-size: 1.1rem;'>Actual Sold</p>
                <h1 style='font-size: 2.5rem; margin: 10px 0;'>112 kg</h1>
                <p style='margin: 0; font-size: 0.9rem;'>98% utilization</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #fc466b 0%, #3f5efb 100%); 
            border-radius: 10px; color: white;'>
                <p style='margin: 0; font-size: 1.1rem;'>Waste</p>
                <h1 style='font-size: 2.5rem; margin: 10px 0;'>3 kg</h1>
                <p style='margin: 0; font-size: 0.9rem;'>2.6% of prepared</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            """
            <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); 
            border-radius: 10px; color: white;'>
                <p style='margin: 0; font-size: 1.1rem;'>Savings</p>
                <h1 style='font-size: 2.5rem; margin: 10px 0;'>¥850</h1>
                <p style='margin: 0; font-size: 0.9rem;'>(17 kg × ¥50/kg)</p>
            </div>
            """,
            unsafe_allow_html=True
        )

with tab2:
    st.header("📦 Real-time Inventory Tracking")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        current_inventory = restaurant_data[restaurant_data['date'] == restaurant_data['date'].max()]
        
        fig_inventory = px.bar(current_inventory, x='dish', y='inventory_level', color='category',
                              title="Current Inventory Levels")
        st.plotly_chart(fig_inventory, use_container_width=True)
        
        # === ADD TIMELINE TABLE HERE ===
        
        st.markdown("---")
        st.subheader("📅 Inventory Timeline & Alerts")
        
        # Timeline data
        timeline_data = [
            {"day": "Sunday", "event": "Buy Paneer (20 kg bought)", "status": "completed", "icon": "🛒"},
            {"day": "Monday", "event": "10 kg remaining", "status": "current", "icon": "📊"},
            {"day": "Tuesday Morning Alert", "event": "10 kg Paneer expires in 2 days", "status": "alert", "icon": "⚠️"},
            {"day": "Wednesday", "event": "Recommended: Use in special dishes", "status": "recommendation", "icon": "💡"},
            {"day": "Thursday", "event": "Donate if unused (expiry day)", "status": "future", "icon": "❤️"}
        ]
        
        # Create timeline display
        for item in timeline_data:
            if item['status'] == 'completed':
                bg_color = "#e8f5e8"
                border_color = "#51cf66"
            elif item['status'] == 'current':
                bg_color = "#e3f2fd"
                border_color = "#2196f3"
            elif item['status'] == 'alert':
                bg_color = "#ffeaa7"
                border_color = "#fdcb6e"
            elif item['status'] == 'recommendation':
                bg_color = "#f8f9fa"
                border_color = "#6c757d"
            else:
                bg_color = "#ffffff"
                border_color = "#dee2e6"
            
            st.markdown(
                f"""
                <div style='
                    background-color: {bg_color};
                    border-left: 4px solid {border_color};
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 5px;
                    display: flex;
                    align-items: center;
                '>
                    <span style='font-size: 1.5rem; margin-right: 15px;'>{item['icon']}</span>
                    <div>
                        <strong style='font-size: 1.1rem;'>{item['day']}</strong><br>
                        <span style='color: #666;'>{item['event']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Quick actions based on timeline
        st.markdown("#### 🚀 Quick Actions")
        
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("📋 Create Special Menu", use_container_width=True, key="special_menu"):
                st.success("Paneer special menu created! 🍽️")
        
        with action_col2:
            if st.button("🎯 Set Promotion", use_container_width=True, key="set_promo"):
                st.success("20% discount promotion activated! 💰")
        
        with action_col3:
            if st.button("❤️ Schedule Donation", use_container_width=True, key="schedule_donate"):
                st.success("Donation scheduled with Food Bank! 🤝")
        
        # Inventory aging analysis
        st.markdown("---")
        st.subheader("📊 Inventory Aging Analysis")
        
        aging_data = {
            "Product": ["Paneer", "Chicken", "Vegetables", "Bread", "Milk"],
            "Current Stock": ["10 kg", "15 kg", "8 kg", "12 units", "20 L"],
            "Days Until Expiry": ["2 days", "5 days", "1 day", "3 days", "4 days"],
            "Status": ["⚠️ Urgent", "✅ Safe", "🚨 Critical", "⚠️ Urgent", "✅ Safe"],
            "Recommended Action": ["Use today", "Monitor", "Use immediately", "Promote", "Normal use"]
        }
        
        aging_df = pd.DataFrame(aging_data)
        
        # Style the aging table
        st.markdown(
            """
            <style>
            .aging-table {
                width: 100%;
                border-collapse: collapse;
            }
            .aging-table th {
                background-color: #667eea;
                color: white;
                padding: 12px;
                text-align: left;
            }
            .aging-table td {
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }
            .aging-table tr:nth-child(even) {
                background-color: #f8f9fa;
            }
            .status-urgent { color: #e74c3c; font-weight: bold; }
            .status-critical { color: #c0392b; font-weight: bold; }
            .status-safe { color: #27ae60; font-weight: bold; }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Display the table
        st.table(aging_df)
    
    with col2:
        st.subheader("Inventory Alerts")
        
        low_inventory = current_inventory[current_inventory['inventory_level'] < 30]
        if not low_inventory.empty:
            st.error("**🚨 Low Inventory Alert:**")
            for _, item in low_inventory.iterrows():
                st.write(f"⚠️ {item['dish']}: {item['inventory_level']} units")
        else:
            st.success("✅ All inventory levels are adequate")
        
        st.divider()
        
        total_inventory = current_inventory['inventory_level'].sum()
        avg_inventory = current_inventory['inventory_level'].mean()
        
        st.metric("Total Inventory Value", f"${total_inventory * 10:,.0f}")
        st.metric("Average Stock per Dish", f"{avg_inventory:.0f} units")
        
        # AI Smart Suggestions
        st.markdown("---")
        st.subheader("🤖 AI Smart Suggestions")
        
        st.markdown(
            """
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 15px; border-radius: 10px; color: white; margin-bottom: 15px;'>
                <h4 style='margin: 0 0 10px 0; color: white;'>1. Run "Pasta Festival" promotion (30% off all pasta dishes)</h4>
                <p style='margin: 0; font-size: 0.9em;'>High inventory + predicted low demand detected</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
            padding: 15px; border-radius: 10px; color: white; margin-bottom: 15px;'>
                <h4 style='margin: 0 0 10px 0; color: white;'>2. Auto-post to Zomato/Swiggy</h4>
                <p style='margin: 0; font-size: 0.9em;'>Promote special offers on food delivery platforms</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div style='background: linear-gradient(135deg, #fc466b 0%, #3f5efb 100%); 
            padding: 15px; border-radius: 10px; color: white; margin-bottom: 20px;'>
                <h4 style='margin: 0 0 10px 0; color: white;'>3. Push notification to 5,000 app users nearby</h4>
                <p style='margin: 0; font-size: 0.9em;'>Target customers within 5km radius</p>
            </div>
            """,
            unsafe_allow_html=True
        )

with tab3:
    st.header("🗑️ Waste Tracking & Analytics")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        waste_by_dish = restaurant_data.groupby('dish')['waste_kg'].sum().reset_index()
        fig_waste = px.pie(waste_by_dish, values='waste_kg', names='dish',
                          title="Total Waste by Dish (kg)")
        st.plotly_chart(fig_waste, use_container_width=True)
        
        waste_trends = restaurant_data.groupby('date')['waste_kg'].sum().reset_index()
        fig_waste_trend = px.line(waste_trends, x='date', y='waste_kg',
                                 title="Daily Waste Trends")
        st.plotly_chart(fig_waste_trend, use_container_width=True)
    
    with col2:
        st.subheader("Waste Analytics")
        
        total_waste = restaurant_data['waste_kg'].sum()
        total_cost = restaurant_data['cost'].sum()
        waste_cost = total_waste * 8
        
        st.metric("Total Food Waste", f"{total_waste:.1f} kg")
        st.metric("Waste Cost Impact", f"${waste_cost:.0f}")
        st.metric("Waste Percentage", f"{(total_waste/(total_waste + total_cost)*100):.1f}%")
        
        st.divider()
        
        st.write("**💡 Waste Reduction Tips:**")
        tips = [
            "Portion control for high-waste dishes",
            "Implement first-in-first-out system",
            "Donate excess food",
            "Track waste patterns daily"
        ]
        for tip in tips:
            st.write(f"• {tip}")

# NEW DONATE FOOD TAB
with tab4:
    st.header("❤️ Food Donation Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Donation Statistics
        st.subheader("📈 Donation Impact Overview")
        
        # Impact metrics
        total_donated = donation_data['quantity_kg'].sum()
        total_impact = donation_data['impact_score'].sum()
        avg_impact = donation_data['impact_score'].mean()
        carbon_saved = donation_data['carbon_saved'].sum()
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric("Total Food Donated", f"{total_donated} kg")
        with metric_col2:
            st.metric("Meals Provided", f"{(total_donated * 4):.0f}+")
        with metric_col3:
            st.metric("Carbon Saved", f"{carbon_saved} kg CO₂")
        
        # Donation trends
        donation_trends = donation_data.groupby('date')['quantity_kg'].sum().reset_index()
        fig_donation_trend = px.line(donation_trends, x='date', y='quantity_kg',
                                   title="Monthly Donation Trends")
        st.plotly_chart(fig_donation_trend, use_container_width=True)
        
        # NGO Performance
        st.subheader("🏢 NGO Partnership Performance")
        ngo_performance = donation_data.groupby('ngo_name').agg({
            'quantity_kg': 'sum',
            'impact_score': 'mean'
        }).reset_index()
        
        fig_ngo = px.bar(ngo_performance, x='ngo_name', y='quantity_kg',
                        color='impact_score',
                        title="Food Donated by NGO Partner")
        st.plotly_chart(fig_ngo, use_container_width=True)
    
    with col2:
        # Quick Donation Actions
        st.subheader("🚀 Quick Donation")
        
        with st.form("quick_donation"):
            st.write("**Schedule New Donation**")
            food_type = st.selectbox("Food Type", ["Prepared Meals", "Fresh Vegetables", "Bread & Bakery", "Dairy", "Fruits"])
            quantity = st.slider("Quantity (kg)", 1, 50, 10)
            ngo = st.selectbox("NGO Partner", donation_data['ngo_name'].unique())
            schedule_date = st.date_input("Pickup Date", datetime.now() + timedelta(days=1))
            
            if st.form_submit_button("📅 Schedule Donation"):
                st.success(f"✅ Donation scheduled! {quantity}kg of {food_type} to {ngo}")
        
        st.divider()
        
        # Recent Donations
        st.subheader("📋 Recent Donations")
        recent_donations = donation_data.sort_values('date', ascending=False).head(5)
        for _, donation in recent_donations.iterrows():
            status_color = "🟢" if donation['status'] == 'Completed' else "🟡" if donation['status'] == 'Scheduled' else "🔵"
            st.write(f"{status_color} **{donation['food_item']}** - {donation['quantity_kg']}kg")
            st.write(f"   → {donation['ngo_name']} ({donation['status']})")
            st.write("")
        
        

    # Donation Impact Visualization
    st.markdown("---")
    st.subheader("🎯 Donation Impact Analysis")
    
    impact_col1, impact_col2 = st.columns(2)
    
    with impact_col1:
        # Food type distribution
        food_dist = donation_data.groupby('food_item')['quantity_kg'].sum().reset_index()
        fig_food_dist = px.pie(food_dist, values='quantity_kg', names='food_item',
                              title="Donated Food Distribution")
        st.plotly_chart(fig_food_dist, use_container_width=True)
    
    with impact_col2:
        # Impact by NGO
        st.subheader("🏆 Top Performing Partners")
        top_ngos = donation_data.groupby('ngo_name').agg({
            'quantity_kg': 'sum',
            'impact_score': 'mean'
        }).nlargest(3, 'quantity_kg')
        
        for ngo, row in top_ngos.iterrows():
            st.write(f"**{ngo}**")
            st.write(f"• Donated: {row['quantity_kg']}kg")
            st.write(f"• Impact Score: {row['impact_score']:.0f}/100")
            st.progress(row['impact_score']/100)
            st.write("")

# NEW VOICE LOG TAB FOR RESTAURANT
with tab5:
    st.header("🎤 Voice Command Center - Restaurant")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Voice Command Interface
        st.subheader("🎙️ Quick Voice Commands")
        
        # Voice command buttons
        cmd_col1, cmd_col2, cmd_col3 = st.columns(3)
        
        with cmd_col1:
            if st.button("📦 Update Inventory", use_container_width=True):
                st.success("🎤 Say: 'Add 20kg pasta to inventory'")
            if st.button("🗑️ Report Waste", use_container_width=True):
                st.success("🎤 Say: 'Report 5kg vegetable waste'")
        
        with cmd_col2:
            if st.button("❤️ Schedule Donation", use_container_width=True):
                st.success("🎤 Say: 'Schedule donation for excess bread'")
            if st.button("📊 Stock Check", use_container_width=True):
                st.success("🎤 Say: 'Check chicken inventory'")
        
        with cmd_col3:
            if st.button("🔄 Quick Order", use_container_width=True):
                st.success("🎤 Say: 'Order 50kg rice'")
            if st.button("📈 Daily Report", use_container_width=True):
                st.success("🎤 Say: 'Generate waste report'")
        
        # Manual voice input
        st.subheader("💬 Manual Voice Input")
        voice_input = st.text_input("Or type your command manually:", placeholder="e.g., 'Add 15kg tomatoes to inventory'")
        if voice_input:
            st.info(f"🔊 Processing: '{voice_input}'")
            if st.button("Execute Command"):
                st.success(f"✅ Command executed: {voice_input}")
        
        # Voice Log History
        st.subheader("📋 Recent Voice Commands")
        
        # Filter logs
        status_filter = st.selectbox("Filter by status:", ["All", "Completed", "Processing", "Failed"])
        filtered_logs = voice_logs_restaurant if status_filter == "All" else voice_logs_restaurant[voice_logs_restaurant['status'] == status_filter]
        
        for _, log in filtered_logs.head(8).iterrows():
            status_color = "🟢" if log['status'] == 'Completed' else "🟡" if log['status'] == 'Processing' else "🔴"
            st.write(f"{status_color} **{log['command']}**")
            st.write(f"   👤 {log['user']} | ⏰ {log['timestamp'].strftime('%Y-%m-%d %H:%M')} | 🎯 {log['action_type']}")
            st.write(f"   📊 Confidence: {log['confidence']*100}%")
            st.write("")
    
    with col2:
        # Voice Analytics
        st.subheader("📊 Voice Command Analytics")
        
        # Stats
        total_commands = len(voice_logs_restaurant)
        completed_commands = len(voice_logs_restaurant[voice_logs_restaurant['status'] == 'Completed'])
        success_rate = (completed_commands / total_commands) * 100
        avg_confidence = voice_logs_restaurant['confidence'].mean() * 100
        
        st.metric("Total Commands", total_commands)
        st.metric("Success Rate", f"{success_rate:.1f}%")
        st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
        
        st.divider()
        
        # Command type distribution
        st.subheader("🎯 Command Types")
        cmd_types = voice_logs_restaurant['action_type'].value_counts()
        fig_cmd_types = px.pie(values=cmd_types.values, names=cmd_types.index,
                              title="Voice Command Distribution")
        st.plotly_chart(fig_cmd_types, use_container_width=True)
        
        st.divider()
        
        # Quick Tips
        st.subheader("💡 Voice Command Tips")
        tips = [
            "Speak clearly and slowly",
            "Use specific quantities (e.g., '15kg')",
            "Mention product names clearly",
            "Include action verbs like 'add', 'update', 'report'"
        ]
        for tip in tips:
            st.write(f"• {tip}")

    # Voice Command Performance
    st.markdown("---")
    st.subheader("📈 Voice Command Performance")
    
    perf_col1, perf_col2 = st.columns(2)
    
    with perf_col1:
        # Success rate over time
        voice_logs_restaurant['date'] = voice_logs_restaurant['timestamp'].dt.date
        daily_performance = voice_logs_restaurant.groupby('date').agg({
            'confidence': 'mean',
            'status': lambda x: (x == 'Completed').mean()
        }).reset_index()
        
        fig_performance = px.line(daily_performance, x='date', y='confidence',
                                 title="Daily Average Confidence Score")
        st.plotly_chart(fig_performance, use_container_width=True)
    
    with perf_col2:
        # User performance
        user_stats = voice_logs_restaurant.groupby('user').agg({
            'confidence': 'mean',
            'status': lambda x: (x == 'Completed').mean()
        }).reset_index()
        
        fig_users = px.bar(user_stats, x='user', y='confidence',
                          color='status',
                          title="User Performance & Success Rate")
        st.plotly_chart(fig_users, use_container_width=True)
        
# Pricing & ROI Section at the bottom
st.markdown("---")
st.header("💰 Pricing & ROI")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("### Monthly Subscription")
    st.markdown("<h1 style='text-align: center; color: #1f77b4;'>¥5,999</h1>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Average Monthly Savings")
    st.markdown("<h1 style='text-align: center; color: #2ca02c;'>¥20,000</h1>", unsafe_allow_html=True)

with col2:
    st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)
    
    if st.button(
        "**Start 30-Day Free Trial**", 
        use_container_width=True, 
        type="primary",
        key="free_trial_main",
        help="Start your free trial with no commitment"
    ):
        st.success("🎉 Free trial started! You'll be redirected to setup...")
    
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style='text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px;'>
            <p style='margin: 0; color: #666; font-size: 1.1rem; line-height: 1.4;'>
                Join <strong>3,300+</strong> restaurants reducing food waste with AI
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown("### ROI")
    st.markdown(
        """
        <div style='
            text-align: center; 
            padding: 40px 20px; 
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
            border-radius: 50%; 
            width: 180px; 
            height: 180px; 
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        '>
            <h1 style='font-size: 3rem; margin: 0; color: white;'>233%</h1>
            <p style='margin: 5px 0 0 0; font-size: 1rem; color: white;'>Return on Investment</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Real-time updates
st.sidebar.header("Real-time Controls")
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.info("Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))