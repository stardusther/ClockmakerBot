import discord
from discord.ext import commands
from commands.start_panel import setup as setup_start_panel
import os
from dotenv import load_dotenv

print(f"🔧 Usando discord.py versión: {discord.__version__}")


# Cargar variables de entorno desde .env
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True


bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot listo como {bot.user}")

# Registrar el panel principal
setup_start_panel(bot)

# Ejecutar bot
bot.run(TOKEN)
