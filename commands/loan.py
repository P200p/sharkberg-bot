# commands/loan.py
<<<<<<< Updated upstream

from discord.ext import commands
from db import create_loan, approve_loan, record_transaction
from collections import defaultdict
from datetime import datetime, timedelta

borrow_log = defaultdict(list)
ADMIN_ID = "767982567604879371"

def is_borrow_spammer(user_id):
    now = datetime.now(datetime.timezone.utc)
    borrow_log[user_id] = [
        t for t in borrow_log[user_id] if now - t < timedelta(minutes=30)
    ]
    borrow_log[user_id].append(now)
    return len(borrow_log[user_id]) > 3
=======
import discord
from discord.ext import commands
from db import create_loan, approve_loan, record_transaction
>>>>>>> Stashed changes


class LoanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="เบิก")
    async def request_loan(self, ctx, amount: int):
        import random

        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
<<<<<<< Updated upstream

        if is_borrow_spammer(user_id):
            await ctx.send("ที่บ้านคุณพี่ชายไม่ทำมาหาแดกหรอค่ะ 😘 เบิกถี่จัง")
            return
        loan_id = create_loan(user_id, guild_id, amount)
        loan_responses = [
            f"ขอวงเงิน {amount} เครดิต รอแอดมินรอดก่อนนะจ๊ะ! (loan_id: {loan_id})",
=======
        loan_id = create_loan(user_id, guild_id, amount)
        loan_responses = [
            f"ขอวงเงิน {amount} SharkCredit รอแอดมินหลามรอดก่อนนะจ๊ะ! (loan_id: {loan_id})",
>>>>>>> Stashed changes
            f"ขอกู้รอบนี้ ขอหลักฐานการปั่นเมื่อวานด้วยจ้า! (วง {amount})",
            f"จะยืมอีกแล้วเหรอ? เมื่อไหร่จะแตกซักที~ (ขอ {amount})",
            f"วงหมดก็ต้องปั่นให้แตกก่อนนะจ๊ะ! (ขอ {amount})",
            f"อยากเบิกใช่มั้ย? แอดมินใจดีรออนุมัติอยู่~ (ขอ {amount})",
            f"ขอเครดิตเพิ่ม? ขอใจแอดมินก่อนมั้ยล่ะ! (ขอ {amount})",
        ]
        await ctx.send(random.choice(loan_responses))
        record_transaction(user_id, guild_id, loan_id, "request_loan", amount, 0)

<<<<<<< Updated upstream
        # แจ้งไป DM แอดมินเท่านั้น
        admin = await self.bot.fetch_user(int(ADMIN_ID))
        if admin:
            await admin.send(
                f"💰 มีคนขอกู้เครดิต {amount} (loan_id: {loan_id})\nจาก: {ctx.author.display_name} ({user_id})"
            )

=======
>>>>>>> Stashed changes
    @commands.command(name="หลามรอด")
    @commands.has_permissions(administrator=True)
    async def approve_loan_cmd(self, ctx, loan_id: str):
        admin_id = str(ctx.author.id)
        approve_loan(loan_id, admin_id)
<<<<<<< Updated upstream
        await ctx.send(f"วงเงินเครดิต อนุมัติแล้วจ้า! (loan_id: {loan_id})")
        await ctx.send("แม่ดีใจแทบแตก~ ถ้าว่างสแกน QR โดเนทให้แม่นะคะ ❤️‍🔥 (อยู่ที่ปกทวิตพี่หลาม) 🙏")
        record_transaction(
            admin_id, ctx.guild.id, loan_id, "approve_loan", 0, amount
        )
=======
        await ctx.send(f"วงเงิน SharkCredit อนุมัติแล้วจ้า! (loan_id: {loan_id})")

    @commands.command(name="ประวัติ")
    async def history(self, ctx):
        await ctx.send("(ฟีเจอร์นี้รอเชื่อมต่อฐานข้อมูล)")

>>>>>>> Stashed changes

async def setup(bot):
    await bot.add_cog(LoanCog(bot))
