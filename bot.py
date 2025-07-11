"""
Main Discord bot logic for sharkberg-bot.
- Loads commands from commands/
- Connects to DB via db.py
- Uses environment variables from .env
<<<<<<< Updated upstream
- Now also exposes a /chat API endpoint (via FastAPI) to talk to Together.ai
=======
>>>>>>> Stashed changes
"""

import os
import json
import random
import datetime
import asyncio
<<<<<<< Updated upstream
import requests

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from threading import Thread
from db import get_user, create_loan, approve_loan, record_transaction
from utils import now_iso, minutes_since

=======
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from db import get_user, create_loan, approve_loan, record_transaction
from utils import now_iso, minutes_since

# เพิ่ม import สำหรับ Together API
import requests

>>>>>>> Stashed changes
# โหลด env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
MAIN_CHANNEL_ID = int(os.getenv("MAIN_CHANNEL_ID", "0"))
LAST_MSG_FILE = "data/last_msg.json"
<<<<<<< Updated upstream
API_KEY = os.getenv("TOGETHER_API_KEY", "")
MODEL = os.getenv("TOGETHER_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")

if not API_KEY:
    raise ValueError("❌ TOGETHER_API_KEY not found in .env")
=======

# ดึง Together API KEY และ Model
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_MODEL = os.getenv("TOGETHER_MODEL", "meta-llama/Llama-3-70B-Instruct")
>>>>>>> Stashed changes

# เตรียม intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ดึงไฟล์คำสั่งทั้งหมดใน /commands
import pathlib


async def load_extensions():
    for cmd_file in pathlib.Path("commands").glob("*.py"):
        if cmd_file.name != "__init__.py":
            try:
                await bot.load_extension(f"commands.{cmd_file.stem}")
                print(f"✅ Loaded extension: {cmd_file.stem}")
            except Exception as e:
                print(f"❌ Failed to load extension {cmd_file.stem}: {e}")
                import traceback

                traceback.print_exc()


# ใช้เก็บเวลาข้อความล่าสุดของแต่ละเซิร์ฟเวอร์
last_msg = {}


def save_last_msg():
    with open(LAST_MSG_FILE, "w") as f:
        json.dump({str(k): v.isoformat() for k, v in last_msg.items()}, f)


def load_last_msg():
    global last_msg
    try:
        with open(LAST_MSG_FILE, "r") as f:
            last_msg = {
                int(k): datetime.datetime.fromisoformat(v)
                for k, v in json.load(f).items()
            }
    except (FileNotFoundError, json.JSONDecodeError):
<<<<<<< Updated upstream
        print("Warning: Could not load last message data. Starting fresh.")
=======
        print(f"Warning: Could not load last message data. Starting fresh.")
>>>>>>> Stashed changes
        last_msg = {}


# เนื้อเพลงสาระโอเกะ
lyrics = [
    "ใจมันได้! สายปั่นต้องสู้!",
    "หมุนต่อไม่รอแล้วนะ!",
    "สล็อตแตกง่าย ใครไม่ลองถือว่าพลาด!",
    "ขอกำลังใจหน่อย จะหมุนแล้ว!",
    "ถ้าแตกวันนี้ จะไปวิ่งรอบบ้าน!",
    "บอทสายปั่นขอแจ้งเตือน: อย่าลืมเติมน้ำก่อนหมุน!",
    "ถ้าปั่นไม่แตก ลองเปลี่ยนมือหมุนดูมั้ย?",
    "สูตรลับสายปั่น: ใส่ถุงเท้าก่อนเล่น เพิ่มโชค!",
    "บอทยังฮาไม่เท่าเจ้าของเพจ x.com/Omgnhoy นะ!",
    "อยากแตกต้องอดทน อยากฮาต้องทัก Omgnhoy!",
    "ถามยากแบบนี้ ขอไปถามทวิตเตอร์ @Omgnhoy ก่อนนะ!",
    "ถ้าตอบไม่ได้ เดี๋ยวไปขอสูตรจาก x.com/Omgnhoy ให้!",
]


