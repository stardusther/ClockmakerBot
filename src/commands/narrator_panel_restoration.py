from discord.ext import commands
import discord
from views.narrator_panel import NarratorRoomView

def is_narrator_channel(channel_name):
    return channel_name.startswith("sala-narrador-")

def extract_town_name(channel_name):
    return channel_name.replace("sala-narrador-", "").strip()

def has_narrator_role(member, town_name):
    expected_role_name = f"Narrador {town_name}"
    return any(role.name == expected_role_name for role in member.roles)

async def restore_narrator_panel(channel, town_name):
    await channel.send(f"🎛 Panel restaurado para **{town_name}**:", view=NarratorRoomView(town_name))

# 🔁 Listener automático: si escribe en su sala, se le reenvía el panel
async def handle_narrator_message(message):
    if message.author.bot:
        return
    if not is_narrator_channel(message.channel.name):
        return

    town_name = extract_town_name(message.channel.name)
    if has_narrator_role(message.author, town_name):
        await restore_narrator_panel(message.channel, town_name)

# 🧩 Setup: comando + event listener
def setup(bot):
    @bot.command(name="panel")
    async def show_panel(ctx):
        for channel in ctx.guild.text_channels:
            if is_narrator_channel(channel.name) and ctx.author in channel.members:
                town_name = extract_town_name(channel.name)
                await restore_narrator_panel(channel, town_name)
                await ctx.send("✅ Panel reenviado a tu sala de narrador.", delete_after=5)
                return
        await ctx.send("❌ No encontré tu sala de narrador.", delete_after=10)

    @bot.event
    async def on_message(message):
        await handle_narrator_message(message)
        await bot.process_commands(message)  # Muy importante para que comandos sigan funcionando
