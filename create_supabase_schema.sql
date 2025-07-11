-- SQL สำหรับสร้างตารางหลัก sharkcial-loan-bot-v3
-- ตาราง users
CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id text NOT NULL,
  guild_id text NOT NULL,
  display_name text,
  credit_limit int DEFAULT 20,
  is_blocked boolean DEFAULT FALSE,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS users_userid_guildid_idx ON users(user_id, guild_id);

-- ตาราง loans
CREATE TABLE IF NOT EXISTS loans (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id text NOT NULL,
  guild_id text NOT NULL,
  amount int NOT NULL,
  status text NOT NULL CHECK (status IN ('pending', 'approved', 'rejected', 'paid', 'defaulted')),
  requested_at timestamptz DEFAULT now(),
  approved_at timestamptz,
  paid_at timestamptz,
  interest_accrued float DEFAULT 0,
  admin_id text,
  FOREIGN KEY (user_id, guild_id) REFERENCES users(user_id, guild_id)
);

-- ตาราง transactions
CREATE TABLE IF NOT EXISTS transactions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id text NOT NULL,
  guild_id text NOT NULL,
  loan_id uuid,
  action text NOT NULL, -- เช่น request, approve, pay, interest, etc.
  amount int,
  interest float,
  admin_id text,
  created_at timestamptz DEFAULT now()
);

-- เปิด RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE loans ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

-- Policy: ให้ owner เห็น/แก้ของตัวเอง, admin เห็นหมด (สามารถปรับเพิ่มภายหลัง)
-- (ตัวอย่าง policy สำหรับ users)
CREATE POLICY "Users can view their own info" ON users
  FOR SELECT USING (auth.uid()::text = user_id);
CREATE POLICY "Admins can view all users" ON users
  FOR SELECT USING (EXISTS (SELECT 1 FROM auth.users WHERE id = auth.uid() AND raw_user_meta_data->>'role' = 'admin'));