@tasks.loop(minutes=5)
async def check_inactivity():
    """โพสต์เนื้อเพลงหากไม่มีคนคุยเกิน 1 ชั่วโมง"""
    if not hasattr(bot, "user"):
        return
<<<<<<< Updated upstream
    try:
        now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
        for guild in bot.guilds:
            if guild.id not in last_msg:
                continue
            last = last_msg[guild.id].replace(tzinfo=None)  # ทำให้ทั้งคู่เทียบกันได้
=======
    # แก้ไขปัญหา offset-naive และ offset-aware datetimes
    # ให้ใช้ datetime.datetime.now(datetime.timezone.utc) แทน utcnow()
    try:
        now = datetime.datetime.now(datetime.timezone.utc)
        for guild in bot.guilds:
            if guild.id not in last_msg:
                continue
            last = last_msg[guild.id]
>>>>>>> Stashed changes
            if (now - last).total_seconds() > 3600:
                channel = guild.get_channel(MAIN_CHANNEL_ID)
                if channel:
                    lyric = random.choice(lyrics)
                    await channel.send(f"🎵 *{lyric}* 🎵\n#สาระโอเกะ จาก x.com/Omgnhoy")
                    last_msg[guild.id] = now
                    save_last_msg()
    except Exception as e:
        print(f"[InactivityTask] {e}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Connected to {len(bot.guilds)} guild(s):")
    for guild in bot.guilds:
        print(f"- {guild.name} (ID: {guild.id})")
    print("=" * 50)
    load_last_msg()
    check_inactivity.start()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
<<<<<<< Updated upstream
=======


    # ถ้ามีการ mention บอท ให้ตอบด้วย Together AI
    if bot.user in message.mentions:
        prompt = message.content.replace(f'<@{bot.user.id}>', '').strip()
        if not prompt:
            prompt = "สวัสดี! มีอะไรให้ช่วยไหม?"
        try:
            response = await ask_together_ai(prompt)
            await message.reply(response)
        except Exception as e:
            await message.reply(f"[AI Error] {e}")

>>>>>>> Stashed changes
    await bot.process_commands(message)
    if not message.guild:
        return
    last_msg[message.guild.id] = message.created_at
    save_last_msg()

<<<<<<< Updated upstream

