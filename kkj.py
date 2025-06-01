import discord
from discord.ext import commands
import random
import asyncio
import time
import discloud.config
# ========================== CONFIGURAÇÃO DAS INTENTS ==========================
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # Necessário pra banir membros

bot = commands.Bot(command_prefix="!", intents=intents)

# ========================== LISTAS DE CANTADAS ==========================
cantadas_comuns = [
    "Gata, você acredita em amor à primeira vista ou vou ter que passar de novo com a moto 🏍️",
    "Se você fosse um crime, com certeza seria um assalto... ao meu coração 💔🚓",
    "Nem o Bolsonaro aprova, mas eu faria uma reforma no seu coração 🛠️💖",
    "Gata, se você fosse uma série, com certeza eu te maratonava em um dia 🍿😏",
    "Se beleza desse cadeia, você tava na solitária, pra ninguém nem olhar 🔥😳"
]

cantadas_raras = [
    "Se o crush não te nota, me nota aí só pra eu não ser segunda opção 👀💔",
    "Gata, você não é CPF cancelado, mas tá causando nos meus sentimentos 🔥📉",
    "Você é tão charmosa que minha conexão até caiu, igual o servidor 🖥️😅",
    "Nem o Google Maps me acha, porque eu tô completamente perdido em você 🗺️💘",
    "Se você fosse like, eu te dava curtida eterna 👍💞"
]

cantada_extremamente_rara = "KKKKKKKKKK essa cantada aí eu peguei do Matheus: 'Você é tão bonita que o Windows até parou de responder!' 😂"

# ========================== SISTEMA ANTI-RAID ==========================
message_counter = {}
LIMIT_MESSAGES = 5    # Quantidade de mensagens
TIME_INTERVAL = 5     # Tempo em segundos

# ========================== EVENTO DE BOT ONLINE ==========================
@bot.event
async def on_ready():
    print(f'Bot {bot.user} está online e pronto pra zueira e proteção!')

# ========================== EVENTO AO ENTRAR NO SERVIDOR ==========================
@bot.event
async def on_guild_join(guild):
    owner = guild.owner
    try:
        await owner.send(
            "Salve! Obrigado por me adicionar ao servidor! 😎\n"
            "Me configura direitinho aí ein, senão não faço milagre.\n"
            "Manual do Usuário: [Coloca o link aqui depois]"
        )
    except discord.Forbidden:
        print(f"Não consegui mandar DM pro dono {owner.name}.")

# ========================== COMANDO DE CANTADA ==========================
@bot.command()
async def cantada(ctx):
    await ctx.reply("Por acaso você é mulher? rsrsssrsrsrsrsrsr")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("Demorou demais pra responder, perdeu a chance!")
    else:
        if msg.content.lower() in ['sim', 's']:
            tipo_cantada = random.choices(
                ["comum", "rara", "extremamente_rara"],
                weights=[80, 19, 1],
                k=1
            )[0]

            if tipo_cantada == "comum":
                cantada = random.choice(cantadas_comuns)
            elif tipo_cantada == "rara":
                cantada = random.choice(cantadas_raras)
            else:
                cantada = cantada_extremamente_rara

            await ctx.reply(cantada)

        elif msg.content.lower() in ['não', 'nao', 'n']:
            await ctx.reply("Cai fora macho escroto!")

