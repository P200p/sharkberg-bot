# commands/loan.py

from discord.ext import commands
from discord import app_commands, Interaction
from config import config
from db import create_loan, approve_loan, record_transaction
from collections import defaultdict
from datetime import datetime, timedelta
import discord
from discord import ui
import random

borrow_log = defaultdict(list)
ADMIN_USER_IDS = config.ADMIN_USER_IDS

def admin_only():
    def predicate(interaction: Interaction) -> bool:
        return interaction.user.id in config.ADMIN_USER_IDS
    return app_commands.check(predicate)

def is_borrow_spammer(user_id):
    now = datetime.now(datetime.timezone.utc)
    borrow_log[user_id] = [
        t for t in borrow_log[user_id] if now - t < timedelta(minutes=30)
    ]
    borrow_log[user_id].append(now)
    return len(borrow_log[user_id]) > 3

class LoanRequestModal(ui.Modal):
    def __init__(self) -> None:
        super().__init__(title="ขอกู้เครดิต")
        self.add_item(ui.TextInput(label="จำนวนเงิน", placeholder="จำนวนเงินที่ต้องการขอกู้", style=discord.TextInputStyle.short, required=True))

    async def callback(self, interaction: discord.Interaction):
        amount = int(self.children[0].value)
        user_id = str(interaction.user.id)
        guild_id = str(interaction.guild_id)

        if is_borrow_spammer(user_id):
            await interaction.response.send_message("ที่บ้านคุณพี่ชายไม่ทำมาหาแดกหรอค่ะ 😘 เบิกถี่จัง", ephemeral=True)
            return

        loan_id = create_loan(user_id, guild_id, amount)
        embed = discord.Embed(title="รายละเอียดการขอกู้", description=f"เงินต้น: {amount} เครดิต", color=0x00ff00)
        embed.add_field(name="ดอกเบี้ย", value="10%", inline=False)
        embed.add_field(name="ยอดรวม", value=f"{amount * 1.1} เครดิต", inline=False)
        view = LoanConfirmView(loan_id, amount)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

        # แจ้งไป DM แอดมินเท่านั้น
        # แจ้ง DM แอดมินทุกคนใน whitelist
        for admin_id in ADMIN_USER_IDS:
            try:
                admin = await interaction.client.fetch_user(int(admin_id))
                if admin:
                    await admin.send(
                        f"💰 มีคนขอกู้เครดิต {amount} (loan_id: {loan_id})\nจาก: {interaction.user.display_name} ({user_id})"
                    )
            except Exception as e:
                print(f"[WARN] แจ้งแอดมิน {admin_id} ไม่สำเร็จ: {e}")

        # Auto reject ใน 10 นาที
        await interaction.client.loop.create_task(view.auto_reject(loan_id, interaction.client))

