import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from utils.auth import authenticate_user, logout
from utils.firebase_client import init_firebase
import requests
import cv2
from PIL import Image
import pyzbar.pyzbar as pyzbar
from utils.cashback import cashback_system
from datetime import datetime, timedelta
import requests
from utils.cashback import cashback_system
import random
from datetime import datetime
import speech_recognition as sr
import audio_recorder_streamlit as ars


# Page configuration
st.set_page_config(
    page_title="FoodSaver - Reduce Food Waste",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Firebase
init_firebase()

def show_dashboard():
    # Custom CSS for Dashboard
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
        border: none;
        width: 100%;
    }
    .quick-action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .expiring-item {
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 12px; 
        margin: 8px 0; 
        background: #f8f9fa; 
        border-radius: 8px; 
        border-left: 4px solid #ff6b6b;
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
            <div style="display: blue; justify-content: space-between; align-items: center; 
                        padding: 12px; margin: 8px 0; background: blue; 
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

def show_scan_product():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .product-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
    }
    .barcode-result {
        background: #e8f5e8;
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #4CAF50;
        margin: 10px 0;
    }
    .api-source {
        background: #fff3cd;
        padding: 8px 12px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 5px 0;
    }
    .free-badge {
        background: #4CAF50;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        margin-left: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header">📦 Scan Product <span class="free-badge">100% Free APIs</span></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔄 Scan Barcode")
        
        uploaded_file = st.file_uploader(
            "Upload product barcode image", 
            type=['png', 'jpg', 'jpeg'],
            help="Take a clear picture of the product barcode."
        )
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Barcode Image", use_column_width=True)
            
            if st.button("🔍 Scan Barcode", type="primary"):
                with st.spinner("Scanning barcode using free global databases..."):
                    try:
                        barcode_data = scan_barcode(uploaded_file)
                        
                        if barcode_data['success']:
                            st.success("✅ Barcode scanned successfully!")
                            
                            # Get product information from FREE APIs only
                            product_info = get_product_info_free_only(barcode_data['barcode'])
                            
                            display_product_info_free(product_info, barcode_data)
                            process_cashback_reward(product_info)
                            
                        else:
                            st.error("❌ Could not detect barcode. Please try with a clearer image.")
                            st.info("💡 Tips for better scanning:")
                            st.write("- Ensure good lighting")
                            st.write("- Keep camera steady")
                            st.write("- Focus on the barcode")
                            
                    except Exception as e:
                        st.error(f"❌ Scanning error: {str(e)}")
        
        # Manual barcode entry
        st.subheader("🔢 Manual Entry")
        manual_barcode = st.text_input("Or enter barcode manually:", placeholder="e.g., 8901234567890")
        if st.button("Lookup Product") and manual_barcode:
            with st.spinner("Looking up product from free databases..."):
                product_info = get_product_info_free_only(manual_barcode)
                display_product_info_free(product_info, {'barcode': manual_barcode, 'format': 'Manual Entry'})
                process_cashback_reward(product_info)
    
    with col2:
        st.subheader("💡 How It Works")
        st.markdown("""
        1. **Take a clear photo** of the product barcode
        2. **Upload the image** using the file picker
        3. **AI scans the barcode** using computer vision
        4. **Fetch real product details** from free global databases
        5. **Earn ₹2 cashback** for each product scanned
        
        🌐 **Free Data Sources:**
        - Open Food Facts (Global Community)
        - USDA FoodData (Government Data)
        - Barcode Monster (Free API)
        - Open FDA (Government API)
        - EU Food Database
        - Local Indian Products
        
        🎯 **All APIs are 100% Free - No Keys Required!**
        """)
        
        # Free API Status
        st.subheader("🌐 Free API Status")
        api_status = check_free_api_status()
        for api, status in api_status.items():
            if "✅" in status:
                st.success(f"{api}: {status}")
            else:
                st.warning(f"{api}: {status}")
        
        # Recent scans
        display_recent_scans()

def get_product_info_free_only(barcode):
    """
    Get product information from FREE APIs only - no keys required
    """
    st.info(f"🔍 Searching for product {barcode} in free databases...")
    
    # All FREE APIs (no keys needed)
    free_apis = [
        ("Open Food Facts", get_from_open_food_facts_enhanced),
        ("USDA FoodData", get_from_usda_food_data),
        ("Barcode Monster", get_from_barcode_monster),
        ("Open FDA", get_from_open_fda),
    ]
    
    results = []
    used_apis = []
    
    for api_name, api_function in free_apis:
        try:
            product_data = api_function(barcode)
            if product_data['success']:
                score = score_product_data(product_data)
                product_data['score'] = score
                product_data['api_name'] = api_name
                results.append(product_data)
                used_apis.append(api_name)
                
                st.success(f"✅ {api_name} found product data")
                
        except Exception as e:
            continue
    
    # Show which FREE APIs were used
    if used_apis:
        st.info(f"📡 Free APIs used: {', '.join(used_apis)}")
    
    # Return the best result
    if results:
        best_result = max(results, key=lambda x: x.get('score', 0))
        st.success(f"🎯 Best free data from: {best_result['api_name']} (Score: {best_result['score']}/10)")
        return best_result
    
    # Final fallback to local database
    st.warning("⚠️ No free API found product data, using local database")
    return get_product_from_local_db(barcode)

def get_from_open_food_facts_enhanced(barcode):
    try:
        api_url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 1:
                product = data['product']
                brand = extract_brand_enhanced(product)
                name = extract_product_name(product)
                category = extract_category(product)
                
                return {
                    'success': True,
                    'name': name,
                    'brand': brand,
                    'category': category,
                    'image_url': product.get('image_url', ''),
                    'quantity': product.get('quantity', ''),
                    'ingredients': product.get('ingredients_text', ''),
                    'nutrition_grade': product.get('nutrition_grades', '').upper(),
                    'barcode': barcode,
                    'source': 'Open Food Facts 🌍 (Free)'
                }
    except:
        pass
    return {'success': False}

def get_from_usda_food_data(barcode):
    try:
        demo_url = f"https://api.nal.usda.gov/fdc/v1/foods/search"
        params = {
            'api_key': 'DEMO_KEY',
            'query': barcode,
            'pageSize': 1
        }
        
        response = requests.get(demo_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('foods') and len(data['foods']) > 0:
                food = data['foods'][0]
                return {
                    'success': True,
                    'name': food.get('description', f'Product {barcode}'),
                    'brand': food.get('brandOwner', 'Unknown Brand'),
                    'category': food.get('foodCategory', 'General'),
                    'barcode': barcode,
                    'source': 'USDA FoodData 🥦 (Free)',
                    'nutrition': extract_nutrition_info(food)
                }
    except:
        pass
    return {'success': False}

def get_from_barcode_monster(barcode):
    try:
        api_url = f"https://barcode.monster/api/{barcode}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('product'):
                product = data['product']
                return {
                    'success': True,
                    'name': product.get('description', f'Product {barcode}'),
                    'brand': product.get('brand', 'Unknown Brand'),
                    'category': product.get('category', 'General'),
                    'image_url': product.get('image', ''),
                    'barcode': barcode,
                    'source': 'Barcode Monster 🦄 (Free)'
                }
    except:
        pass
    return {'success': False}

def get_from_open_fda(barcode):
    try:
        api_url = "https://api.fda.gov/food/enforcement.json"
        params = {
            'search': f"product_code:{barcode}",
            'limit': 1
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results') and len(data['results']) > 0:
                product = data['results'][0]
                return {
                    'success': True,
                    'name': product.get('product_description', f'Product {barcode}'),
                    'brand': product.get('recalling_firm', 'Unknown Brand'),
                    'category': 'Food',
                    'barcode': barcode,
                    'source': 'Open FDA 🏛️ (Free)'
                }
    except:
        pass
    return {'success': False}

def extract_brand_enhanced(product_data):
    brand_fields = ['brands', 'brand_owner', 'manufacturer', 'brands_tags']
    for field in brand_fields:
        if product_data.get(field):
            brand = product_data[field]
            if ',' in brand:
                brand = brand.split(',')[0]
            if brand and brand != 'Unknown':
                return brand.strip()
    
    product_name = product_data.get('product_name', '')
    common_brands = ['Amul', 'Nestle', 'Britannia', 'ITC', 'Tata', 'Patanjali']
    for brand in common_brands:
        if brand.lower() in product_name.lower():
            return brand
    
    return 'Unknown Brand'

def extract_product_name(product_data):
    name = product_data.get('product_name', '') or product_data.get('product_name_en', '')
    if not name:
        generic = product_data.get('generic_name', '')
        brand = extract_brand_enhanced(product_data)
        if generic and brand != 'Unknown Brand':
            return f"{brand} {generic}"
        return f"Product"
    
    if len(name) > 60:
        name = name[:57] + "..."
    return name

def extract_category(product_data):
    category = product_data.get('categories', '')
    if category:
        categories = category.split(',')
        if categories:
            main_category = categories[-1].strip()
            for prefix in ['en:', 'fr:', 'de:', 'es:']:
                if main_category.startswith(prefix):
                    main_category = main_category[len(prefix):]
            return main_category
    return 'General'

def extract_nutrition_info(food_data):
    nutrients = {}
    if food_data.get('foodNutrients'):
        for nutrient in food_data['foodNutrients']:
            if nutrient.get('nutrientName') and nutrient.get('value'):
                nutrients[nutrient['nutrientName']] = nutrient['value']
    return nutrients

def score_product_data(product_data):
    score = 0
    if product_data.get('brand') and product_data['brand'] != 'Unknown Brand':
        score += 3
    if product_data.get('image_url'):
        score += 2
    if product_data.get('category') and product_data['category'] != 'General':
        score += 2
    additional_fields = ['nutrition', 'ingredients', 'quantity', 'description']
    for field in additional_fields:
        if product_data.get(field):
            score += 1
            break
    return min(score, 10)

def display_product_info_free(product_info, barcode_data):
    if product_info['success']:
        st.markdown(f"""
        <div class="api-source">
            <strong>Free Data Source:</strong> {product_info.get('source', 'Unknown')}
            {f" | <strong>Quality Score:</strong> {product_info.get('score', 'N/A')}/10" if product_info.get('score') else ""}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="barcode-result">', unsafe_allow_html=True)
        st.subheader("📦 Product Details")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Product:** {product_info['name']}")
            st.write(f"**Brand:** {product_info['brand']}")
            st.write(f"**Category:** {product_info['category']}")
        with col2:
            st.write(f"**Barcode:** {barcode_data['barcode']}")
            st.write(f"**Format:** {barcode_data.get('format', 'Unknown')}")
            if product_info.get('quantity'):
                st.write(f"**Quantity:** {product_info['quantity']}")
        
        if product_info.get('image_url'):
            try:
                st.image(product_info['image_url'], caption=product_info['name'], width=200)
            except:
                st.info("📷 Product image not available")
        
        if product_info.get('nutrition_grade'):
            st.write(f"**Nutrition Grade:** {product_info['nutrition_grade']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Spoilage prediction
        spoilage_info = predict_spoilage_date(product_info['category'])
        st.subheader("📅 Shelf Life Prediction")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Base Shelf Life", f"{spoilage_info['base_days']} days")
            st.metric("Climate Factor", f"{spoilage_info['adjustment']}%")
        with col_b:
            st.metric("Adjusted Shelf Life", f"{spoilage_info['adjusted_days']} days")
            st.metric("Expiry Date", spoilage_info['expiry_date'])
        
        # Storage tips
        st.subheader("💡 Storage Tips")
        storage_tips = get_storage_tips(product_info['category'])
        for tip in storage_tips:
            st.write(f"• {tip}")

def check_free_api_status():
    """Check status of FREE APIs"""
    apis_status = {}
    
    # Open Food Facts
    try:
        response = requests.get("https://world.openfoodfacts.org/", timeout=5)
        apis_status['Open Food Facts'] = "✅ Online (Free)" if response.status_code == 200 else "❌ Offline"
    except:
        apis_status['Open Food Facts'] = "❌ Offline"
    
    # USDA FoodData
    try:
        response = requests.get("https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query=test", timeout=5)
        apis_status['USDA FoodData'] = "✅ Online (Free Demo)" if response.status_code == 200 else "❌ Offline"
    except:
        apis_status['USDA FoodData'] = "❌ Offline"
    
    # Barcode Monster
    try:
        response = requests.get("https://barcode.monster/", timeout=5)
        apis_status['Barcode Monster'] = "✅ Online (Free)" if response.status_code == 200 else "❌ Offline"
    except:
        apis_status['Barcode Monster'] = "❌ Offline"
    
    # Open FDA
    try:
        response = requests.get("https://api.fda.gov/food/enforcement.json?limit=1", timeout=5)
        apis_status['Open FDA'] = "✅ Online (Free)" if response.status_code == 200 else "❌ Offline"
    except:
        apis_status['Open FDA'] = "❌ Offline"
    
    return apis_status

def scan_barcode(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        image_np = np.array(image)
        if len(image_np.shape) == 3:
            gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        else:
            gray = image_np
        
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, 11, 2)
        
        barcodes = pyzbar.decode(thresh)
        if not barcodes:
            barcodes = pyzbar.decode(gray)
        
        if barcodes:
            barcode = barcodes[0]
            return {
                'success': True,
                'barcode': barcode.data.decode("utf-8"),
                'format': barcode.type,
                'message': f'Found {barcode.type} barcode'
            }
        else:
            return {'success': False, 'error': 'No barcode detected'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def process_cashback_reward(product_info):
    # Simulate cashback processing
    cashback_amount = 2
    st.balloons()
    st.success(f"🎉 Earned ₹{cashback_amount} cashback for scanning {product_info['name']}!")
    st.info(f"💰 Your cashback balance has been updated!")

def predict_spoilage_date(category):
    base_shelf_life = {
        'Dairy': 7, 'Grains': 180, 'Beverages': 365, 'Bakery': 5,
        'Instant Food': 180, 'Snacks': 90, 'Sweeteners': 365, 'General': 30
    }
    base_days = base_shelf_life.get(category, 30)
    adjustment = 0.8  # Default for Indian climate
    adjusted_days = int(base_days * adjustment)
    expiry_date = (datetime.now() + timedelta(days=adjusted_days)).strftime('%b %d, %Y')
    
    return {
        'base_days': base_days,
        'adjustment': int((1 - adjustment) * 100),
        'adjusted_days': adjusted_days,
        'expiry_date': expiry_date
    }

def get_storage_tips(category):
    tips = {
        'Dairy': ["Store in refrigerator at 4°C or below", "Keep in original packaging"],
        'Grains': ["Store in airtight containers", "Keep in cool, dry place"],
        'Bakery': ["Store in bread box", "Freeze for longer storage"]
    }
    return tips.get(category, ["Store in cool, dry place", "Keep away from direct sunlight"])

def display_recent_scans():
    st.subheader("📋 Recent Scans")
    st.info("Scan products to see your history here!")

def get_product_from_local_db(barcode):
    local_products = {
        # Amul Products
        '8901234567890': {'name': 'Amul Taaza Milk', 'brand': 'Amul', 'category': 'Dairy'},
        '8901000101020': {'name': 'Amul Butter', 'brand': 'Amul', 'category': 'Dairy'},
        '8901060310122': {'name': 'Amul Cheese', 'brand': 'Amul', 'category': 'Dairy'},
        '8901060700125': {'name': 'Amul Paneer', 'brand': 'Amul', 'category': 'Dairy'},
        '8901060740121': {'name': 'Amul Yogurt', 'brand': 'Amul', 'category': 'Dairy'},
        
        # ITC Products
        '8901234567891': {'name': 'Aashirvaad Atta', 'brand': 'ITC', 'category': 'Grains'},
        '8901493003016': {'name': 'Aashirvaad Select Sharbati Atta', 'brand': 'ITC', 'category': 'Grains'},
        '8901493004013': {'name': 'Sunfeast Biscuits', 'brand': 'ITC', 'category': 'Snacks'},
        '8901493005010': {'name': 'Bingo Mad Angles', 'brand': 'ITC', 'category': 'Snacks'},
        '8901493101019': {'name': 'YiPPee Noodles', 'brand': 'ITC', 'category': 'Instant Food'},
        
        # Nestle Products
        '8901000201028': {'name': 'Maggi Noodles', 'brand': 'Nestle', 'category': 'Instant Food'},
        '8901000201042': {'name': 'Maggi Masala', 'brand': 'Nestle', 'category': 'Spices'},
        '8901000201066': {'name': 'Nescafe Coffee', 'brand': 'Nestle', 'category': 'Beverages'},
        '8901000201080': {'name': 'KitKat Chocolate', 'brand': 'Nestle', 'category': 'Snacks'},
        '8901000201103': {'name': 'Milkmaid Condensed Milk', 'brand': 'Nestle', 'category': 'Dairy'},
        
        # Britannia Products
        '8901060900128': {'name': 'Britannia Bread', 'brand': 'Britannia', 'category': 'Bakery'},
        '8901060901125': {'name': 'Britannia Cake', 'brand': 'Britannia', 'category': 'Bakery'},
        '8901060902122': {'name': 'Britannia Biscuits', 'brand': 'Britannia', 'category': 'Snacks'},
        '8901060903129': {'name': 'Good Day Cookies', 'brand': 'Britannia', 'category': 'Snacks'},
        '8901060904126': {'name': 'Tiger Biscuits', 'brand': 'Britannia', 'category': 'Snacks'},
        
        # Patanjali Products
        '8901234567894': {'name': 'Patanjali Ghee', 'brand': 'Patanjali', 'category': 'Dairy'},
        '8904185100014': {'name': 'Patanjali Dant Kanti', 'brand': 'Patanjali', 'category': 'Personal Care'},
        '8904185100021': {'name': 'Patanjali Honey', 'brand': 'Patanjali', 'category': 'Sweeteners'},
        '8904185100038': {'name': 'Patanjali Atta', 'brand': 'Patanjali', 'category': 'Grains'},
        '8904185100045': {'name': 'Patanjali Biscuits', 'brand': 'Patanjali', 'category': 'Snacks'},
    }
    
    if barcode in local_products:
        product_data = local_products[barcode]
        product_data.update({
            'success': True,
            'barcode': barcode,
            'source': 'Local Database 🗂️'
        })
        return product_data
    
    return {
        'success': True,
        'name': f'Product {barcode}',
        'brand': 'Unknown Brand',
        'category': 'General',
        'barcode': barcode,
        'source': 'Basic Database'
    }

def show_voice_log():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .meal-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
    }
    .recording-section {
        background: #e8f5e8;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header">🎤 Voice Log</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎤 Record Your Meal")
        
        # Voice recording section
        st.info("Speak your meal in English or Hindi. Example: 'I ate 2 roti, dal, and sabzi'")
        
        # Audio recorder (simulated since audio_recorder_streamlit might not be available)
        st.markdown('<div class="recording-section">', unsafe_allow_html=True)
        st.write("🎙️ **Voice Recorder**")
        
        # Simulate recording button
        if st.button("🎤 Start Recording", key="start_recording"):
            st.session_state.recording = True
            st.info("🔴 Recording... Speak now!")
            
        if st.session_state.get('recording'):
            if st.button("⏹️ Stop Recording", key="stop_recording"):
                st.session_state.recording = False
                st.success("✅ Recording saved!")
                
                # Process the recording
                with st.spinner("Processing your voice..."):
                    time.sleep(2)
                    meal_data = mock_speech_recognition()
                    
                    st.success("✅ Meal logged successfully!")
                    
                    # Display parsed meal
                    st.subheader("🍽️ Meal Details")
                    for item in meal_data['items']:
                        st.write(f"• {item}")
                    
                    st.write(f"**Total Calories:** {meal_data['calories']} kcal")
                    
                    # Process cashback
                    process_voice_cashback(meal_data)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Manual entry fallback
        st.subheader("📝 Manual Entry")
        meal_text = st.text_area("Or type your meal here:", placeholder="e.g., I ate 2 roti, dal, and sabzi for lunch")
        if st.button("Log Meal Manually"):
            if meal_text:
                st.success(f"✅ Meal logged: {meal_text}")
                # Process manual entry cashback
                process_manual_cashback(meal_text)
            else:
                st.error("Please enter your meal details")
    
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
        **English:**
        - "I ate 2 roti and dal"
        - "Breakfast: poha and tea"  
        - "Lunch: rice, sambar, potato fry"
        - "Dinner: chapati, paneer, salad"
        
        **Hindi:**
        - "मैंने 2 रोटी और दाल खाई"
        - "नाश्ता: पोहा और चाय"
        - "दोपहर का खाना: चावल, सांभर, आलू की सब्जी"
        - "रात का खाना: चपाती, पनीर, सलाद"
        """)
        
        # Today's logs
        st.subheader("📊 Today's Logs")
        today_logs = [
            {"meal": "Breakfast", "items": "Poha, Tea", "time": "8:00 AM", "calories": 280},
            {"meal": "Lunch", "items": "Roti, Dal, Rice, Salad", "time": "1:30 PM", "calories": 520}
        ]
        
        for log in today_logs:
            with st.expander(f"🍽️ {log['meal']} ({log['time']})"):
                st.write(f"**Items:** {log['items']}")
                st.write(f"**Calories:** {log['calories']} kcal")
                st.write(f"**Cashback:** ₹0.50")

def mock_speech_recognition():
    """Mock speech recognition for prototype"""
    sample_meals = [
        {
            "items": ["2 Roti", "Dal", "Mixed Vegetables", "Salad"],
            "calories": 485,
            "meal_type": "Lunch"
        },
        {
            "items": ["Rice", "Sambar", "Potato Fry", "Curd"],
            "calories": 520,
            "meal_type": "Lunch"
        },
        {
            "items": ["Poha", "Tea", "Fruits"],
            "calories": 320,
            "meal_type": "Breakfast"
        },
        {
            "items": ["3 Chapati", "Paneer Butter Masala", "Naan"],
            "calories": 650,
            "meal_type": "Dinner"
        },
        {
            "items": ["Idli", "Sambar", "Coconut Chutney"],
            "calories": 280,
            "meal_type": "Breakfast"
        }
    ]
    
    import random
    return random.choice(sample_meals)

def process_voice_cashback(meal_data):
    """Process cashback for voice-logged meals"""
    cashback_amount = 0.50
    st.balloons()
    st.success(f"🎉 Earned ₹{cashback_amount} cashback for logging your {meal_data.get('meal_type', 'meal')}!")
    st.info(f"💰 Your cashback balance has been updated!")
    
    # Display nutritional insights
    st.subheader("📊 Nutritional Insights")
    calories = meal_data['calories']
    
    if calories < 300:
        st.info(f"🍃 Light meal - {calories} kcal (Good for snacks/small meals)")
    elif calories < 500:
        st.success(f"⚖️ Balanced meal - {calories} kcal (Ideal portion size)")
    else:
        st.warning(f"🔥 Heavy meal - {calories} kcal (Consider smaller portions)")
    
    # Food waste prevention tips
    st.subheader("💡 Food Waste Tips")
    tips = [
        "Store leftovers properly to extend shelf life",
        "Plan portions to avoid overcooking",
        "Use vegetable peels for stocks or composting",
        "Freeze excess food for later use"
    ]
    
    for tip in tips:
        st.write(f"• {tip}")

def process_manual_cashback(meal_text):
    """Process cashback for manually logged meals"""
    cashback_amount = 0.50
    st.balloons()
    st.success(f"🎉 Earned ₹{cashback_amount} cashback for logging your meal!")
    st.info(f"💰 Your cashback balance has been updated!")
    
    # Simple analysis based on keywords
    st.subheader("📊 Quick Analysis")
    
    if any(word in meal_text.lower() for word in ['leftover', 'excess', 'extra']):
        st.warning("⚠️ You mentioned leftovers - great for reducing food waste!")
    
    if any(word in meal_text.lower() for word in ['fresh', 'new', 'just cooked']):
        st.success("🌱 Fresh meal - consider portion control to avoid waste")
    
    # General tips
    st.subheader("💡 Meal Logging Benefits")
    benefits = [
        "Helps track eating patterns and reduce overbuying",
        "Identifies frequently wasted food items",
        "Provides insights for better meal planning",
        "Reduces food waste through conscious consumption"
    ]
    
    for benefit in benefits:
        st.write(f"• {benefit}")

def show_donate_food():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .donation-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
    }
    .impact-section {
        background: #e8f5e8;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        margin: 10px 0;
    }
    .ngo-card {
        background: #fff3cd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
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
                    # Simulate AI food detection
                    time.sleep(2)
                    detection_result = mock_food_detection(uploaded_file)
                    
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
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("People Fed", "156")
        with col2:
            st.metric("Food Donated", "78 kg")
        with col3:
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

def mock_food_detection(uploaded_file):
    """Mock AI food detection for prototype"""
    food_categories = [
        "Cooked Rice", "Chapati/Roti", "Vegetable Curry", "Dal/Lentils", 
        "Fruits", "Bread", "Cooked Vegetables", "Sweets", "Snacks"
    ]
    
    # Generate random detections
    num_detections = random.randint(1, 4)
    detections = []
    total_weight_grams = 0
    
    for i in range(num_detections):
        category = random.choice(food_categories)
        weight = random.randint(200, 1000)  # 200g to 1000g
        confidence = round(random.uniform(0.7, 0.95), 2)
        
        detections.append({
            'category': category,
            'estimated_weight_grams': weight,
            'confidence': confidence
        })
        total_weight_grams += weight
    
    return {
        'success': True,
        'detections': detections,
        'total_weight_kg': round(total_weight_grams / 1000, 2),
        'message': f'Detected {num_detections} food items'
    }

def find_nearby_ngos():
    """Find nearby NGOs for donation"""
    return [
        {"name": "Akshaya Patra", "distance": "2.3 km", "rating": "4.8★", "specialization": "Meals for Children"},
        {"name": "Robin Hood Army", "distance": "4.1 km", "rating": "4.7★", "specialization": "Hunger Relief"},
        {"name": "Feeding India", "distance": "5.2 km", "rating": "4.6★", "specialization": "Food Distribution"},
        {"name": "No Food Waste", "distance": "3.7 km", "rating": "4.5★", "specialization": "Food Rescue"}
    ]

def process_donation(detection_result, ngo_name, image_name):
    """Process the donation and issue rewards"""
    
    # Process cashback
    cashback_amount = 50
    st.balloons()
    st.success("🎉 Donation confirmed successfully!")
    
    # Display rewards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Cashback Earned", f"₹{cashback_amount}")
    
    with col2:
        people_fed = int(detection_result['total_weight_kg'] * 2)  # Approx 2 people per kg
        st.metric("People Fed", people_fed)
    
    with col3:
        tax_saving = int(detection_result['total_weight_kg'] * 50)  # ₹50 per kg tax benefit
        st.metric("Tax Benefit", f"₹{tax_saving}")
    
    # Donation details
    st.subheader("📋 Donation Details")
    st.write(f"**NGO:** {ngo_name}")
    st.write(f"**Total Food Donated:** {detection_result['total_weight_kg']} kg")
    st.write(f"**Food Items:** {', '.join([d['category'] for d in detection_result['detections']])}")
    st.write(f"**Donation Time:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Pickup information
    st.subheader("🚚 Pickup Information")
    st.info(f"""
    **{ngo_name}** will contact you within 2 hours to schedule pickup.
    
    📞 Contact: +91-XXXXXX-XXXX
    📧 Email: contact@{ngo_name.lower().replace(' ', '')}.org
    ⏰ Estimated Pickup: Today, 4-6 PM
    """)
    
    # Social share
    st.subheader("📢 Share Your Impact")
    share_message = f"""
    I just donated {detection_result['total_weight_kg']}kg of food through FoodSaver App! 
    🍽️ Fed {people_fed} people and earned ₹50 cashback + tax benefits. 
    Join me in fighting food waste! ❤️
    #FoodSaver #StopFoodWaste #FeedTheHungry
    """
    
    st.code(share_message)
    
    if st.button("📱 Copy Message to Share"):
        st.success("Message copied to clipboard! Share it on social media 🎉")
    
    # Next steps
    st.subheader("📝 Next Steps")
    st.write("1. Keep the food properly packaged and ready for pickup")
    st.write("2. You'll receive a confirmation call from the NGO")
    st.write("3. Track your donation status in the app")
    st.write("4. Tax certificate will be emailed within 7 days")

def main():
    # Initialize session state for page navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Dashboard"

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

    # Update current page based on sidebar selection
    st.session_state.current_page = page

    # Logout button
    if st.sidebar.button("🚪 Logout"):
        logout()

    # Page routing
    if st.session_state.current_page == "🏠 Dashboard":
        show_dashboard()
    elif st.session_state.current_page == "📦 Scan Product":
        show_scan_product()
    elif st.session_state.current_page == "🎤 Voice Log":
        show_voice_log()
    elif st.session_state.current_page == "❤️ Donate Food":
        show_donate_food()

if __name__ == "__main__":
    main()