# ========================== EVENTO DE MENSAGENS (ZUEIRA + ANTI RAID) ==========================
@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return

    msg = message.content.lower()

    # ----------- RESPOSTAS DE FUTEBOL E POLÍTICA -----------
    if bot.user in message.mentions and not msg.startswith("!"):
        await message.reply("Marca não random")

    if "palmeiras" in msg:
        await message.reply("NÃO DIGA MAIS PALMEIRAS!")

    if any(word in msg for word in ["lula", "esquerda"]):
        await message.reply("Hey! aqui é bolsonaro porra!")

    if any(word in msg for word in ["direita", "bolsonaro"]):
        await message.reply("Opa amigão, vc é foda Bolsonaro eterno")

    if "flamengo" in msg:
        await message.reply("Não, flamengo não!")

    if "vasco" in msg:
        await message.reply("Torce pra time morto kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")

    if "são paulo" in msg:
        await message.reply("ISSO AIII PORRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA SÃO PAULO!")

    if "grêmio" in msg or "gremio" in msg:
        await message.reply("Bah!")

    if "corinthians" in msg:
        await message.reply("VAI SE FODER SEU LIXO IDIOTA ARROMBADO(a)")

    # ----------- DETECTOR DE NOMES FEMININOS PRA CANTADA AUTOMÁTICA -----------
    nome_usuario = message.author.display_name.lower()
    nomes_femininos = ["ana", "bia", "carol", "dani", "fernanda", "juliana", "maria", "luana"]

    if any(nome in nome_usuario for nome in nomes_femininos):
        tipo_cantada = random.choices(
            ["comum", "rara", "extremamente_rara"],
            weights=[80, 19, 1],
            k=1
        )[0]

        if tipo_cantada == "comum":
            cantada = random.choice(cantadas_comuns)
        elif tipo_cantada == "rara":
            cantada = random.choice(cantadas_raras)
        else:
            cantada = cantada_extremamente_rara

        await message.reply(cantada)

    # ----------- SISTEMA ANTI-SPAM DE MENSAGEM -----------
    guild_id = message.guild.id
    user_id = message.author.id
    current_time = time.time()

    if guild_id not in message_counter:
        message_counter[guild_id] = {}

    if user_id not in message_counter[guild_id]:
        message_counter[guild_id][user_id] = [1, current_time]
    else:
        msg_count, first_msg_time = message_counter[guild_id][user_id]
        if current_time - first_msg_time <= TIME_INTERVAL:
            message_counter[guild_id][user_id][0] += 1
        else:
            message_counter[guild_id][user_id] = [1, current_time]

        if message_counter[guild_id][user_id][0] >= LIMIT_MESSAGES:
            try:
                await message.guild.ban(message.author, reason="Anti-Raid: Spam detectado.")
                await message.channel.send(f"{message.author.mention} foi banido por spam!")
                print(f"{message.author} foi banido por flood.")
            except Exception as e:
                print(f"Erro ao banir spammer: {e}")

    await bot.process_commands(message)

# ========================== EVENTO ANTI-RAID: CRIAÇÃO DE CANAL ==========================
@bot.event
async def on_guild_channel_create(channel):
    guild = channel.guild
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
        executor = entry.user

        if executor == bot.user or executor.bot:
            return

        try:
            await channel.delete()
            await guild.ban(executor, reason="Anti-Raid: Criação suspeita de canais.")
            await channel.guild.system_channel.send(f"{executor.mention} foi banido por criar canais rapidamente.")
            print(f"{executor} foi banido por criação de canais em massa.")
        except Exception as e:
            print(f"Erro no anti-raid de canal: {e}")

# ========================== EVENTO ANTI-RAID: CRIAÇÃO DE CARGO ==========================
@bot.event
async def on_guild_role_create(role):
    guild = role.guild
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
        executor = entry.user

        if executor == bot.user or executor.bot:
            return

        try:
            await role.delete()
            await guild.ban(executor, reason="Anti-Raid: Criação suspeita de cargos.")
            await guild.system_channel.send(f"{executor.mention} foi banido por criar cargos rapidamente.")
            print(f"{executor} foi banido por criação de cargos em massa.")
        except Exception as e:
            print(f"Erro no anti-raid de cargo: {e}")

# ========================== TOKEN DO BOT ==========================
bot.run('MTMwMjMxOTU5ODIxMzAwOTQzOQ.G_5n9M.Zhm2ItZXRIZoXk_A4am_lqdvkZUVFRUhN5mm7g')
