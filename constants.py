"""
constants.py - config หลัก sharkcial-loan-bot
"""
# ดอกเบี้ยต่อชั่วโมง
INTEREST_RATE = 0.10
# Cooldown (นาที)
REQUEST_COOLDOWN_MINUTES = 10
# วงเงินเริ่มต้น
DEFAULT_CREDIT_LIMIT = 20
# วงเงินขั้นต่ำ
MIN_CREDIT_LIMIT = 10
# จำนวนชั่วโมงที่ถือว่า defaulted
DEFAULTED_HOURS = 24
# Role admin
ADMIN_ROLE_NAME = "admin"
# Guild field name (ถ้ารองรับ multiguild)
GUILD_FIELD = "guild_id"
