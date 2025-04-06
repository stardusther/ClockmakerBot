from discord.ext import commands
import discord
from discord.utils import get
from views.night_button import NightButtonView

async def start_game(ctx, town_name):
    guild = ctx.guild

    villager_role = get(guild.roles, name=f"Aldeano {town_name}")
    storyteller_role = get(guild.roles, name=f"Narrador {town_name}")

    if not villager_role or not storyteller_role:
        await ctx.send("❌ No se encontraron los roles necesarios para ese pueblo.")
        return

    if storyteller_role not in ctx.author.roles:
        await ctx.send("❌ Solo un narrador de este pueblo puede iniciar la partida.")
        return

    # Mostrar botón de noche
    view = NightButtonView(town_name, villager_role, storyteller_role)
    await ctx.send("🌙 La partida ha comenzado. Usa este botón para iniciar la noche:", view=view)
