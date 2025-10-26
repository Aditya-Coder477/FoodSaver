import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import json

def init_firebase_auth():
    """Initialize Firebase Authentication"""
    if not firebase_admin._apps:
        # For prototype, use a service account or anonymous auth
        try:
            cred = credentials.Certificate("firebase-service-account.json")
            firebase_admin.initialize_app(cred)
        except:
            # Fallback to demo mode
            st.warning("Running in demo mode - no Firebase connection")

def authenticate_user():
    """Simple authentication for prototype"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_email = "demo@foodsaver.com"
        st.session_state.user_id = "demo_user_123"
        st.session_state.cashback_balance = 0
    
    if not st.session_state.authenticated:
        show_login_screen()
        return False
    return True

def show_login_screen():
    """Display login/signup screen"""
    st.markdown('<div class="main-header">🍽️ FoodSaver</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_btn"):
            # Simple demo authentication
            if email and password:
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.session_state.user_id = f"user_{hash(email)}"
                st.session_state.cashback_balance = 50  # Starting bonus
                st.success("Login successful! 🎉")
                st.rerun()
            else:
                st.error("Please enter email and password")
    
    with col2:
        st.subheader("Sign Up")
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        


def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.user_email = None
    st.session_state.user_id = None
    st.session_state.cashback_balance = 0
    st.rerun()