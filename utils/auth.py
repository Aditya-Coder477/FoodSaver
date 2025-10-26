import streamlit as st
import hashlib
import time

def authenticate_user(username, password):
    """
    Simple authentication without external dependencies
    """
    # Simple user database (in production, use proper database)
    users = {
        "admin": {
            "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # "password"
            "role": "admin",
            "name": "Administrator"
        },
        "manager": {
            "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # "password"
            "role": "manager", 
            "name": "Restaurant Manager"
        },
        "staff": {
            "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # "password"
            "role": "staff",
            "name": "Staff Member"
        }
    }
    
    # Hash the input password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Check credentials
    if username in users and users[username]["password"] == password_hash:
        return {
            "success": True,
            "user": {
                "username": username,
                "name": users[username]["name"],
                "role": users[username]["role"],
                "login_time": time.time()
            }
        }
    else:
        return {"success": False, "error": "Invalid credentials"}

def logout():
    """
    Logout user by clearing session state
    """
    if 'user' in st.session_state:
        del st.session_state.user
    if 'logged_in' in st.session_state:
        st.session_state.logged_in = False

def require_login():
    """
    Check if user is logged in, redirect to login if not
    """
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("🔒 Please log in to access this page")
        st.info("Use the main app page to log in")
        st.stop()

def get_current_user():
    """
    Get current logged in user info
    """
    if 'user' in st.session_state:
        return st.session_state.user
    return None

def has_permission(required_role):
    """
    Check if current user has required role permissions
    """
    user = get_current_user()
    if not user:
        return False
    
    role_hierarchy = {"admin": 3, "manager": 2, "staff": 1}
    user_level = role_hierarchy.get(user.get("role", "staff"), 0)
    required_level = role_hierarchy.get(required_role, 0)
    
    return user_level >= required_level
