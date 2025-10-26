import streamlit as st
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

class FoodDetector:
    def __init__(self):
        st.success("✅ Food detection ready!")
    
    def detect_food(self, image):
        """Mock food detection for prototype"""
        # Return mock data without actual AI
        mock_foods = [
            {'category': 'Roti', 'confidence': 0.92, 'estimated_weight_grams': 40},
            {'category': 'Dal', 'confidence': 0.88, 'estimated_weight_grams': 150},
            {'category': 'Rice', 'confidence': 0.85, 'estimated_weight_grams': 200},
            {'category': 'Vegetable Curry', 'confidence': 0.78, 'estimated_weight_grams': 180},
            {'category': 'Bread', 'confidence': 0.90, 'estimated_weight_grams': 100}
        ]
        
        num_items = random.randint(2, 4)
        selected_foods = random.sample(mock_foods, num_items)
        
        total_weight = sum([f['estimated_weight_grams'] for f in selected_foods]) / 1000
        
        return {
            'success': True,
            'detections': selected_foods,
            'total_items': num_items,
            'total_weight_kg': round(total_weight, 2)
        }

class SpoilagePredictor:
    def predict_spoilage(self, food_item, purchase_date, location="Mumbai"):
        """Simple spoilage prediction without LSTM"""
        base_shelf_life = {
            'tomatoes': 7, 'potatoes': 14, 'onions': 30, 'leafy_greens': 3,
            'carrots': 21, 'milk': 5, 'paneer': 3, 'yogurt': 10,
            'atta': 180, 'rice': 365, 'dal': 365, 'bread': 7,
            'rot': 3, 'dal': 2, 'sabzi': 2
        }
        
        base_days = base_shelf_life.get(food_item.lower(), 7)
        
        # Simple adjustments
        adjustment_factors = {
            'Mumbai': 0.8, 'Delhi': 0.9, 'Bangalore': 1.0, 'Chennai': 0.7
        }
        
        adjustment = adjustment_factors.get(location, 0.8)
        adjusted_days = int(base_days * adjustment)
        
        spoilage_date = purchase_date + timedelta(days=adjusted_days)
        
        return {
            'food_item': food_item,
            'base_shelf_life_days': base_days,
            'adjusted_shelf_life_days': adjusted_days,
            'predicted_spoilage_date': spoilage_date.strftime('%Y-%m-%d'),
            'confidence': 0.85
        }
        
        
def predict_demand(historical_data, days=7):
    """
    Simple demand prediction using historical patterns
    In a real application, this would use ML models
    """
    predictions = []
    
    for dish in historical_data['dish'].unique():
        dish_data = historical_data[historical_data['dish'] == dish]
        avg_demand = dish_data['demand'].mean()
        trend = np.polyfit(range(len(dish_data)), dish_data['demand'], 1)[0]
        
        # Add some randomness and trend
        base_prediction = avg_demand + trend * len(dish_data)
        prediction = max(0, base_prediction + np.random.normal(0, 5))
        
        predictions.append({
            'dish': dish,
            'predicted_demand': prediction,
            'confidence': min(0.95, max(0.7, 0.8 + trend * 10))
        })
    
    return pd.DataFrame(predictions)

# Global instances
food_detector = FoodDetector()
spoilage_predictor = SpoilagePredictor()