class LoanConfirmView(ui.View):
    def __init__(self, loan_id, amount):
        super().__init__()
        self.loan_id = loan_id
        self.amount = amount

    @ui.button(label="ยืนยัน", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("ยืนยันการขอกู้แล้ว", ephemeral=True)
        # อนุมัติ loan_id นี้
        approve_loan(self.loan_id, None)
        record_transaction(
            str(interaction.user.id), str(interaction.guild_id), self.loan_id, "approve_loan", 0, self.amount
        )

    @ui.button(label="ยกเลิก", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("ยกเลิกการขอกู้แล้ว", ephemeral=True)
        # ยกเลิก loan_id นี้
        create_loan(str(interaction.user.id), str(interaction.guild_id), self.amount, status="cancelled")

    async def auto_reject(self, loan_id, client):
        await discord.utils.sleep(600)  # 10 นาที
        # ตรวจสอบว่า loan_id นี้ยังไม่ได้รับการอนุมัติ
        if not approve_loan(loan_id, None):
            reject_responses = [
                f"วงเงินเครดิต {loan_id} ถูกปฏิเสธอัตโนมัติ",
                f"ขอโทษครับ/ค่ะ วงเงินเครดิต {loan_id} ไม่ได้รับการอนุมัติ",
                f"วงเงินเครดิต {loan_id} ถูกปฏิเสธเนื่องจากไม่มีการตอบกลับ",
            ]
            await client.get_channel(CHANNEL_ID).send(random.choice(reject_responses))

class LoanRequestView(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(
            ui.Button(label="ขอกู้เครดิต", emoji="💸", custom_id="loan_request")
        )

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.guild is None:
            await interaction.response.send_message(
                "คุณไม่สามารถใช้ฟังก์ชันนี้ใน DM ได้", ephemeral=True
            )
            return False
        return True

    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.data.custom_id == "loan_request":
            modal = LoanRequestModal()
            await interaction.response.send_modal(modal)


class QuickLoanView(ui.View):
    def __init__(self, amount, admin, bot):
        super().__init__(timeout=300)  # 5 นาที
        self.amount = amount
        self.claimed = False
        self.admin = admin
        self.bot = bot

    @ui.button(label="ขอกู้เงิน", style=discord.ButtonStyle.green, custom_id="quick_loan_claim")
    async def claim_loan(self, interaction: discord.Interaction, button: ui.Button):
        if self.claimed:
            await interaction.response.send_message("สิทธิ์นี้ถูกใช้ไปแล้ว!", ephemeral=True)
            return
        self.claimed = True
        button.disabled = True
        user_id = str(interaction.user.id)
        guild_id = str(interaction.guild_id)
        loan_id = create_loan(user_id, guild_id, self.amount)
        # แจ้งผู้กด
        await interaction.response.send_message(
            f"🎉 คุณได้รับสิทธิ์กู้ {self.amount} เครดิต (loan_id: {loan_id}) สำเร็จ!",
            ephemeral=True
        )
        # แจ้งแอดมิน
        if self.admin:
            await self.admin.send(
                f"✅ {interaction.user.display_name} ({user_id}) ได้รับสิทธิ์กู้ {self.amount} เครดิต (loan_id: {loan_id})"
            )
        # แจ้งในแชทหลัก
        channel = interaction.channel
        if channel:
            await channel.send(
                f"🎉 {interaction.user.mention} ได้รับสิทธิ์กู้ {self.amount} เครดิต (loan_id: {loan_id})"
            )
        self.stop()

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, ui.Button):
                item.disabled = True
        # แจ้งหมดเวลา (optional)

class LoanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="เบิก", description="ขอกู้เงิน SharkCredit")
    async def request_loan_slash(self, interaction: Interaction, amount: int):
        user_id = str(interaction.user.id)
        guild_id = str(interaction.guild_id)
        if is_borrow_spammer(user_id):
            await interaction.response.send_message("ที่บ้านคุณพี่ชายไม่ทำมาหาแดกหรอค่ะ 😘 เบิกถี่จัง", ephemeral=True)
            return
        loan_id = create_loan(user_id, guild_id, amount)
        loan_responses = [
            f"ขอวงเงิน {amount} เครดิต รอแอดมินรอดก่อนนะจ๊ะ! (loan_id: {loan_id})",
            f"ขอกู้รอบนี้ ขอหลักฐานการปั่นเมื่อวานด้วยจ้า! (วง {amount})",
            f"จะยืมอีกแล้วเหรอ? เมื่อไหร่จะแตกซักที~ (ขอ {amount})",
            f"วงหมดก็ต้องปั่นให้แตกก่อนนะจ๊ะ! (ขอ {amount})",
            f"อยากเบิกใช่มั้ย? แอดมินใจดีรออนุมัติอยู่~ (ขอ {amount})",
            f"ขอเครดิตเพิ่ม? ขอใจแอดมินก่อนมั้ยล่ะ! (ขอ {amount})",
        ]
        await interaction.response.send_message(random.choice(loan_responses), ephemeral=True)
        record_transaction(user_id, guild_id, loan_id, "request_loan", amount, 0)
        # แจ้งไป DM แอดมินเท่านั้น
        for admin_id in config.ADMIN_USER_IDS:
            admin = await self.bot.fetch_user(admin_id)
            if admin:
                await admin.send(
                    f"💰 มีคนขอกู้เครดิต {amount} (loan_id: {loan_id})\nจาก: {interaction.user.display_name} ({user_id})"
                )

    @app_commands.command(name="ประวัติ", description="ดูประวัติการกู้ SharkCredit")
    async def loan_history_slash(self, interaction: Interaction):
        user_id = str(interaction.user.id)
        guild_id = str(interaction.guild_id)
        from db import get_loan_history
        history = get_loan_history(user_id, guild_id)
        if not history:
            await interaction.response.send_message("ไม่พบประวัติการกู้ของคุณ", ephemeral=True)
        else:
            msg = "\n".join([
                f"loan_id: {h.get('id', '-')}, amount: {h.get('amount', '-')} เครดิต, status: {h.get('status', '-')}"
                for h in history
            ])
            await interaction.response.send_message(f"ประวัติการกู้ของคุณ:\n{msg}", ephemeral=True)

    @app_commands.command(name="ปล่อยกู้", description="ปล่อยกู้ด่วน (admin only)")
    @admin_only()
    async def quick_loan_slash(self, interaction: Interaction, amount: int):
        admin = interaction.user
        view = QuickLoanView(amount, admin, self.bot)
        embed = discord.Embed(
            title="ปล่อยกู้ด่วน!",
            description=f"แอดมินปล่อยกู้ {amount} เครดิต คนแรกที่กดจะได้สิทธิ์ทันที!",
            color=0x00ffcc
        )
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="approve_loan", description="อนุมัติวงเงิน (admin only)")
    @admin_only()
    async def approve_loan_slash(self, interaction: Interaction, loan_id: str):
        admin_id = str(interaction.user.id)
        approve_loan(loan_id, admin_id)
        await interaction.response.send_message(f"วงเงินเครดิต อนุมัติแล้วจ้า! (loan_id: {loan_id})", ephemeral=True)
        record_transaction(
            admin_id, interaction.guild_id, loan_id, "approve_loan", 0, 0
        )

    @app_commands.command(name="close_loan", description="ปิดหนี้ (admin only)")
    @admin_only()
    async def close_loan_slash(self, interaction: Interaction, loan_id: str, user: discord.Member, amount: int):
        admin_id = str(interaction.user.id)
        user_id = str(user.id)
        guild_id = str(interaction.guild_id)
        try:
            from db import sb_update_loan
            sb_update_loan(loan_id, status='paid', admin_id=admin_id)
        except ImportError:
            pass
        record_transaction(user_id, guild_id, loan_id, "pay", amount, int(amount * 0.1), admin_id=admin_id)
        await interaction.response.send_message(f"✅ ปิดหนี้ของ {user.mention} (loan_id: {loan_id}) สำเร็จแล้ว", ephemeral=True)


    @app_commands.command(name="ประวัติ", description="ดูประวัติการกู้ SharkCredit")
    async def loan_history_slash(self, interaction: Interaction):
        user_id = str(interaction.user.id)
        guild_id = str(interaction.guild_id)
        from db import get_loan_history
        history = get_loan_history(user_id, guild_id)
        if not history:
            await interaction.response.send_message("ไม่พบประวัติการกู้ของคุณ", ephemeral=True)
        else:
            msg = "\n".join([
                f"loan_id: {h.get('id', '-')}, amount: {h.get('amount', '-')} เครดิต, status: {h.get('status', '-')}"
                for h in history
            ])
            await interaction.response.send_message(f"ประวัติการกู้ของคุณ:\n{msg}", ephemeral=True)

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ปล่อยกู้")
    @commands.has_permissions(administrator=True)
    async def quick_loan(self, ctx, amount: int):
        admin = ctx.author
        view = QuickLoanView(amount, admin, self.bot)
        embed = discord.Embed(
            title="ปล่อยกู้ด่วน!",
            description=f"แอดมินปล่อยกู้ {amount} เครดิต คนแรกที่กดจะได้สิทธิ์ทันที!",
            color=0x00ffcc
        )
        await ctx.send(embed=embed, view=view)

    @app_commands.command(name="close_loan", description="ปิดหนี้ (admin only)")
    @admin_only()
    async def close_loan_slash(self, interaction: Interaction, loan_id: str, user: discord.Member, amount: int):
        admin_id = str(interaction.user.id)
        user_id = str(user.id)
        guild_id = str(interaction.guild_id)
        try:
            from db import sb_update_loan
            sb_update_loan(loan_id, status='paid', admin_id=admin_id)
        except ImportError:
            pass
        record_transaction(user_id, guild_id, loan_id, "pay", amount, int(amount * 0.1), admin_id=admin_id)
        await interaction.response.send_message(f"✅ ปิดหนี้ของ {user.mention} (loan_id: {loan_id}) สำเร็จแล้ว", ephemeral=True)


    @app_commands.command(name="loan", description="ขอกู้ SharkCredit (ต้อง admin อนุมัติ)")
    async def request_loan_slash(self, interaction: Interaction, amount: int):
        user_id = str(interaction.user.id)
        guild_id = str(interaction.guild_id)

        if is_borrow_spammer(user_id):
            await interaction.response.send_message("ที่บ้านคุณพี่ชายไม่ทำมาหาแดกหรอค่ะ 😘 เบิกถี่จัง", ephemeral=True)
            return
        loan_id = create_loan(user_id, guild_id, amount)
        record_transaction(user_id, guild_id, loan_id, "request_loan", amount, 0)
        embed = discord.Embed(title="ขอกู้ SharkCredit", description=f"จำนวน: {amount} เครดิต", color=0x00ff00)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        # แจ้ง DM แอดมินทุกคนใน whitelist
        for admin_id in ADMIN_USER_IDS:
            try:
                admin = await interaction.client.fetch_user(int(admin_id))
                if admin:
                    await admin.send(
                        f"💰 มีคนขอกู้เครดิต {amount} (loan_id: {loan_id})\nจาก: {interaction.user.display_name} ({user_id})"
                    )
            except Exception as e:
                print(f"[WARN] แจ้งแอดมิน {admin_id} ไม่สำเร็จ: {e}")

    @app_commands.command(name="approve_loan", description="อนุมัติวงเงิน (admin only)")
    @admin_only()
    async def approve_loan_slash(self, interaction: Interaction, loan_id: str):
        admin_id = str(interaction.user.id)
        approve_loan(loan_id, admin_id)
        await interaction.response.send_message(f"✅ อนุมัติวงเงิน SharkCredit สำเร็จ! (loan_id: {loan_id})", ephemeral=True)
        record_transaction(
            admin_id, interaction.guild_id, loan_id, "approve_loan", 0, 0
        )

    @commands.command(name="แจ้งเตือน")
    async def notify(self, ctx):
        # แจ้งเตือนค้างชำระทุก 2 ชม.
        await ctx.send("กำลังแจ้งเตือนค้างชำระ...")
        # ตรวจสอบค้างชำระและแจ้งเตือน

async def setup(bot):
    await bot.add_cog(LoanCog(bot))
