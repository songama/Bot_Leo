import discord
from discord.ext import commands
from datetime import datetime

# Configuração do bot
TOKEN = "MTMxMDM5Mzg0MjA4MzU2NTYwOQ.GgckNv.Zx3S4M9FqpF1q2hGLZh1sKC7KcsPht_4LZgQ1Q"  # Token do bot
TEXT_CHANNEL_ID = 1310430922801283102  # ID do canal de texto para notificações

# Inicialização do bot
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="l!", intents=intents)

# Dicionário para armazenar os tempos temporariamente
user_times = {}

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}!")

@bot.event
async def on_voice_state_update(member, before, after):
    try:
        # Busca o canal de texto configurado
        text_channel = bot.get_channel(TEXT_CHANNEL_ID)

        if before.channel != after.channel:
            now = datetime.now()

            # Quando o usuário entra em uma call
            if after.channel:
                user_times[member.id] = {"start": now, "channel": after.channel.name}
                msg = f"📥 {member.name} entrou na call '{after.channel.name}' às {now.strftime('%H:%M:%S')}."
                
                # Envia mensagem para o canal de texto
                if text_channel:
                    await text_channel.send(msg)

            # Quando o usuário sai de uma call
            if before.channel:
                if member.id in user_times and "start" in user_times[member.id]:
                    start_time = user_times[member.id]["start"]
                    channel_name = user_times[member.id]["channel"]
                    time_spent = now - start_time

                    msg = (
                        f"📤 {member.name} saiu da call '{before.channel.name}' às {now.strftime('%H:%M:%S')}. "
                        f"Tempo total na call: {str(time_spent).split('.')[0]}."
                    )
                    
                    # Envia mensagem para o canal de texto
                    if text_channel:
                        await text_channel.send(msg)

                    # Remove o registro temporário do usuário
                    del user_times[member.id]
    except Exception as e:
        print(f"Erro em on_voice_state_update: {e}")

# Inicializa o bot
bot.run("MTMxMDM5Mzg0MjA4MzU2NTYwOQ.GgckNv.Zx3S4M9FqpF1q2hGLZh1sKC7KcsPht_4LZgQ1Q")
