"""
supabase.py - ฟังก์ชันเชื่อมต่อและ CRUD กับ Supabase
สำหรับ users, loans, transactions ของ sharkcial-loan-bot-v3
"""
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
sb = create_client(SUPABASE_URL, SUPABASE_KEY)

# ========================
# USERS
# ========================

def get_user(user_id, guild_id):
    """ดึงข้อมูล user ตาม user_id และ guild_id"""
    try:
        res = sb.table("users").select("*").eq("user_id", user_id).eq("guild_id", guild_id).single().execute()
        return res.data
    except Exception as e:
        print(f"[Supabase] get_user error: {e}")
        return None

def add_user(user_id, guild_id, display_name=None, credit_limit=20):
    """เพิ่ม user ใหม่"""
    data = {
        "user_id": user_id,
        "guild_id": guild_id,
        "display_name": display_name,
        "credit_limit": credit_limit
    }
    try:
        res = sb.table("users").insert(data).execute()
        return res.data
    except Exception as e:
        print(f"[Supabase] add_user error: {e}")
        return None

def update_user(user_id, guild_id, **fields):
    """อัปเดตข้อมูล user"""
    try:
        res = sb.table("users").update(fields).eq("user_id", user_id).eq("guild_id", guild_id).execute()
        return res.data
    except Exception as e:
        print(f"[Supabase] update_user error: {e}")
        return None

# ========================
# LOANS
# ========================

def add_loan(user_id, guild_id, amount, status="pending", requested_at=None, approved_at=None, admin_id=None):
    """สร้างคำขอกู้ใหม่"""
    data = {
        "user_id": user_id,
        "guild_id": guild_id,
        "amount": amount,
        "status": status,
        "requested_at": requested_at,
        "approved_at": approved_at,
        "admin_id": admin_id
    }
    try:
        res = sb.table("loans").insert(data).execute()
        return res.data
    except Exception as e:
        print(f"[Supabase] add_loan error: {e}")
        return None

def get_loans_by_user(user_id, guild_id, status=None):
    """ดึง loan ของ user ใน guild นั้น ๆ (optionally filter by status)"""
    q = sb.table("loans").select("*").eq("user_id", user_id).eq("guild_id", guild_id)
    if status:
        q = q.eq("status", status)
    try:
        res = q.execute()
        return res.data
    except Exception as e:
        print(f"[Supabase] get_loans_by_user error: {e}")
        return []

def update_loan(loan_id, **fields):
    """อัปเดตข้อมูล loan ตาม loan_id"""
    try:
        res = sb.table("loans").update(fields).eq("id", loan_id).execute()
        return res.data
    except Exception as e:
        print(f"[Supabase] update_loan error: {e}")
        return None

# ========================
# TRANSACTIONS
# ========================

def add_transaction(user_id, guild_id, loan_id, action, amount=None, interest=None, admin_id=None):
    """บันทึกธุรกรรม (เช่น request, approve, pay, interest, etc.)"""
    data = {
        "user_id": user_id,
        "guild_id": guild_id,
        "loan_id": loan_id,
        "action": action,
        "amount": amount,
        "interest": interest,
        "admin_id": admin_id
    }
    try:
        res = sb.table("transactions").insert(data).execute()
        return res.data
    except Exception as e:
        print(f"[Supabase] add_transaction error: {e}")
        return None

def get_transactions_by_user(user_id, guild_id):
    """ดึงธุรกรรมทั้งหมดของ user"""
    try:
        res = sb.table("transactions").select("*").eq("user_id", user_id).eq("guild_id", guild_id).order("created_at", desc=True).execute()
        return res.data
    except Exception as e:
        print(f"[Supabase] get_transactions_by_user error: {e}")
        return []
