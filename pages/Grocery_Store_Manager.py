import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.title("🛒 Grocery Store Manager")

# Generate sample data
@st.cache_data(ttl=60)  # Cache for 1 hour
def generate_grocery_data():
    products = [
        'Milk', 'Bread', 'Eggs', 'Cheese', 'Yogurt', 'Chicken', 
        'Apples', 'Bananas', 'Tomatoes', 'Lettuce', 'Potatoes', 'Onions'
    ]
    categories = {
        'Milk': 'Dairy', 'Bread': 'Bakery', 'Eggs': 'Dairy', 'Cheese': 'Dairy',
        'Yogurt': 'Dairy', 'Chicken': 'Meat', 'Apples': 'Produce', 
        'Bananas': 'Produce', 'Tomatoes': 'Produce', 'Lettuce': 'Produce',
        'Potatoes': 'Produce', 'Onions': 'Produce'
    }
    
    data = []
    base_date = datetime(2024, 2, 1)
    
    for product in products:
        for i in range(30):  # 30 days of data
            expiry_days = random.randint(1, 14)
            data.append({
                'date': base_date + timedelta(days=i),
                'product': product,
                'category': categories[product],
                'current_stock': random.randint(10, 100),
                'sold_today': random.randint(5, 30),
                'expiry_date': base_date + timedelta(days=i + expiry_days),
                'promotion_discount': random.choice([0, 0, 0, 5, 10, 15]),  # Mostly no discount
                'price': round(random.uniform(1, 10), 2),
                'sales_rank': random.randint(1, 12)
            })
    
    return pd.DataFrame(data)

# Generate voice log data for grocery
@st.cache_data(ttl=3600)
def generate_voice_logs_grocery():
    commands = [
        "Check milk expiry dates",
        "Add 30 units bread to stock",
        "Set 15% discount on apples",
        "Report 10 units spoiled lettuce",
        "Update egg inventory to 25 units",
        "Create promotion for expiring yogurt",
        "Scan tomato barcode for stock",
        "Generate expiry report for dairy"
    ]
    
    data = []
    for i in range(25):
        data.append({
            'timestamp': datetime.now() - timedelta(hours=random.randint(1, 168)),
            'command': random.choice(commands),
            'status': random.choice(['Completed', 'Processing', 'Failed']),
            'confidence': round(random.uniform(0.7, 0.98), 2),
            'user': random.choice(['Manager Suzuki', 'Staff Kobayashi', 'Stock Clerk Ito']),
            'action_type': random.choice(['Expiry Check', 'Stock Update', 'Promotion', 'Waste Report', 'Inventory Scan'])
        })
    return pd.DataFrame(data)

# Load data
grocery_data = generate_grocery_data()
voice_logs_grocery = generate_voice_logs_grocery()

# Create tabs
tab1, tab2,tab3 = st.tabs([
    "📅 Expiry Tracking & Promotions",
    "📊 Product Performance Analytics",
    "🎤 Voice Log" 
])

