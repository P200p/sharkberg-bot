# commands/fun.py
import discord
from discord.ext import commands
import random

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="สาระโอเกะ")
    async def random_lyric(self, ctx):
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
            "ถ้าตอบไม่ได้ เดี๋ยวไปขอสูตรจาก x.com/Omgnhoy ให้!"
        ]
        await ctx.send(random.choice(lyrics))

    @commands.command(name="สุ่ม")
    async def random_user(self, ctx):
        members = [m for m in ctx.guild.members if not m.bot]
        user = random.choice(members)
        await ctx.send(f"วันนี้ขอแกล้ง {user.mention}!")

    @commands.command(name="เตือน")
    async def warn(self, ctx):
        warns = [
            "อย่าลืมกดสปิน!",
            "ใครยังไม่กู้ รีบเลย!",
            "สล็อตไม่หมุนเองนะเว้ย!"
        ]
        await ctx.send(random.choice(warns))

    @commands.command(name="บ่น")
    async def rant(self, ctx):
        rants = [
            "บอทก็เหนื่อยเป็นนะ!",
            "แอดมินก็อยากปั่นเหมือนกัน!",
            "ใครจะช่วยบอทบ้าง!",
            "ถามมาได้ทุกเรื่อง ยกเว้นเลขหวย!",
            "คำถามยากๆ แบบนี้ ให้ไปถาม x.com/Omgnhoy ดีกว่า!",
            "บอทสายปั่นขอพักสมอง 0.5 วิ...",
            "ถ้าตอบไม่ได้ เดี๋ยวไปขอสูตรจากทวิตเตอร์!",
            "บอทขอคิดก่อน เดี๋ยวตอบแบบฮาๆ ให้!",
            "ถ้าปั่นไม่แตก ให้ลองถาม Omgnhoy ดู!"
        ]
        await ctx.send(random.choice(rants))

async def setup(bot):
    await bot.add_cog(FunCog(bot))
