import streamlit as st
from datetime import datetime, timedelta

class CashbackSystem:
    def __init__(self):
        self.rules = {
            'product_scan': 2.00,
            'voice_log': 0.50,
            'bill_upload': 5.00,
            'recipe_used': 3.00,
            'zero_waste': 1.00,
            'donation': 50.00,
            'weekly_bonus': 15.00,
            'monthly_bonus': 50.00
        }
        
        self.daily_limits = {
            'product_scan': 5,
            'voice_log': 3,
            'bill_upload': 1,
            'recipe_used': 2,
            'zero_waste': 2,
            'donation': None  # No limit
        }
    
    def process_cashback(self, action_type, user_id, metadata=None):
        """Process cashback for user action"""
        if action_type not in self.rules:
            return {'success': False, 'error': 'Invalid action type'}
        
        # Check daily limits
        if not self.check_daily_limit(user_id, action_type):
            return {'success': False, 'error': 'Daily limit reached'}
        
        amount = self.rules[action_type]
        
        # Update user balance
        if 'cashback_balance' not in st.session_state:
            st.session_state.cashback_balance = 0
        
        st.session_state.cashback_balance += amount
        
        # Record transaction
        transaction = {
            'user_id': user_id,
            'action_type': action_type,
            'amount': amount,
            'timestamp': datetime.now(),
            'metadata': metadata
        }
        
        # Store in session state (in production, save to database)
        if 'cashback_transactions' not in st.session_state:
            st.session_state.cashback_transactions = []
        st.session_state.cashback_transactions.append(transaction)
        
        return {
            'success': True,
            'amount': amount,
            'new_balance': st.session_state.cashback_balance,
            'message': f'🎉 ₹{amount} cashback earned!'
        }
    
    def check_daily_limit(self, user_id, action_type):
        """Check if user has reached daily limit for action"""
        if action_type not in self.daily_limits or self.daily_limits[action_type] is None:
            return True
        
        today = datetime.now().date()
        user_transactions = [
            t for t in st.session_state.get('cashback_transactions', [])
            if t['user_id'] == user_id and 
            t['action_type'] == action_type and
            t['timestamp'].date() == today
        ]
        
        return len(user_transactions) < self.daily_limits[action_type]
    
    def get_user_stats(self, user_id):
        """Get user cashback statistics"""
        user_transactions = [
            t for t in st.session_state.get('cashback_transactions', [])
            if t['user_id'] == user_id
        ]
        
        today = datetime.now().date()
        today_earnings = sum(
            t['amount'] for t in user_transactions 
            if t['timestamp'].date() == today
        )
        
        monthly_earnings = sum(
            t['amount'] for t in user_transactions 
            if t['timestamp'].month == datetime.now().month
        )
        
        return {
            'total_balance': st.session_state.get('cashback_balance', 0),
            'today_earnings': today_earnings,
            'monthly_earnings': monthly_earnings,
            'total_transactions': len(user_transactions)
        }

# Global instance
cashback_system = CashbackSystem()