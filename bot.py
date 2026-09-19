import discord
from discord.ext import commands
from config import TOKEN


intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Ban ve Kick işlemleri için üye listesi izni gereklidir!
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Admin botu giriş yaptı : {bot.user}")


@bot.event
async def on_message(message):
    # Botun kendi mesajlarını denetlemesini engelle:
    if message.author == bot.user:
        return
    # Mesaj içinde link (http:// veya https://) var mı denetle:
    icerik = message.content.lower()
    if "http://" in icerik or "https://" in icerik or "discord.gg/" in icerik:
        # Yetkili olmayan bir üye link attıysa mesajı sil ve uyar:
        if not message.author.guild_permissions.administrator:
            await message.delete()
            await message.channel.send(
                f"⚠️ {message.author.mention}, sunucuda izinsiz link veya reklam paylaşmak yasaktır!",
                delete_after=5
            )
            return
    # 🚨 ÇOK ÖNEMLİ: on_message ezildiğinde diğer komutların çalışması için:
    await bot.process_commands(message)

@bot .command(name="ban",help ="belirtilen uyeyi kalic1 olarak yasaklar ")

@commands. has_permissions(ban_members=True) 

@bot.command(name="ban",help ="belirtilen üyeyi kalıcı olarak yasaklar ")
async def ban(ctx, uye:discord.Member, *,sebep="Kural ihlali"):
    
    try:
        await uye.ban(reason=sebep)
        await ctx.send(f"{uye.mention} sunucudan yasaklandı  sebep: {sebep}")
    except discord.Forbidden:
        await ctx.send("❌ Bu kullanıcıyı yasaklayamıyorum. Gerekli izinlere sahip değilim.")




bot. run(TOKEN)

