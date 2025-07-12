# db.py
"""
Database functions for sharkberg-bot.
- Connects to Supabase/PostgreSQL
- Provides CRUD operations for users, loans, transactions
"""

from supabase_helpers import (
    get_user as sb_get_user,
    add_loan as sb_add_loan,
    update_loan as sb_update_loan,
    add_transaction as sb_add_transaction,
)

# --- User functions ---
def get_user(user_id, guild_id):
    return sb_get_user(user_id, guild_id)

def set_display_name(user_id, guild_id, display_name):
    # ใช้ update_user ของ supabase_helpers
    from supabase_helpers import update_user
    return update_user(user_id, guild_id, display_name=display_name)

# --- Loan functions ---

def get_loan_history(user_id, guild_id):
    """
    ดึงประวัติการกู้ของ user ใน guild นั้น ๆ
    """
    from supabase_helpers import get_loans_by_user
    return get_loans_by_user(user_id, guild_id)

def sb_update_loan(loan_id, **fields):
    """
    อัปเดตข้อมูล loan ตาม loan_id (wrapper จาก supabase_helpers.update_loan)
    """
    from supabase_helpers import update_loan
    return update_loan(loan_id, **fields)

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
    result = sb_add_transaction(user_id, guild_id, loan_id, action, amount, interest, admin_id)
    # เพิ่มวงเงิน 10% ทุกครั้งที่จ่ายดอกเบี้ย (action == 'pay' และ interest > 0)
    if action == 'pay' and interest and interest > 0:
        update_credit_limit_on_interest_payment(user_id, guild_id, interest)
    return result


def update_credit_limit_on_interest_payment(user_id, guild_id, interest_paid):
    """
    เพิ่ม credit_limit ของ user 10% ของดอกเบี้ยที่จ่ายแต่ละครั้ง
    """
    from supabase_helpers import update_user
    user = sb_get_user(user_id, guild_id)
    if user and isinstance(user, dict):
        current_limit = user.get('credit_limit', 20)
        try:
            new_limit = float(current_limit) + (0.10 * float(interest_paid))
            update_user(user_id, guild_id, credit_limit=new_limit)
        except Exception as e:
            print(f'[ERROR] update_credit_limit_on_interest_payment: {e}')

