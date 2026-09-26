import discord
from discord.ext import commands
from config import TOKEN
import random
import asyncio

# --- 1. POKÉMON SINIFI VE SAVAŞ MEKANİKLERİ ---
class Pokemon:
    def __init__(self, isim, can, guc, seviye):
        self.isim = isim
        self.seviye = seviye
        # Seviyeye göre varsayılan can ve güç artışı
        self.max_can = can + (seviye * 5)
        self.can = self.max_can
        self.guc = guc + (seviye * 2)

    def saldir(self, hedef):
        # %25 ihtimalle Kritik Vuruş (%150 hasar)
        kritik = random.random() < 0.25
        hasar = self.guc
        
        if kritik:
            hasar = int(hasar * 1.5)

        hedef.can -= hasar
        if hedef.can < 0:
            hedef.can = 0

        return hasar, kritik

    def hayatta_mi(self):
        return self.can > 0


# --- 2. BOT KURULUMU ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Ban ve Kick işlemleri için üye listesi izni

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Admin ve Oyun botu giriş yaptı : {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    icerik = message.content.lower()
    if "http://" in icerik or "https://" in icerik or "discord.gg/" in icerik:
        if not message.author.guild_permissions.administrator:
            await message.delete()
            await message.channel.send(
                f" {message.author.mention}, sunucuda izinsiz link veya reklam paylaşmak yasaktır!",
                delete_after=5
            )
            return

    await bot.process_commands(message)


# --- 3. POKÉMON SAVAŞ MOTORU (DISCORD KOMUTU) ---
@bot.command(name="savas", help="Pikachu ve Charizard arasında Pokémon savaşını başlatır.")
async def pokemon_savas(ctx):
    # Pokémon Nesnelerinin Oluşturulması
    pikachu = Pokemon(isim="Pikachu ", can=90, guc=18, seviye=5)
    charizard = Pokemon(isim="Charizard ", can=110, guc=15, seviye=5)

    await ctx.send(
        f" **POKÉMON SAVAŞI BAŞLIYOR!** \n"
        f"**{pikachu.isim}** (Can: {pikachu.can} | Seviye: {pikachu.seviye}) **VS** "
        f"**{charizard.isim}** (Can: {charizard.can} | Seviye: {charizard.seviye})\n"
        f"─────────────────────────────"
    )

    sira = 1
    # İki taraf da hayatta olduğu sürece savaş devam eder
    while pikachu.hayatta_mi() and charizard.hayatta_mi():
        if sira % 2 != 0:
            saldiran, hedef = pikachu, charizard
        else:
            saldiran, hedef = charizard, pikachu

        hasar, kritik = saldiran.saldir(hedef)

        mesaj = f" **{saldiran.isim}**, {hedef.isim}'e **{hasar}** hasar verdi!"
        if kritik:
            mesaj += "  **KRİTİK VURUŞ!**"
        
        mesaj += f"\n **{hedef.isim}** Kalan Can: `{hedef.can}/{hedef.max_can}`"

        await ctx.send(mesaj)
        await asyncio.sleep(2)  # Tur aralarında 2 saniye bekleme (heyecan katmak için)
        sira += 1

    kazanan = pikachu if pikachu.hayatta_mi() else charizard
    await ctx.send(f"\n **SAVAŞ BİTTİ!** Kazanan: **{kazanan.isim}** ")


# --- 4. YÖNETİCİ KOMUTLARI ---
@bot.command(name="ban", help="Belirtilen üyeyi kalıcı olarak yasaklar.")
@commands.has_permissions(ban_members=True)
async def ban(ctx, uye: discord.Member, *, sebep="Kural ihlali"):
    try:
        await uye.ban(reason=sebep)
        await ctx.send(f"{uye.mention} sunucudan yasaklandı. Sebep: {sebep}")
    except discord.Forbidden:
        await ctx.send(" Bu kullanıcıyı yasaklayamıyorum. Gerekli izinlere sahip değilim.")


bot.run(TOKEN)
