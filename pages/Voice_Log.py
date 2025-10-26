import streamlit as st
import speech_recognition as sr
import audio_recorder_streamlit as ars

# Simple cashback function replacement
def simple_cashback_system(amount, transaction_type="donation"):
    """Simplified cashback system without external dependencies"""
    rates = {
        "donation": 0.05,  # 5% cashback for donations
        "purchase": 0.02,  # 2% cashback for purchases
        "waste_reduction": 0.03  # 3% for waste reduction
    }
    
    rate = rates.get(transaction_type, 0.01)
    cashback = amount * rate
    return cashback
# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.title("🔒 Authentication Required")
    st.error("Please log in to use Voice Log feature")
    st.info("Use the login form in the main app to access this feature")
    st.stop()

    
def show():
    st.markdown('<div class="main-header">🎤 Voice Log</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎤 Record Your Meal")
        
        # Voice recording section
        st.info("Speak your meal in English or Hindi. Example: 'I ate 2 roti, dal, and sabzi'")
        
        # Audio recorder
        audio_bytes = ars.audio_recorder(
            text="Click to record",
            recording_color="#e8b62c",
            neutral_color="#6aa36f",
            icon_name="microphone",
            icon_size="2x",
        )
        
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            
            if st.button("🎯 Process Recording", type="primary"):
                with st.spinner("Processing your voice..."):
                    # Mock speech recognition
                    meal_data = mock_speech_recognition()
                    
                    st.success("✅ Meal logged successfully!")
                    
                    # Display parsed meal
                    st.subheader("🍽️ Meal Details")
                    for item in meal_data['items']:
                        st.write(f"• {item}")
                    
                    st.write(f"**Total Calories:** {meal_data['calories']} kcal")
                    
                    # Process cashback
                    result = cashback_system.process_cashback(
                        'voice_log',
                        st.session_state.user_id,
                        {'meal_items': meal_data['items']}
                    )
                    
                    if result['success']:
                        st.success(result['message'])
        
        # Manual entry fallback
        st.subheader("📝 Manual Entry")
        meal_text = st.text_area("Or type your meal here:")
        if st.button("Log Meal Manually"):
            if meal_text:
                st.success(f"Meal logged: {meal_text}")
                result = cashback_system.process_cashback(
                    'voice_log', 
                    st.session_state.user_id,
                    {'meal_text': meal_text}
                )
                if result['success']:
                    st.success(result['message'])
    
    with col2:
        st.subheader("💡 How It Works")
        st.markdown("""
        1. **Click the microphone** to start recording
        2. **Speak your meal** in simple English or Hindi
        3. **AI processes** your voice and extracts food items
        4. **Get nutrition insights** and track your consumption
        5. **Earn ₹0.50 cashback** for each meal logged
        
        🎯 **Supported Languages:** English, Hindi
        🎯 **Daily Limit:** 3 meals (₹1.50 max)
        """)
        
        # Example phrases
        st.subheader("🗣️ Example Phrases")
        st.markdown("""
        - "I ate 2 roti and dal"
        - "Breakfast: poha and tea"  
        - "Lunch: rice, sambar, potato fry"
        - "Dinner: chapati, paneer, salad"
        - "मैंने 2 रोटी और दाल खाई"
        """)
        
        # Today's logs
        st.subheader("📊 Today's Logs")
        today_logs = [
            {"meal": "Breakfast", "items": "Poha, Tea", "time": "8:00 AM"},
            {"meal": "Lunch", "items": "Roti, Dal, Rice", "time": "1:30 PM"}
        ]
        
        for log in today_logs:
            st.write(f"**{log['meal']}** ({log['time']})")
            st.write(f"{log['items']}")
            st.write("---")

def mock_speech_recognition():
    """Mock speech recognition for prototype"""
    sample_meals = [
        {
            "items": ["2 Roti", "Dal", "Mixed Vegetables", "Salad"],
            "calories": 485
        },
        {
            "items": ["Rice", "Sambar", "Potato Fry", "Curd"],
            "calories": 520
        },
        {
            "items": ["Poha", "Tea", "Fruits"],
            "calories": 320
        },
        {
            "items": ["3 Chapati", "Paneer Butter Masala", "Naan"],
            "calories": 650
        }
    ]
    
    import random
    return random.choice(sample_meals)
