import streamlit as st
from utils.auth import authenticate_user, logout
from utils.firebase_client import init_firebase

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Simple login form in main app
if not st.session_state.logged_in:
    st.title("🌱 FoodSaver - Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.subheader("🔐 Login to Continue")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
            
            if login_button:
                # Simple authentication (replace with your actual auth logic)
                if username == "admin" and password == "password":
                    st.session_state.logged_in = True
                    st.success("Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try: admin/password")
    
    st.info("""
    **Demo Credentials:**
    - Username: `admin`
    - Password: `password`
    """)
    
    st.stop()

# Page configuration
st.set_page_config(
    page_title="FoodSaver - Stop Food Waste",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Firebase
init_firebase()

def main():
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .cashback-card {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

    # Authentication
    if not authenticate_user():
        return

    # Sidebar Navigation
    st.sidebar.title("🍽️ FoodSaver")
    st.sidebar.markdown(f"Welcome, **{st.session_state.user_email}**!")
    
    # Navigation
    page = st.sidebar.radio("Navigate to:", [
        "🏠 Dashboard",
        "📦 Scan Product", 
        "🎤 Voice Log",
        "❤️ Donate Food"
    ])

    # Logout button
    if st.sidebar.button("🚪 Logout"):
        logout()

    # Page routing
    if page == "🏠 Dashboard":
        from pages import Dashboard
        Dashboard.show()
    elif page == "📦 Scan Product":
        from pages import Scan_Product
        Scan_Product.show()
    elif page == "🎤 Voice Log":
        from pages import Voice_Log
        Voice_Log.show()
    elif page == "❤️ Donate Food":
        from pages import Donate_Food
        Donate_Food.show()

if __name__ == "__main__":
    main()