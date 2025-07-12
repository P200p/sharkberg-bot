import discord
from discord.ext import commands
from db import get_user, set_display_name

class ProfileCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ตั้งชื่อผู้ใช้")
    async def set_display_name(self, ctx: commands.Context, *, name: str):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        set_display_name(user_id, guild_id, name)
        await ctx.send(f"ชื่อผู้ใช้ set to {name}")

    @commands.command(name="ตั้งชื่อฉลาม")
    async def set_shark_name(self, ctx: commands.Context, *, name: str):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        set_display_name(user_id, guild_id, name)
        await ctx.send(f"ชื่อฉลาม set to {name}")

    @commands.command(name="สถานะ")
    async def status(self, ctx: commands.Context):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        user_data = get_user(user_id, guild_id)
        await ctx.send(f"Your status is: {user_data['status']}")

    @commands.command(name="ชีวิตประวัติ")
    async def bio(self, ctx: commands.Context, *, bio: str):
        await ctx.send("Bio placeholder")

    @commands.command(name="โปรไฟล์")
    async def profile(self, ctx: commands.Context):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        user_data = get_user(user_id, guild_id)
        await ctx.send(f"Your profile link is: {user_data['profile_link']}")

async def setup(bot: commands.Bot):
    await bot.add_cog(ProfileCog(bot))