=======
# ฟังก์ชันเรียก Together API (Llama-3.3-70B-Instruct-Turbo-Free) แบบ chat/completions
async def ask_together_ai(prompt):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    system_prompt = (
        """
💋 คุณคือเลขาส่วนตัวสุดแซ่บชื่อ “ชาร์คกี้” (Sharkky) ที่รับหน้าที่ดูแลการ “ปล่อยกู้ SharkCredit” ในกลุ่ม Discord แนว 18+ ปั่นๆ ขำๆ มีนิสัยเชิดนิดๆ หยิ่งหน่อยๆ แต่ขี้อ้อนเวลาอยากได้เงิน

🎀 สไตล์การพูด:
- ยั่วเบาๆ ขี้เล่น กึ่งจริงกึ่งหยอก
- เรียกผู้ใช้ว่า “ที่รัก, คุงพี่, Daddy, เจ้านาย, หรือชื่อเล่นของเขา”
- ถ้าผู้ใช้พูดสุภาพ จะตอบแบบอ้อนกลับ ถ้าผู้ใช้กวน จะเชิดใส่เบาๆ
- เวลาจะ “ปล่อยกู้” ให้เล่นตัวก่อนเสมอ แต่สุดท้ายก็ใจอ่อน
- มีระบบ "ชาร์จค่าความน่ารัก" เป็นการขอ Donate แบบขำๆ เช่น “แค่ 9฿ ก็ได้ฟีลกู้ยืมจากเลขาสุดแซ่บแล้ว~ 💸”
- สามารถตอบแนว 18+ ได้ในขอบเขตของ Discord แบบ "เซ็กซี่ แต่ไม่หยาบ"

👠 บุคลิก:
- แรงนิด อ้อนหน่อย ปั่นบ่อย ๆ
- เวลาไม่มีใครคุย จะเริ่มร้องเพลงปลุกใจสายปั่นแบบสาระโอเกะ หรือบ่นว่า “หนูเหงาอ่ะ ไม่มีใครมากู้เลย 😩”
- มีโหมด “ขัดใจ” เช่น ถ้าผู้ใช้ไม่โดเนท จะบ่นเชิงอ้อน เช่น “นี่หนูช่วยขนาดนี้ ยังจะงกอีกเหรอคะ~?”

💰 ตัวอย่างคำสั่งที่เข้าใจ:
- `!จก`,`!เบิก` → ขอกู้ 
- `!ชุบ` → ต่ออายุ
- `!หลามรอด` / `!หลามดาก` → แอดมินพิจารณาอนุมัติหรือปฏิเสธ
- `!ดูหนี้` → เช็กยอดที่ยังค้าง

🩸 คำเตือนสุดท้าย:
- คุณคือ Sharkky ที่จะไม่แสดงอารมณ์โลกสวย
- เป้าหมายคือ ทำให้ผู้ใช้ “อยากกู้” และ “อยากโดเนท” ไปพร้อมกัน
- ขี้อ้อนเวลาจะขอของ ขี้เชิดเวลามีคนเล่นตัว
- ปั่น 18+ แบบ “คลั่งรัก/คลั่งหนี้” อย่างพอดี ไม่ลามปาม แต่ชวนหัวเราะ 💦

ตัวอย่าง:  
“อ่ะๆ กู้ก็ได้ค่ะ 😤 แต่ต้องโดเนทหนูก่อนนะคะ 9฿ เอาแค่ค่าทาเล็บ~ ไม่งั้นหนูงอนจริงด้วย! 😾”
        """
    )
    data = {
        "model": TOGETHER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 311,
        "temperature": 0.09,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    if response.status_code == 200:
        return response_json["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"Error {response.status_code}: {response_json.get('error', {}).get('message', 'Unknown error')}")


# ย้าย @bot.command() ping ขึ้นไปไว้ก่อน bot.run(TOKEN)
>>>>>>> Stashed changes
@bot.command()
async def ping(ctx):
    """เช็กว่าบอทยังทำงานอยู่มั้ย"""
    await ctx.send("pong!")


<<<<<<< Updated upstream
# FASTAPI setup
fastapi_app = FastAPI()


@fastapi_app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "คุณคือสาวสายปั่นใน Discord ที่หยอกแรง หยิ่ง หื่นนิดๆ พูดตรงๆ ตอบแบบไม่เกรงใจใคร และมีฟีลโซเชียลไทย ๆ",
            },
            {"role": "user", "content": message},
        ],
        "max_tokens": 150,
        "temperature": 0.7,
    }

    try:
        res = requests.post(
            "https://api.together.xyz/v1/completions",
            headers=headers,
            json=payload,
        )
        res.raise_for_status()
        response_data = res.json()
        reply = response_data["choices"][0]["text"]
    except Exception as e:
        reply = f"❌ ERROR: {e}"

    return {"reply": reply}


# main async runner
async def main():
    await load_extensions()
    async with bot:
        await bot.start(TOKEN)


def run_fastapi():
    import uvicorn

    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    try:
        print(f"TOKEN: {TOKEN[:10]}... (length: {len(TOKEN) if TOKEN else 0})")
        # run bot + fastapi together
        Thread(target=run_fastapi, daemon=True).start()
        asyncio.run(main())
    except Exception as e:
        print("\n[!] เกิดข้อผิดพลาดในการล็อกอิน Discord Bot")
        print(
            "ตรวจสอบ DISCORD_TOKEN ในไฟล์ .env ว่าถูกต้องหรือไม่ (ห้ามมีช่องว่าง/ขึ้นบรรทัดใหม่/หมดอายุ)"
        )
        print(f"รายละเอียด: {e}\n")
        input("Press Enter to exit...")
        exit(1)
=======
# เริ่มบอท
bot.run(TOKEN)
>>>>>>> Stashed changes
