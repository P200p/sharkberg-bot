"""
utils.py - ฟังก์ชันช่วยสำหรับ sharkcial-loan-bot-v3
รวมฟังก์ชันจัดการไฟล์, log, datetime, validation ฯลฯ
"""
import json
from datetime import datetime

# ฟังก์ชันโหลดไฟล์ JSON

def load_json(filepath, default=None):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default if default is not None else {}

# ฟังก์ชันบันทึกไฟล์ JSON

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ฟังก์ชันแปลง timestamp เป็น string

def now_iso():
    return datetime.now().isoformat()

# ฟังก์ชันคำนวณเวลาห่าง (นาที)

def minutes_since(iso_str):
    t = datetime.fromisoformat(iso_str)
    return (datetime.now() - t).total_seconds() / 60

# ฟังก์ชัน validate user id

def is_valid_user_id(user_id):
    return isinstance(user_id, str) and user_id.isdigit()
