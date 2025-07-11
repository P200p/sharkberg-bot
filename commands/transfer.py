# commands/transfer.py
import discord
from discord.ext import commands
from db import record_transaction

class TransferCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="โอน")
    async def transfer(self, ctx, user: discord.Member, amount: int):
        sender_id = str(ctx.author.id)
        receiver_id = str(user.id)
        guild_id = str(ctx.guild.id)
        # บันทึกธุรกรรมแบบ pending
        record_transaction(sender_id, guild_id, None, "request_transfer", amount, 0)
        await ctx.send(f"ขอโอน {amount} SharkCredit ให้ {user.mention} (รอแอดมินอนุมัติ)")
        # ในระบบจริงควรสร้างปุ่ม Approve/Reject

    @commands.command(name="approve_transfer")
    @commands.has_permissions(administrator=True)
    async def approve_transfer(self, ctx, sender_id: str, receiver_id: str, amount: int):
        guild_id = str(ctx.guild.id)
        # อัปเดตธุรกรรมเป็นสำเร็จ
        record_transaction(sender_id, guild_id, None, "approve_transfer", amount, 0, admin_id=str(ctx.author.id))
        await ctx.send(f"แอดมินอนุมัติการโอน {amount} SharkCredit แล้ว!")

async def setup(bot):
    await bot.add_cog(TransferCog(bot))
