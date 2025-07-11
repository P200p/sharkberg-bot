# db.py
"""
Database functions for sharkberg-bot.
- Connects to Supabase/PostgreSQL
- Provides CRUD operations for users, loans, transactions
"""
import os
from supabase_helpers import get_user as sb_get_user, add_loan as sb_add_loan, update_loan as sb_update_loan, add_transaction as sb_add_transaction

# --- User functions ---
def get_user(user_id, guild_id):
    return sb_get_user(user_id, guild_id)

def set_display_name(user_id, guild_id, display_name):
    # ใช้ update_user ของ supabase_helpers
    from supabase_helpers import update_user
    return update_user(user_id, guild_id, display_name=display_name)

# --- Loan functions ---
def create_loan(user_id, guild_id, amount):
    # คืน loan id (หรือ object) จาก supabase
    result = sb_add_loan(user_id, guild_id, amount)
    if result and isinstance(result, list) and len(result) > 0:
        return result[0].get('id')
    return None

def approve_loan(loan_id, admin_id):
    # อัปเดต loan เป็น approved
    return sb_update_loan(loan_id, status='approved', admin_id=admin_id)

# --- Transaction functions ---
def record_transaction(user_id, guild_id, loan_id, action, amount, interest, admin_id=None):
    return sb_add_transaction(user_id, guild_id, loan_id, action, amount, interest, admin_id)
