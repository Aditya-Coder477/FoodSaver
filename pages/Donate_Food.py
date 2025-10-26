import streamlit as st
from utils.ai_models import food_detector
from utils.cashback import cashback_system
import random
from datetime import datetime

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.title("🔒 Authentication Required")
    st.error("Please log in to use Donate Food feature")
    st.info("Use the login form in the main app to access this feature")
    st.stop()
    
def show():
    st.markdown('<div class="main-header">❤️ Donate Food</div>', unsafe_allow_html=True)
    
    st.info("Help feed the hungry while earning cashback and tax benefits! 🎁")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📸 Upload Food Photo")
        
        uploaded_file = st.file_uploader(
            "Take a clear photo of the food you want to donate",
            type=['png', 'jpg', 'jpeg'],
            help="Ensure good lighting and show all food containers"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            st.image(uploaded_file, caption="Food to Donate", use_column_width=True)
            
            if st.button("🔍 Analyze Food", type="primary"):
                with st.spinner("AI is analyzing your food..."):
                    # Use AI to detect food
                    detection_result = food_detector.detect_food(uploaded_file)
                    
                    if detection_result['success']:
                        st.success("✅ Food analysis complete!")
                        
                        # Display detection results
                        st.subheader("🍽️ Detected Food Items")
                        
                        for detection in detection_result['detections']:
                            col1, col2, col3 = st.columns([2, 1, 1])
                            with col1:
                                st.write(f"**{detection['category']}**")
                            with col2:
                                st.write(f"{detection['estimated_weight_grams']}g")
                            with col3:
                                st.write(f"{detection['confidence']*100}%")
                        
                        st.write(f"**Total Quantity:** {detection_result['total_weight_kg']} kg")
                        
                        # NGO matching
                        st.subheader("🏠 Available NGOs")
                        ngos = find_nearby_ngos()
                        
                        selected_ngo = st.selectbox(
                            "Choose an NGO for donation:",
                            options=[ngo['name'] for ngo in ngos],
                            format_func=lambda x: f"{x} ({ngos[[ngo['name'] for ngo in ngos].index(x)]['distance']} away)"
                        )
                        
                        if st.button("🎁 Confirm Donation", type="primary"):
                            # Process donation
                            process_donation(
                                detection_result, 
                                selected_ngo, 
                                uploaded_file.name
                            )
    
    with col2:
        st.subheader("💡 How It Works")
        st.markdown("""
        1. **Take a photo** of the food you want to donate
        2. **AI automatically detects** food items and quantities
        3. **Choose a nearby NGO** from our verified network
        4. **Get ₹50 cashback** instantly + tax benefits
        5. **Track your impact** in real-time
        
        🌟 **Benefits:**
        - ₹50 instant cashback per donation
        - Tax deduction certificates
        - Live tracking of food distribution
        - Social impact badges
        """)
        
        # Impact statistics
        st.subheader("📊 Your Impact")
        st.metric("People Fed", "156")
        st.metric("Food Donated", "78 kg")
        st.metric("CO₂ Saved", "234 kg")
        
        # Recent donations
        st.subheader("🕒 Recent Donations")
        donations = [
            {"date": "Today", "food": "Wedding Food", "quantity": "25 kg", "people": "80"},
            {"date": "2 days ago", "food": "Restaurant Surplus", "quantity": "15 kg", "people": "45"},
            {"date": "1 week ago", "food": "Party Leftovers", "quantity": "8 kg", "people": "25"}
        ]
        
        for donation in donations:
            st.write(f"**{donation['date']}**: {donation['food']}")
            st.write(f"{donation['quantity']} → {donation['people']} people")
            st.write("---")

def find_nearby_ngos():
    """Find nearby NGOs for donation"""
    return [
        {"name": "Akshaya Patra", "distance": "2.3 km", "rating": "4.8★"},
        {"name": "Robin Hood Army", "distance": "4.1 km", "rating": "4.7★"},
        {"name": "Feeding India", "distance": "5.2 km", "rating": "4.6★"},
        {"name": "No Food Waste", "distance": "3.7 km", "rating": "4.5★"}
    ]

def process_donation(detection_result, ngo_name, image_name):
    """Process the donation and issue rewards"""
    
    # Process cashback
    result = cashback_system.process_cashback(
        'donation',
        st.session_state.user_id,
        {
            'ngo': ngo_name,
            'quantity_kg': detection_result['total_weight_kg'],
            'food_items': [d['category'] for d in detection_result['detections']]
        }
    )
    
    if result['success']:
        st.balloons()
        st.success("🎉 Donation confirmed successfully!")
        
        # Display rewards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Cashback Earned", "₹50")
        
        with col2:
            people_fed = int(detection_result['total_weight_kg'] * 2)  # Approx 2 people per kg
            st.metric("People Fed", people_fed)
        
        with col3:
            tax_saving = detection_result['total_weight_kg'] * 50  # ₹50 per kg tax benefit
            st.metric("Tax Benefit", f"₹{tax_saving}")
        
        # Social share
        st.subheader("📢 Share Your Impact")
        share_message = f"""
        I just donated {detection_result['total_weight_kg']}kg of food through @FoodSaverApp! 
        🍽️ Fed {people_fed} people and earned ₹50 cashback + tax benefits. 
        Join me in fighting food waste! ❤️
        """
        
        st.code(share_message)
        
        if st.button("📱 Copy to Share"):
            st.success("Message copied! Share it on social media 🎉")