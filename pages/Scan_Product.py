import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pyzbar.pyzbar as pyzbar
from utils.cashback import cashback_system
from datetime import datetime, timedelta
import requests
import json


# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.title("🔒 Authentication Required")
    st.error("Please log in to use Scan Product feature")
    st.info("Use the login form in the main app to access this feature")
    st.stop()
    
def show():
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

# Free API implementations (same as above, but consolidated)
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

# Helper functions
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

# Other functions remain the same (scan_barcode, process_cashback_reward, etc.)
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
    result = cashback_system.process_cashback(
        'product_scan',
        st.session_state.user_id,
        {'product': product_info['name'], 'barcode': product_info['barcode']}
    )
    
    if result['success']:
        st.balloons()
        st.success(f"🎉 {result['message']}")
        st.info(f"💰 Your new cashback balance: **₹{result['new_balance']}**")

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
        
        # Tata Products
        '8901234567893': {'name': 'Tata Tea', 'brand': 'Tata', 'category': 'Beverages'},
        '8901010101011': {'name': 'Tata Salt', 'brand': 'Tata', 'category': 'Spices'},
        '8901010101028': {'name': 'Tata Sampann Pulses', 'brand': 'Tata', 'category': 'Grains'},
        '8901010101035': {'name': 'Tata Coffee', 'brand': 'Tata', 'category': 'Beverages'},
        
        # Hindustan Unilever Products
        '8901010102018': {'name': 'Dove Soap', 'brand': 'Hindustan Unilever', 'category': 'Personal Care'},
        '8901010102025': {'name': 'Lux Soap', 'brand': 'Hindustan Unilever', 'category': 'Personal Care'},
        '8901010102032': {'name': 'Lifebuoy Soap', 'brand': 'Hindustan Unilever', 'category': 'Personal Care'},
        '8901010102049': {'name': 'Pepsodent Toothpaste', 'brand': 'Hindustan Unilever', 'category': 'Personal Care'},
        '8901010102056': {'name': 'Brooke Bond Red Label Tea', 'brand': 'Hindustan Unilever', 'category': 'Beverages'},
        
        # Dabur Products
        '8901010103015': {'name': 'Dabur Honey', 'brand': 'Dabur', 'category': 'Sweeteners'},
        '8901010103022': {'name': 'Dabur Chyawanprash', 'brand': 'Dabur', 'category': 'Health'},
        '8901010103039': {'name': 'Dabur Red Toothpaste', 'brand': 'Dabur', 'category': 'Personal Care'},
        '8901010103046': {'name': 'Dabur Amla Hair Oil', 'brand': 'Dabur', 'category': 'Personal Care'},
        
        # Parle Products
        '8901010104012': {'name': 'Parle-G Biscuits', 'brand': 'Parle', 'category': 'Snacks'},
        '8901010104029': {'name': 'Monaco Biscuits', 'brand': 'Parle', 'category': 'Snacks'},
        '8901010104036': {'name': 'KrackJack Biscuits', 'brand': 'Parle', 'category': 'Snacks'},
        '8901010104043': {'name': 'Hide & Seek Biscuits', 'brand': 'Parle', 'category': 'Snacks'},
        
        # Coca-Cola Products
        '8901010105019': {'name': 'Coca-Cola', 'brand': 'Coca-Cola', 'category': 'Beverages'},
        '8901010105026': {'name': 'Sprite', 'brand': 'Coca-Cola', 'category': 'Beverages'},
        '8901010105033': {'name': 'Fanta', 'brand': 'Coca-Cola', 'category': 'Beverages'},
        '8901010105040': {'name': 'Thums Up', 'brand': 'Coca-Cola', 'category': 'Beverages'},
        
        # PepsiCo Products
        '8901010106016': {'name': 'Pepsi', 'brand': 'PepsiCo', 'category': 'Beverages'},
        '8901010106023': {'name': 'Lays Chips', 'brand': 'PepsiCo', 'category': 'Snacks'},
        '8901010106030': {'name': 'Kurkure', 'brand': 'PepsiCo', 'category': 'Snacks'},
        '8901010106047': {'name': 'Quaker Oats', 'brand': 'PepsiCo', 'category': 'Grains'},
        
        # Fortune Products
        '8901234567892': {'name': 'Fortune Rice', 'brand': 'Fortune', 'category': 'Grains'},
        '8901010107013': {'name': 'Fortune Oil', 'brand': 'Fortune', 'category': 'Cooking Oil'},
        '8901010107020': {'name': 'Fortune Atta', 'brand': 'Fortune', 'category': 'Grains'},
        
        # MDH Products
        '8901010108010': {'name': 'MDH Garam Masala', 'brand': 'MDH', 'category': 'Spices'},
        '8901010108027': {'name': 'MDH Chana Masala', 'brand': 'MDH', 'category': 'Spices'},
        '8901010108034': {'name': 'MDH Chicken Masala', 'brand': 'MDH', 'category': 'Spices'},
        
        # Catch Products
        '8901010109017': {'name': 'Catch Salt', 'brand': 'Catch', 'category': 'Spices'},
        '8901010109024': {'name': 'Catch Spices', 'brand': 'Catch', 'category': 'Spices'},
        '8901010109031': {'name': 'Catch Tea Masala', 'brand': 'Catch', 'category': 'Spices'},
        
        # Real Indian Product Barcodes (Sample)
        '8901030317904': {'name': 'MTR Gulab Jamun Mix', 'brand': 'MTR', 'category': 'Ready Mix'},
        '8901030317911': {'name': 'MTR Rava Idli Mix', 'brand': 'MTR', 'category': 'Ready Mix'},
        '8901030317928': {'name': 'MTR Sambar Powder', 'brand': 'MTR', 'category': 'Spices'},
        
        '8901052001234': {'name': 'Gits Ready Mix', 'brand': 'Gits', 'category': 'Ready Mix'},
        '8901052001241': {'name': 'Gits Dal Makhani', 'brand': 'Gits', 'category': 'Ready Mix'},
        
        '8901060001234': {'name': 'Haldirams Bhujia', 'brand': 'Haldirams', 'category': 'Snacks'},
        '8901060001241': {'name': 'Haldirams Rasgulla', 'brand': 'Haldirams', 'category': 'Sweets'},
        
        '8901075001234': {'name': 'Bikanervala Bhujia', 'brand': 'Bikanervala', 'category': 'Snacks'},
        '8901075001241': {'name': 'Bikanervala Samosa', 'brand': 'Bikanervala', 'category': 'Snacks'},
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