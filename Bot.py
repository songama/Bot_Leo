import discord
from discord.ext import commands
from datetime import datetime, timedelta
import openpyxl
import os

# Configuração do bot
TOKEN = "7aab8dd7f2c255b1c961abc40ef87db8273c8c147a2f0af021745345f5a0870d"  # Substitua pelo token do bot
LOG_CHANNEL_ID = 1310126406537187348  # ID do canal para logs
ADMIN_USER_ID = 473996118645145600  # Seu ID de usuário no Discord para notificações

# Arquivo da planilha
EXCEL_FILE = "dados_bot_discord.xlsx"

# Inicialização do bot
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="l!", intents=intents)

# Dicionário para armazenar os tempos temporariamente
user_times = {}

def save_to_excel(user_id, user_name, channel_name, time_spent):
    """Salva os dados na planilha."""
    if not os.path.exists(EXCEL_FILE):
        # Cria uma nova planilha
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Registros"
        # Cabeçalhos
        ws.append(["Usuário ID", "Nome", "Canal", "Data", "Horas"])
        wb.save(EXCEL_FILE)

    # Abre a planilha e insere os dados
    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb["Registros"]
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    ws.append([user_id, user_name, channel_name, now, str(time_spent)])
    wb.save(EXCEL_FILE)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}!")

@bot.event
async def on_voice_state_update(member, before, after):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    admin_user = await bot.fetch_user(ADMIN_USER_ID)  # Busca o administrador

    if before.channel != after.channel:
        now = datetime.now()

        # Entrando em uma call
        if after.channel:
            user_times[member.id] = {"start": now, "channel": after.channel.name}
            msg = f"📥 {member.name} entrou na call '{after.channel.name}' às {now.strftime('%H:%M:%S')}."
            await log_channel.send(msg)
            await admin_user.send(f"🔔 Notificação: {member.name} entrou na call '{after.channel.name}'.")

        # Saindo de uma call
        if before.channel:
            if member.id in user_times and "start" in user_times[member.id]:
                start_time = user_times[member.id]["start"]
                channel_name = user_times[member.id]["channel"]
                time_spent = now - start_time
                save_to_excel(member.id, member.name, channel_name, time_spent)
                msg = (
                    f"📤 {member.name} saiu da call '{before.channel.name}'. "
                    f"Tempo total: {str(time_spent).split('.')[0]}."
                )
                await log_channel.send(msg)
                await admin_user.send(f"🔔 Notificação: {member.name} saiu da call '{before.channel.name}' após {str(time_spent).split('.')[0]}.")

                # Limpar o registro
                del user_times[member.id]

bot.run("7aab8dd7f2c255b1c961abc40ef87db8273c8c147a2f0af021745345f5a0870d")
