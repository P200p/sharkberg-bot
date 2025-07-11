# commands/admin.py
import discord
from discord.ext import commands
from db import record_transaction


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="boost")
    @commands.has_permissions(administrator=True)
    async def boost(self, ctx, user: discord.Member, amount: int):
        record_transaction(
            str(user.id),
            str(ctx.guild.id),
            None,
            "boost",
            amount,
            0,
            admin_id=str(ctx.author.id),
        )
        await ctx.send(f"เพิ่มเครดิต {amount} ให้ {user.mention}")

    @commands.command(name="ban")
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, user: discord.Member):
        await ctx.send(f"ระงับบัญชีของ {user.mention} (ฟีเจอร์นี้รอเชื่อมต่อฐานข้อมูล)")

    @commands.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx, user: discord.Member):
        await ctx.send(f"รีเซ็ตสถานะบัญชี {user.mention} (ฟีเจอร์นี้รอเชื่อมต่อฐานข้อมูล)")

    @commands.command(name="forcepay")
    @commands.has_permissions(administrator=True)
    async def forcepay(self, ctx, user: discord.Member):
        await ctx.send(
            f"ตัดเครดิตหรือยึด SharkCredit ของ {user.mention} (ฟีเจอร์นี้รอเชื่อมต่อฐานข้อมูล)"
        )

    @commands.command(name="ล้างหนี้")
    @commands.has_permissions(administrator=True)
    async def clear_loans(self, ctx, user: discord.Member):
        await ctx.send(f"ลบหนี้ทั้งหมดของ {user.mention} (ฟีเจอร์นี้รอเชื่อมต่อฐานข้อมูล)")


async def setup(bot):
    await bot.add_cog(AdminCog(bot))
    print("AdminCog loaded")
