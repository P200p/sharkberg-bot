-- SQL สำหรับสร้างตาราง credit_limits ใน Supabase
create table if not exists credit_limits (
  user_id text primary key,
  limit float not null default 20
);

-- เปิด Row Level Security
alter table credit_limits enable row level security;

-- Policy: ให้ user เห็น/แก้ไขเฉพาะของตัวเอง
create policy "ผู้ใช้สามารถดูและแก้ไขวงเงินตัวเอง" on credit_limits
for select using (user_id = auth.uid()::text);
create policy "ผู้ใช้สามารถเพิ่ม/อัปเดตวงเงินตัวเอง" on credit_limits
for insert using (user_id = auth.uid()::text);
for update using (user_id = auth.uid()::text);
