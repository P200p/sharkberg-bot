import os
import sys
import asyncio
import platform
import aiohttp
from dotenv import load_dotenv
import discord

# Print environment info
print("="*50)
print(f"Python: {platform.python_version()}")
print(f"discord.py: {discord.__version__}")
print("="*50)

async def verify_token(token):
    """Verify the Discord token by making a direct API call"""
    headers = {
        "Authorization": f"Bot {token}",
        "User-Agent": "DiscordBot (https://github.com/Rapptz/discord.py 2.5.2)"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                "https://discord.com/api/v10/users/@me",
                headers=headers
            ) as resp:
                if resp.status == 200:
                    print("✅ Token is valid!")
                    data = await resp.json()
                    print(f"🤖 Bot Username: {data['username']}#{data['discriminator']}")
                    print(f"🔑 Bot ID: {data['id']}")
                    return True
                else:
                    error = await resp.text()
                    print(f"❌ Token verification failed (Status: {resp.status}): {error}")
                    return False
        except Exception as e:
            print(f"❌ Error verifying token: {str(e)}")
            return False

print("="*50)
print("Starting Discord Bot...")
print("="*50)

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"Loading .env from: {env_path}")
load_dotenv(env_path)

# Get token and validate
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("[ERROR] DISCORD_TOKEN not found in .env file!")
    sys.exit(1)

# Clean token (remove quotes and whitespace)
TOKEN = TOKEN.strip('"\'').strip()
print(f"Token found: {TOKEN[:5]}...{TOKEN[-5:]}")
print(f"Token length: {len(TOKEN)} characters")

# Verify token format
if not (len(TOKEN) in [59, 70, 71, 72] and TOKEN.count('.') == 1):
    print("[WARNING] Token format doesn't match expected Discord bot token format!")

# Initialize bot with all intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

class MyClient(discord.Client):
    async def on_ready(self):
        print("\n" + "="*50)
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print(f'Connected to {len(self.guilds)} guild(s):')
        for guild in self.guilds:
            print(f'- {guild.name} (ID: {guild.id})')
        print("="*50 + "\n")

    async def on_error(self, event, *args, **kwargs):
        import traceback
        print(f'Error in {event}:')
        traceback.print_exc()

# Initialize client with error handling
client = MyClient(intents=intents)

if __name__ == "__main__":
    try:
        # First verify the token works with direct API call
        print("\n🔍 Verifying token with Discord API...")
        token_valid = asyncio.get_event_loop().run_until_complete(verify_token(TOKEN))
        
        if not token_valid:
            print("\n❌ Cannot connect with invalid token. Please check your token and try again.")
            print("Make sure to:")
            print("1. Copy the token correctly (no extra spaces or characters)")
            print("2. Use a token from the 'Bot' section, not the 'General Information' section")
            print("3. Make sure the token hasn't been reset or revoked")
            sys.exit(1)
            
        print("\n🚀 Attempting to connect to Discord...")
    except discord.LoginFailure:
        print("\n[ERROR] Failed to login. Possible reasons:")
        print("1. Invalid token (check for typos or extra spaces)")
        print("2. Token has been reset or revoked")
        print("3. Bot has been deleted from Developer Portal")
        print("\nPlease generate a new token and update your .env file")
    except Exception as e:
        print(f"\n[UNEXPECTED ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nBot has stopped.")
