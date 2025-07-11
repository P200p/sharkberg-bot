"""
supabase_client.py - ฟังก์ชันเชื่อมต่อและ CRUD กับ Supabase
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

# (คัดลอกฟังก์ชัน/โค้ดทั้งหมดจาก supabase.py เดิมมาที่นี่)
