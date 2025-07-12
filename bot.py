"""
Main Discord bot for sharkberg-bot.

This module handles the core bot functionality including:
- Loading commands from the commands/ directory
- Managing message activity tracking
- Running background tasks
- Starting the FastAPI server
"""

import asyncio
import json
import logging
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

import discord
from discord.ext import commands, tasks
from fastapi import FastAPI
import aiohttp
from threading import Thread

from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Type aliases
GuildID = int
LastMessageTimes = Dict[GuildID, datetime]

# Global state
last_msg: LastMessageTimes = {}

# Song lyrics for inactivity messages
LYRICS = [
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


def save_last_msg() -> None:
    """Save the last message times to a JSON file."""
    try:
        with open(config.LAST_MSG_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {str(k): v.isoformat() for k, v in last_msg.items()},
                f,
                ensure_ascii=False,
                indent=2,
            )
    except (IOError, TypeError) as e:
        logger.error(f"Failed to save last message times: {e}")


def load_last_msg() -> None:
    """Load the last message times from a JSON file."""
    global last_msg
    try:
        with open(config.LAST_MSG_FILE, "r", encoding="utf-8") as f:
            last_msg = {
                int(k): datetime.fromisoformat(v)
                for k, v in json.load(f).items()
            }
        logger.info("Successfully loaded last message times")
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning("Could not load last message data. Starting fresh.")
        last_msg = {}
    except Exception as e:
        logger.error(f"Unexpected error loading last message times: {e}")
        last_msg = {}


async def load_extensions() -> None:
    """Load all extension modules from the commands directory."""
    for cmd_file in Path("commands").glob("*.py"):
        if cmd_file.stem == "__init__":
            continue
        
        ext_name = f"commands.{cmd_file.stem}"
        try:
            await bot.load_extension(ext_name)
            logger.info(f"✅ Loaded extension: {ext_name}")
        except Exception as e:
            logger.error(f"❌ Failed to load extension {ext_name}: {e}", exc_info=True)


@tasks.loop(minutes=5)
async def check_inactivity() -> None:
    """Post song lyrics if there's been no activity for over an hour."""
    if not hasattr(bot, "user"):
        return
    
    try:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        for guild in bot.guilds:
            if guild.id not in last_msg:
                continue
                
            last_message_time = last_msg[guild.id].replace(tzinfo=None)
            if (now - last_message_time).total_seconds() > 3600:  # 1 hour
                channel = guild.get_channel(config.MAIN_CHANNEL_ID)
                if channel:
                    lyric = random.choice(LYRICS)
                    try:
                        await channel.send(
                            f"🎵 *{lyric}* 🎵\n#สาระโอเกะ จาก x.com/Omgnhoy"
                        )
                        last_msg[guild.id] = now
                        save_last_msg()
                    except discord.HTTPException as e:
                        logger.error(f"Failed to send inactivity message: {e}")
    except Exception as e:
        logger.error(f"Error in check_inactivity: {e}", exc_info=True)


@bot.event
async def on_ready() -> None:
    """Handle bot startup."""
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    logger.info(f"Connected to {len(bot.guilds)} guild(s):")
    
    for guild in bot.guilds:
        logger.info(f"- {guild.name} (ID: {guild.id})")
    
    logger.info("=" * 50)
    load_last_msg()

    # Sync all application (slash) commands
    try:
        await bot.tree.sync()
        logger.info("Slash commands synced with Discord.")
    except Exception as e:
        logger.error(f"Failed to sync slash commands: {e}")
    
    if not check_inactivity.is_running():
        check_inactivity.start()


@bot.event
async def on_message(message: discord.Message) -> None:
    """Handle incoming messages."""
    if message.author == bot.user:
        return
    try:
        await bot.process_commands(message)
        if message.guild:
            last_msg[message.guild.id] = message.created_at
            save_last_msg()
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)


@bot.command(name="ping")
async def ping_command(ctx: commands.Context) -> None:
    """Check if the bot is responsive (works in both DM and server)."""
    try:
        latency = round(bot.latency * 1000)  # Convert to ms
        await ctx.send(f"🏓 Pong! Latency: {latency}ms")
    except Exception as e:
        logger.error(f"Error in ping command: {e}")
        await ctx.send("❌ An error occurred while processing your request.")


@bot.command(name="ai")
async def ai_command(ctx: commands.Context, *, message: str):
    """เรียก AI ผ่าน API และตอบกลับใน Discord (works in both DM และ DM)."""
    async with ctx.typing():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:8000/chat",
                    json={"message": message},
                    timeout=20
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        reply = data.get("reply", "❌ ไม่สามารถติดต่อ AI ได้")
                    else:
                        reply = f"❌ API Error: {resp.status}"
            await ctx.send(reply)
        except Exception as e:
            logger.error(f"Error in !ai command: {e}")
            await ctx.send(f"❌ เกิดข้อผิดพลาด: {e}")

@ai_command.error
async def ai_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("โปรดระบุข้อความ เช่น `!ai สวัสดี` หรือ `!ai hello`")
    else:
        await ctx.send(f"เกิดข้อผิดพลาด: {error}")


def create_fastapi_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    from api.routes import app as api_router
    return api_router


async def main() -> None:
    """Main entry point for the bot."""
    try:
        await load_extensions()
        async with bot:
            await bot.start(config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot shutting down...")
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
    finally:
        if not bot.is_closed():
            await bot.close()


def run_fastapi() -> None:
    """Run the FastAPI server."""
    import uvicorn
    from api.routes import app as fastapi_app
    
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    try:
        print(f"Starting bot with token: {config.DISCORD_TOKEN[:10]}...")
        print(f"Token length: {len(config.DISCORD_TOKEN)}")
        
        # Run bot + FastAPI together
        import threading
        from threading import Thread
        
        # Start FastAPI in a separate thread
        fastapi_thread = Thread(target=run_fastapi, daemon=True)
        fastapi_thread.start()
        
        # Start the Discord bot
        asyncio.run(main())
    except Exception as e:
        logger.critical("Bot encountered a fatal error", exc_info=True)
        print("\n[!] เกิดข้อผิดพลาดในการล็อกอิน Discord Bot")
        print("ตรวจสอบ DISCORD_TOKEN ในไฟล์ .env ว่าถูกต้องหรือไม่ (ห้ามมีช่องว่าง/ขึ้นบรรทัดใหม่/หมดอายุ)")
        print(f"รายละเอียด: {e}")
        input("\nกด Enter เพื่อปิดโปรแกรม...")
        exit(1)
