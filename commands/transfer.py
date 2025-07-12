import discord
from discord.ext import commands
from discord import app_commands, Interaction, ui
from db import record_transaction
from config import config

ADMIN_USER_IDS = config.ADMIN_USER_IDS


class ApproveTransferView(ui.View):
    def __init__(self, sender_id, receiver_id, amount):
        super().__init__(timeout=180)
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.value = None

    @ui.button(label="✅ อนุมัติ", style=discord.ButtonStyle.green, custom_id="approve_transfer")
    async def approve(self, interaction: Interaction, button: ui.Button):
        if interaction.user.id not in ADMIN_USER_IDS:
            await interaction.response.send_message("คุณไม่มีสิทธิ์อนุมัติ", ephemeral=True)
            return
        record_transaction(
            self.sender_id, str(interaction.guild_id), None, "approve_transfer",
            self.amount, 0, admin_id=str(interaction.user.id)
        )
        await interaction.response.send_message(
            f"✅ อนุมัติการโอน {self.amount} SharkCredit สำเร็จ!",
            ephemeral=False
        )
        self.value = True
        self.stop()

    @ui.button(label="❌ ปฏิเสธ", style=discord.ButtonStyle.red, custom_id="reject_transfer")
    async def reject(self, interaction: Interaction, button: ui.Button):
        if interaction.user.id not in ADMIN_USER_IDS:
            await interaction.response.send_message("คุณไม่มีสิทธิ์ปฏิเสธ", ephemeral=True)
            return
        await interaction.response.send_message(
            f"❌ ปฏิเสธการโอน {self.amount} SharkCredit",
            ephemeral=False
        )
        self.value = False
        self.stop()


class TransferCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="transfer",
        description="โอน SharkCredit ให้ผู้ใช้ (ต้อง admin อนุมัติ)"
    )
    async def transfer(self, interaction: Interaction, user: discord.Member, amount: int):
        sender_id = str(interaction.user.id)
        receiver_id = str(user.id)
        guild_id = str(interaction.guild_id)
        record_transaction(sender_id, guild_id, None, "request_transfer", amount, 0)
        view = ApproveTransferView(sender_id, receiver_id, amount)
        await interaction.response.send_message(
            f"ขอโอน {amount} SharkCredit ให้ {user.mention} (รอแอดมินอนุมัติ)",
            view=view
        )


async def setup(bot):
    await bot.add_cog(TransferCog(bot))
