import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.title("🔒 Authentication Required")
    st.error("Please log in to access the Dashboard")
    st.info("Use the login form in the main app to access this feature")
    st.stop()

def show():
    # Remove the sidebar navigation and display everything in main area
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .cashback-card {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
    }
    .quick-action-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        cursor: pointer;
        transition: transform 0.2s;
        margin-bottom: 10px;
    }
    .quick-action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    </style>
    """, unsafe_allow_html=True)

    # Main Dashboard Header
    st.markdown('<div class="main-header">🏠 FoodSaver Dashboard</div>', unsafe_allow_html=True)
    
    # User stats
    user_stats = {
        'cashback_balance': st.session_state.get('cashback_balance', 50),
        'food_saved_kg': 2.5,
        'donations_made': 3,
        'meals_logged': 47,
        'waste_prevented': 12.8
    }
    
    # ===== CASHBACK BALANCE SECTION =====
    st.markdown(f"""
    <div class="cashback-card">
        <h2 style="margin:0; font-size: 1.2rem;">💰 Cashback Balance</h2>
        <h1 style="margin:10px 0; font-size: 2.5rem;">₹{user_stats['cashback_balance']}</h1>
        <p style="margin:0; opacity: 0.9;">Available to withdraw</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ===== QUICK ACTIONS SECTION =====
    st.subheader("🚀 Quick Actions")
    
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        st.markdown("""
        <div class="quick-action-btn" onclick="alert('Scan Product clicked')">
            <h3>📦</h3>
            <p><strong>Scan Product</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
    with action_col2:
        st.markdown("""
        <div class="quick-action-btn" onclick="alert('Log Meal clicked')">
            <h3>🎤</h3>
            <p><strong>Log Meal</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
    with action_col3:
        st.markdown("""
        <div class="quick-action-btn" onclick="alert('Donate Food clicked')">
            <h3>❤️</h3>
            <p><strong>Donate Food</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
    with action_col4:
        st.markdown("""
        <div class="quick-action-btn" onclick="alert('Withdraw clicked')">
            <h3>💰</h3>
            <p><strong>Withdraw</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Two columns for charts and additional info
    col1, col2 = st.columns(2)
    
    with col1:
        # ===== CASHBACK EARNINGS CHART =====
        st.subheader("📈 Cashback Earnings")
        
        # Sample data for the chart
        dates = [(datetime.now() - timedelta(days=i)).strftime('%b %d') for i in range(6, -1, -1)]
        earnings = [12, 18, 15, 22, 25, 20, 28]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=earnings,
            fill='tozeroy',
            line=dict(color='#4CAF50', width=3),
            marker=dict(size=8, color='#4CAF50'),
            name='Daily Earnings'
        ))
        fig.update_layout(
            height=300,
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # ===== EXPIRING SOON SECTION =====
        st.subheader("⏰ Expiring Soon")
        
        expiring_items = [
            {"name": "Milk", "expires_in": "1 day", "icon": "🥛"},
            {"name": "Tomatoes", "expires_in": "2 days", "icon": "🍅"},
            {"name": "Bread", "expires_in": "3 days", "icon": "🍞"},
            {"name": "Yogurt", "expires_in": "1 day", "icon": "🥣"},
            {"name": "Spinach", "expires_in": "Today", "icon": "🥬"}
        ]
        
        for item in expiring_items:
            urgency_color = "#ff6b6b" if "Today" in item['expires_in'] or "1 day" in item['expires_in'] else "#ffa726"
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; 
                        padding: 12px; margin: 8px 0; background: #f8f9fa; 
                        border-radius: 8px; border-left: 4px solid {urgency_color};">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.2rem; margin-right: 10px;">{item['icon']}</span>
                    <strong>{item['name']}</strong>
                </div>
                <span style="color: {urgency_color}; font-weight: bold;">{item['expires_in']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # ===== ADDITIONAL METRICS =====
        st.subheader("📊 Your Impact")
        
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin:0; color: #4CAF50;">{user_stats['food_saved_kg']} kg</h3>
                <p style="margin:0; font-size: 0.9rem;">Food Saved</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin:0; color: #4CAF50;">{user_stats['donations_made']}</h3>
                <p style="margin:0; font-size: 0.9rem;">Donations Made</p>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin:0; color: #4CAF50;">{user_stats['meals_logged']}</h3>
                <p style="margin:0; font-size: 0.9rem;">Meals Logged</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin:0; color: #4CAF50;">₹{user_stats['waste_prevented'] * 100}</h3>
                <p style="margin:0; font-size: 0.9rem;">Money Saved</p>
            </div>
            """, unsafe_allow_html=True)
    
    # ===== RECENT ACTIVITY SECTION =====
    st.markdown("---")
    st.subheader("📝 Recent Activity")
    
    activities = [
        {"action": "Product Scan", "item": "Aashirvaad Atta", "cashback": "₹2", "time": "2 hours ago", "icon": "📦"},
        {"action": "Voice Log", "item": "Breakfast Meal", "cashback": "₹0.50", "time": "5 hours ago", "icon": "🎤"},
        {"action": "Donation", "item": "Wedding Food", "cashback": "₹50", "time": "1 day ago", "icon": "❤️"},
        {"action": "Bill Upload", "item": "D-Mart Shopping", "cashback": "₹5", "time": "2 days ago", "icon": "🧾"}
    ]
    
    for activity in activities:
        col1, col2, col3, col4 = st.columns([1, 3, 1, 2])
        with col1:
            st.write(f"<span style='font-size: 1.5rem;'>{activity['icon']}</span>", unsafe_allow_html=True)
        with col2:
            st.write(f"**{activity['action']}**")
            st.write(f"{activity['item']}")
        with col3:
            st.success(activity['cashback'])
        with col4:
            st.caption(activity['time'])
        
        st.markdown("---")

# Add some JavaScript for button interactions
st.markdown("""
<script>
// Function to handle quick action button clicks
function handleQuickAction(action) {
    alert(action + " feature clicked!");
}

// Add click listeners to quick action buttons
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.quick-action-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const action = this.querySelector('p').textContent.trim();
            handleQuickAction(action);
        });
    });
});
</script>
""", unsafe_allow_html=True)