with tab1:
    st.header("📅 Expiry Tracking & Promotions")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Expiry timeline
        st.subheader("Products Expiring Soon")
        
        # Filter products expiring in next 7 days
        today = datetime(2024, 2, 15)  # Simulated current date
        week_from_now = today + timedelta(days=7)
        
        expiring_soon = grocery_data[
            (grocery_data['expiry_date'] >= today) & 
            (grocery_data['expiry_date'] <= week_from_now)
        ].copy()
        
        if not expiring_soon.empty:
            expiring_soon['days_until_expiry'] = (expiring_soon['expiry_date'] - today).dt.days
            
            fig_expiry = px.bar(expiring_soon, x='product', y='days_until_expiry', color='category',
                               title="Days Until Expiry for Products",
                               labels={'days_until_expiry': 'Days Until Expiry'})
            st.plotly_chart(fig_expiry, use_container_width=True)
        else:
            st.success("✅ No products expiring in the next 7 days")
        
        # === ADD REAL-TIME EXPIRY DASHBOARD HERE ===
        
        st.markdown("---")
        st.header("🔄 Real-Time Expiry Dashboard")
        
        # Expiry dashboard data
        expiry_dashboard = [
            {
                "product": "Fortune Rice (10 kg)",
                "quantity": "45 packs",
                "days_left": "45 days",
                "status": "safe",
                "action": "Monitor",
                "icon": "🛒"
            },
            {
                "product": "Amul Butter (500g)",
                "quantity": "120 packs", 
                "days_left": "12 days",
                "status": "monitor",
                "action": "Plan promotion",
                "icon": "🧈"
            },
            {
                "product": "Mother Dairy Milk (1L)",
                "quantity": "200 cartons",
                "days_left": "8 days",
                "status": "urgent",
                "action": "40% discount",
                "icon": "🥛"
            }
        ]
        
        # Create expiry dashboard cards
        for i, item in enumerate(expiry_dashboard):
            if item['status'] == 'safe':
                bg_color = "#e8f5e8"
                border_color = "#51cf66"
                status_badge = "🟢 Safe"
            elif item['status'] == 'monitor':
                bg_color = "#fff3cd"
                border_color = "#ffc107"
                status_badge = "🟡 Monitor"
            else:  # urgent
                bg_color = "#ffeaa7"
                border_color = "#e74c3c"
                status_badge = "🔴 Urgent"
            
            # Create two columns for each product card
            col_left, col_right = st.columns([3, 1])
            
            with col_left:
                st.markdown(
                    f"""
                    <div style='
                        background-color: {bg_color};
                        border-left: 4px solid {border_color};
                        padding: 15px;
                        margin: 10px 0;
                        border-radius: 8px;
                    '>
                        <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                            <span style='font-size: 1.5rem; margin-right: 10px;'>{item['icon']}</span>
                            <div>
                                <strong style='font-size: 1.1rem;'>{item['product']}</strong><br>
                                <span style='color: #666;'>{item['quantity']}</span>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col_right:
                st.markdown(
                    f"""
                    <div style='
                        text-align: center;
                        padding: 15px 5px;
                        margin: 10px 0;
                    '>
                        <div style='font-size: 1.2rem; font-weight: bold; color: #2c3e50;'>
                            {item['days_left']}
                        </div>
                        <div style='font-size: 0.9rem; color: #666; margin-top: 5px;'>
                            {item['action']}
                        </div>
                        <div style='font-size: 0.8rem; margin-top: 5px;'>
                            {status_badge}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Add divider between items (except after last item)
            if i < len(expiry_dashboard) - 1:
                st.markdown("---")
        
        # Quick action buttons
        st.markdown("#### 🎯 Quick Actions")
        
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("📊 Generate Expiry Report", use_container_width=True, key="expiry_report"):
                st.success("Expiry report generated! 📈")
        
        with action_col2:
            if st.button("🎪 Create Bundle Deal", use_container_width=True, key="bundle_deal"):
                st.success("Bundle deal created! 🎯")
        
        with action_col3:
            if st.button("📱 Push Notification", use_container_width=True, key="push_notif"):
                st.success("Notification sent to customers! 📲")
        
        # Inventory turnover insights
        st.markdown("---")
        st.subheader("📈 Inventory Turnover Insights")
        
        insight_col1, insight_col2, insight_col3 = st.columns(3)
        
        with insight_col1:
            st.metric("Fast Moving", "15 products", "2.1 days turnover")
        
        with insight_col2:
            st.metric("Slow Moving", "8 products", "8.5 days turnover")
        
        with insight_col3:
            st.metric("Risk Items", "3 products", "Urgent action needed")    
        
    
    with col2:
        st.subheader("🚨 Expiry Alerts")
        
        # Critical alerts (expiring in 3 days)
        critical_expiry = expiring_soon[expiring_soon['days_until_expiry'] <= 3]
        if not critical_expiry.empty:
            st.error("**CRITICAL - Expiring in 3 days:**")
            for _, product in critical_expiry.iterrows():
                st.write(f"🔴 {product['product']} - {product['days_until_expiry']} days")
        else:
            st.success("✅ No critical expiry alerts")
        
        st.divider()
        
        st.subheader("🎯 Active Promotions")
        current_promotions = grocery_data[
            (grocery_data['date'] == grocery_data['date'].max()) & 
            (grocery_data['promotion_discount'] > 0)
        ]
        
        if not current_promotions.empty:
            for _, promo in current_promotions.iterrows():
                discount_color = "🟢" if promo['promotion_discount'] >= 10 else "🟡"
                st.write(f"{discount_color} {promo['product']}: {promo['promotion_discount']}% off")
        else:
            st.info("No active promotions currently")
        
        st.divider()
        
        # Promotion suggestions
        st.subheader("💡 Promotion Suggestions")
        slow_moving = grocery_data.groupby('product')['sold_today'].mean().nsmallest(3)
        for product, sales in slow_moving.items():
            st.write(f"• {product}: Low sales ({sales:.1f}/day) - Consider promotion")

with tab2:
    st.header("📊 Product Performance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales performance by category
        st.subheader("Sales Performance by Category")
        
        category_sales = grocery_data.groupby('category')['sold_today'].sum().reset_index()
        fig_category = px.pie(category_sales, values='sold_today', names='category',
                             title="Total Sales Distribution by Category")
        st.plotly_chart(fig_category, use_container_width=True)
        
        # === ADD AUTOMATED ACTION TIMELINE HERE ===
        
        st.markdown("---")
        st.header("🤖 Automated Action Timeline")
        
        # Timeline data
        timeline_data = [
            {
                "date": "Mar 25 (7 days before expiry)",
                "action": "30% discount promotion",
                "result": "80 packs sold in 3 days",
                "revenue": "₹5,600",
                "status": "success",
                "icon": "💰"
            },
            {
                "date": "Mar 28 (4 days before expiry)", 
                "action": "50% discount promotion",
                "result": "90 packs sold in 2 days",
                "revenue": "₹4,500",
                "status": "success",
                "icon": "🎯"
            },
            {
                "date": "Mar 30 (2 days before expiry)",
                "action": "Donate remaining stock",
                "result": "30 packs donated to Akshaya Patra",
                "revenue": "₹1,500 tax savings",
                "status": "donation",
                "icon": "❤️"
            }
        ]
        
        # Create timeline cards
        for i, item in enumerate(timeline_data):
            if item['status'] == 'success':
                bg_color = "#e8f5e8"
                border_color = "#51cf66"
            elif item['status'] == 'donation':
                bg_color = "#e3f2fd"
                border_color = "#2196f3"
            else:
                bg_color = "#fff3cd"
                border_color = "#ffc107"
            
            st.markdown(
                f"""
                <div style='
                    background-color: {bg_color};
                    border-left: 4px solid {border_color};
                    padding: 15px;
                    margin: 15px 0;
                    border-radius: 8px;
                '>
                    <div style='display: flex; align-items: flex-start;'>
                        <span style='font-size: 1.5rem; margin-right: 12px;'>{item['icon']}</span>
                        <div style='flex: 1;'>
                            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                                <strong style='font-size: 1.1rem; color: #2c3e50;'>{item['date']}</strong>
                                <strong style='font-size: 1.1rem; color: #27ae60;'>{item['revenue']}</strong>
                            </div>
                            <div style='color: #34495e; margin-bottom: 5px;'>
                                <strong>Action:</strong> {item['action']}
                            </div>
                            <div style='color: #7f8c8d;'>
                                <strong>Result:</strong> {item['result']}
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Add divider between timeline and results
        st.markdown("---")
        
        # Final Results Section
        st.subheader("🎯 Final Results")
        
        results_col1, results_col2, results_col3, results_col4 = st.columns(4)
        
        with results_col1:
            st.markdown(
                """
                <div style='text-align: center; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;'>
                    <h3 style='margin: 0; font-size: 1.8rem;'>₹5,600</h3>
                    <p style='margin: 5px 0 0 0; font-size: 0.9rem;'>30% discount sales</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with results_col2:
            st.markdown(
                """
                <div style='text-align: center; padding: 15px; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); border-radius: 10px; color: white;'>
                    <h3 style='margin: 0; font-size: 1.8rem;'>₹4,500</h3>
                    <p style='margin: 5px 0 0 0; font-size: 0.9rem;'>50% discount sales</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with results_col3:
            st.markdown(
                """
                <div style='text-align: center; padding: 15px; background: linear-gradient(135deg, #fc466b 0%, #3f5efb 100%); border-radius: 10px; color: white;'>
                    <h3 style='margin: 0; font-size: 1.8rem;'>₹1,500</h3>
                    <p style='margin: 5px 0 0 0; font-size: 0.9rem;'>Tax savings</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with results_col4:
            st.markdown(
                """
                <div style='text-align: center; padding: 15px; background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); border-radius: 10px; color: white;'>
                    <h3 style='margin: 0; font-size: 1.8rem;'>₹11,600</h3>
                    <p style='margin: 5px 0 0 0; font-size: 0.9rem;'>Total recovered</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Recovery metrics
        recovery_col1, recovery_col2 = st.columns(2)
        
        with recovery_col1:
            st.markdown(
                """
                <div style='text-align: center; padding: 20px; background-color: #e8f5e8; border-radius: 10px; border: 2px solid #51cf66;'>
                    <h2 style='margin: 0; color: #2b8a3e;'>58%</h2>
                    <p style='margin: 5px 0 0 0; color: #2b8a3e; font-weight: bold;'>Recovery Rate</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with recovery_col2:
            st.markdown(
                """
                <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%); border-radius: 10px; color: white;'>
                    <h3 style='margin: 0;'>Without AI: ₹0</h3>
                    <p style='margin: 5px 0 0 0;'>(all expired)</p>
                    <div style='font-size: 1.5rem; margin: 10px 0;'>→</div>
                    <h3 style='margin: 0;'>With AI: ₹11,600</h3>
                    <p style='margin: 5px 0 0 0;'>recovered</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # AI Impact Summary
        st.markdown("---")
        st.subheader("📈 AI Impact Summary")
        
        impact_col1, impact_col2, impact_col3 = st.columns(3)
        
        with impact_col1:
            st.metric("Products Saved", "200 packs", "From expiry")
        
        with impact_col2:
            st.metric("Waste Reduction", "100%", "Zero waste achieved")
        
        with impact_col3:
            st.metric("Customer Reach", "450+", "Through promotions")
    
    with col2:
        # Top performing products
        st.subheader("🏆 Top Performing Products")
        
        product_performance = grocery_data.groupby('product').agg({
            'sold_today': 'mean',
            'current_stock': 'mean',
            'price': 'first'
        }).reset_index()
        
        top_products = product_performance.nlargest(5, 'sold_today')
        
        for _, product in top_products.iterrows():
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Product", product['product'])
            with col2:
                st.metric("Avg Daily Sales", f"{product['sold_today']:.0f}")
            with col3:
                st.metric("Price", f"${product['price']:.2f}")
            st.divider()
        
        # Performance metrics
        st.subheader("📈 Overall Performance")
        
        total_revenue = (grocery_data['sold_today'] * grocery_data['price']).sum()
        avg_daily_sales = grocery_data['sold_today'].mean()
        stock_turnover = grocery_data['sold_today'].sum() / grocery_data['current_stock'].mean()
        
        st.metric("Total Revenue", f"${total_revenue:,.0f}")
        st.metric("Average Daily Sales", f"{avg_daily_sales:.0f} units")
        st.metric("Stock Turnover Ratio", f"{stock_turnover:.2f}")

# NEW VOICE LOG TAB FOR GROCERY
with tab3:
    st.header("🎤 Voice Command Center - Grocery")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Voice Command Interface
        st.subheader("🎙️ Quick Voice Commands")
        
        # Voice command buttons
        cmd_col1, cmd_col2, cmd_col3 = st.columns(3)
        
        with cmd_col1:
            if st.button("📅 Check Expiry", use_container_width=True):
                st.success("🎤 Say: 'Check milk expiry dates'")
            if st.button("📦 Update Stock", use_container_width=True):
                st.success("🎤 Say: 'Add 30 units bread to stock'")
        
        with cmd_col2:
            if st.button("💰 Set Promotion", use_container_width=True):
                st.success("🎤 Say: 'Set 15% discount on apples'")
            if st.button("🗑️ Report Spoilage", use_container_width=True):
                st.success("🎤 Say: 'Report 10 units spoiled lettuce'")
        
        with cmd_col3:
            if st.button("📊 Inventory Scan", use_container_width=True):
                st.success("🎤 Say: 'Scan tomato barcode for stock'")
            if st.button("📈 Expiry Report", use_container_width=True):
                st.success("🎤 Say: 'Generate expiry report for dairy'")
        
        # Manual voice input
        st.subheader("💬 Manual Voice Input")
        voice_input = st.text_input("Or type your command manually:", placeholder="e.g., 'Set 20% discount on expiring bananas'")
        if voice_input:
            st.info(f"🔊 Processing: '{voice_input}'")
            if st.button("Execute Command", key="grocery_execute"):
                st.success(f"✅ Command executed: {voice_input}")
        
        # Voice Log History
        st.subheader("📋 Recent Voice Commands")
        
        # Filter logs
        status_filter = st.selectbox("Filter by status:", ["All", "Completed", "Processing", "Failed"], key="grocery_filter")
        filtered_logs = voice_logs_grocery if status_filter == "All" else voice_logs_grocery[voice_logs_grocery['status'] == status_filter]
        
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
        total_commands = len(voice_logs_grocery)
        completed_commands = len(voice_logs_grocery[voice_logs_grocery['status'] == 'Completed'])
        success_rate = (completed_commands / total_commands) * 100
        avg_confidence = voice_logs_grocery['confidence'].mean() * 100
        
        st.metric("Total Commands", total_commands)
        st.metric("Success Rate", f"{success_rate:.1f}%")
        st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
        
        st.divider()
        
        # Command type distribution
        st.subheader("🎯 Command Types")
        cmd_types = voice_logs_grocery['action_type'].value_counts()
        fig_cmd_types = px.pie(values=cmd_types.values, names=cmd_types.index,
                              title="Voice Command Distribution")
        st.plotly_chart(fig_cmd_types, use_container_width=True)
        
        st.divider()
        
        # Quick Tips
        st.subheader("💡 Voice Command Tips")
        tips = [
            "Specify product names clearly",
            "Use exact quantities and units",
            "Mention discount percentages",
            "Include expiry-related keywords"
        ]
        for tip in tips:
            st.write(f"• {tip}")

    # Voice Command Performance
    st.markdown("---")
    st.subheader("📈 Voice Command Performance")
    
    perf_col1, perf_col2 = st.columns(2)
    
    with perf_col1:
        # Success rate over time
        voice_logs_grocery['date'] = voice_logs_grocery['timestamp'].dt.date
        daily_performance = voice_logs_grocery.groupby('date').agg({
            'confidence': 'mean',
            'status': lambda x: (x == 'Completed').mean()
        }).reset_index()
        
        fig_performance = px.line(daily_performance, x='date', y='confidence',
                                 title="Daily Average Confidence Score")
        st.plotly_chart(fig_performance, use_container_width=True)
    
    with perf_col2:
        # Most common commands
        common_commands = voice_logs_grocery['command'].value_counts().head(6)
        fig_commands = px.bar(x=common_commands.values, y=common_commands.index,
                             orientation='h', title="Most Frequent Commands")
        st.plotly_chart(fig_commands, use_container_width=True)
        
        
# Pricing & ROI Section at the bottom
st.markdown("---")
st.header("💰 Pricing & ROI")

# Create three columns for the pricing cards
col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1.2])

with col1:
    st.subheader("Monthly Subscription")
    st.markdown(
        """
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        border-radius: 10px; color: white;'>
            <h1 style='font-size: 2.5rem; margin: 0;'>$7,999</h1>
            <p style='font-size: 1.1rem; margin: 10px 0 0 0;'>per month</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.subheader("Average Monthly Savings")
    st.markdown(
        """
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
        border-radius: 10px; color: white;'>
            <h1 style='font-size: 2.5rem; margin: 0;'>$50,000</h1>
            <p style='font-size: 1.1rem; margin: 10px 0 0 0;'>recovered revenue</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.subheader("ROI")
    st.markdown(
        """
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #fc466b 0%, #3f5efb 100%); 
        border-radius: 10px; color: white;'>
            <h1 style='font-size: 2.5rem; margin: 0;'>525%</h1>
            <p style='font-size: 1.1rem; margin: 10px 0 0 0;'>return on investment</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.subheader("Free Trial")
    if st.button("**Start 30-Day Free Trial**", 
                 use_container_width=True, 
                 type="primary",
                 help="Start your free trial with no commitment"):
        st.success("🎉 Free trial started! You'll be redirected to setup...")
    
    st.markdown(
        """
        <div style='text-align: center; margin-top: 20px; padding: 15px; background-color: #f0f2f6; 
        border-radius: 10px; border-left: 4px solid #ff4b4b;'>
            <p style='margin: 0; font-weight: bold; color: #333;'>
                Join 500+ grocery stores maximizing revenue recovery
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Additional benefits section
st.markdown("---")
st.subheader("🚀 What You Get With Your Subscription")

benefits_col1, benefits_col2, benefits_col3 = st.columns(3)

with benefits_col1:
    st.markdown(
        """
        <div style='padding: 15px; background-color: #f8f9fa; border-radius: 8px; border-left: 4px solid #667eea;'>
            <h4 style='margin: 0 0 10px 0; color: #333;'>📊 Advanced Analytics</h4>
            <p style='margin: 0; color: #666;'>Real-time expiry tracking and predictive insights</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with benefits_col2:
    st.markdown(
        """
        <div style='padding: 15px; background-color: #f8f9fa; border-radius: 8px; border-left: 4px solid #11998e;'>
            <h4 style='margin: 0 0 10px 0; color: #333;'>🎯 Smart Promotions</h4>
            <p style='margin: 0; color: #666;'>AI-powered discount recommendations</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with benefits_col3:
    st.markdown(
        """
        <div style='padding: 15px; background-color: #f8f9fa; border-radius: 8px; border-left: 4px solid #fc466b;'>
            <h4 style='margin: 0 0 10px 0; color: #333;'>💼 Dedicated Support</h4>
            <p style='margin: 0; color: #666;'>24/7 customer success team</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Quick actions in sidebar
st.sidebar.header("Quick Actions")
if st.sidebar.button("🔄 Refresh Inventory Data"):
    st.rerun()

if st.sidebar.button("📧 Generate Expiry Report"):
    st.sidebar.success("Expiry report generated!")

if st.sidebar.button("🎯 Create New Promotion"):
    st.sidebar.info("Promotion creation panel opened")

st.sidebar.info("Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))