# Sharkberg-bot Project Checklist

## 1. เอกสาร & คู่มือ
- [x] README.md : สรุปโปรเจค
- [x] plan : แผนงาน/Mapping ฟีเจอร์
- [x] คู่มือการใช้งานคำสั่ง.md : คู่มือ dev & user
- [ ] CHANGELOG.md : (แนะนำให้มี)
- [ ] docs/ : (สำหรับขยายเอกสาร)

## 2. Config & Environment
- [x] .env : ตัวแปรลับ
- [x] .gitignore : กันไฟล์ไม่จำเป็น
- [x] requirements.txt : รายการไลบรารี

## 3. ฐานข้อมูล & SQL
- [x] create_supabase_schema.sql : สร้าง schema
- [x] create_credit_limits.sql : SQL credit limit
- [x] data/ : เก็บไฟล์ฐานข้อมูล (ถ้ามี)

## 4. โค้ดหลัก
- [x] constants.py : config
- [ ] bot.py : logic หลัก Discord Bot (ควรสร้างใหม่)
- [ ] db.py : ฟังก์ชันฐานข้อมูล (ควรสร้างใหม่)
- [ ] commands/ : (แนะนำแยก handler ตามกลุ่มคำสั่ง)
- [x] supabase_client.py / supabase_helpers.py : ฟังก์ชันช่วยเชื่อมต่อ Supabase
- [x] utils.py : ฟังก์ชันทั่วไป

## 5. อื่นๆ
- [x] loanbot_tasks.json : (ถ้ามีข้อมูลสำคัญ)
- [x] รูปภาพ/ไฟล์ assets (ถ้าต้องใช้)

---

### ข้อเสนอแนะถัดไป
- สร้างไฟล์/โฟลเดอร์ที่ยังขาด เช่น bot.py, db.py, commands/
- จัดระเบียบไฟล์เอกสาร (เพิ่ม CHANGELOG.md, docs/ ถ้าต้องการ)
- ตรวจสอบ .env, .gitignore ว่าครอบคลุมไฟล์สำคัญ
- ย้ายไฟล์ที่ไม่เกี่ยวกับโค้ด (เช่น รูปภาพ) ไปโฟลเดอร์ assets/ หรือ images/ เพื่อความเป็นระเบียบ
