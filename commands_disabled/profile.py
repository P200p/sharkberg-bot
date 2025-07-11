# commands/profile.py
<<<<<<< Updated upstream
from discord.ext import commands
from db import get_user, set_display_name


class ProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # เก็บ instance ของบอทไว้ใช้งานในคำสั่งต่าง ๆ

    @commands.command(name="ชื่อผู้ใช้")
    async def set_user_name(self, ctx, *, name: str):
        # ดึง ID ของผู้ใช้และเซิร์ฟเวอร์จาก context
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        # บันทึกชื่อผู้ใช้ใหม่ในฐานข้อมูล
        set_display_name(user_id, guild_id, name)
        # ส่งข้อความยืนยันกลับไปยังแชท
        await ctx.send(f"เปลี่ยนชื่อของคุณเป็น {name} เรียบร้อยแล้ว!")

    @commands.command(name="status")
    async def status(self, ctx):
        # ดึง ID ของผู้ใช้และเซิร์ฟเวอร์จาก context
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        # ดึงข้อมูลผู้ใช้จากฐานข้อมูล
        user = get_user(user_id, guild_id)
        # แสดงสถานะของผู้ใช้ในข้อความ
        await ctx.send(f"สถานะผู้ใช้: {user}")

    @commands.command(name="bio")
    async def set_bio(self, ctx, *, bio: str):
        # ฟีเจอร์นี้ยังไม่ได้เชื่อมต่อฐานข้อมูล
=======
import discord
from discord.ext import commands
from db import get_user, set_display_name

class ProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ชื่อฉลาม")
    async def set_shark_name(self, ctx, *, name: str):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        set_display_name(user_id, guild_id, name)
        await ctx.send(f"เปลี่ยนชื่อฉลามของคุณเป็น {name} เรียบร้อย!")

    @commands.command(name="status")
    async def status(self, ctx):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        user = get_user(user_id, guild_id)
        await ctx.send(f"สถานะ SharkUser: {user}")

    @commands.command(name="bio")
    async def set_bio(self, ctx, *, bio: str):
>>>>>>> Stashed changes
        await ctx.send("(ฟีเจอร์นี้รอเชื่อมต่อฐานข้อมูล)")

    @commands.command(name="โปรไฟล์")
    async def profile_link(self, ctx):
<<<<<<< Updated upstream
        # ส่งลิงก์โปรไฟล์ของผู้ใช้ โดยใช้ user_id ใน URL
        await ctx.send(f"ลิงก์โปรไฟล์ของคุณ: https://sharkcial.example.com/{ctx.author.id}")


async def setup(bot):
    # ลงทะเบียน cog กับตัวบอท
=======
        await ctx.send(f"ลิงก์โปรไฟล์: https://sharkcial.example.com/{ctx.author.id}")

async def setup(bot):
>>>>>>> Stashed changes
    await bot.add_cog(ProfileCog(bot))
