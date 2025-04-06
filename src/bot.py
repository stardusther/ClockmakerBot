import os

import discord
from discord.ext import commands

from commands.create_town import setup as setup_create_town
from commands.delete_town import setup as setup_delete_town
from commands.start_game import setup as setup_start_game

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot listo como {bot.user}")

# Register commands
setup_create_town(bot)
setup_delete_town(bot)
setup_start_game(bot)


# Execute bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))

