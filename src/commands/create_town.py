from discord.ext import commands
import discord
from views.lobby_view import LobbyView
from utils.roles import ensure_role

async def create_town(ctx, town_name):
    guild = ctx.guild
    author = ctx.author

    villager_role_name = f"Aldeano {town_name}"
    storyteller_role_name = f"Narrador {town_name}"

    villager_role = await ensure_role(guild, villager_role_name, ctx)
    storyteller_role = await ensure_role(guild, storyteller_role_name, ctx)

    await author.add_roles(storyteller_role)

    # Crear categorías
    category_day = await guild.create_category(town_name)
    category_night = await guild.create_category(f"{town_name} - Noche")

    # Canal de voz público
    await guild.create_voice_channel("plaza-del-pueblo", category=category_day)

    # Canal de texto privado para aldeanos y narrador
    overwrites_text = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        villager_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        storyteller_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    await guild.create_text_channel("charla-privada", overwrites=overwrites_text, category=category_day)

    # Canales de voz temáticos
    voice_channels = [
        ("Pozo ", 2),
        ("Cementerio", 3),
        ("Callejón de Barcelona", 2),
        ("Bosque de la bruja Tuerta", 2),
        ("Bajo la Torre del Reloj", None)
    ]
    overwrites_voice = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        villager_role: discord.PermissionOverwrite(view_channel=True, connect=True),
        storyteller_role: discord.PermissionOverwrite(view_channel=True, connect=True)
    }
    for name, limit in voice_channels:
        await guild.create_voice_channel(name, user_limit=limit, overwrites=overwrites_voice, category=category_day)

    # Canales de noche (cabañas)
    overwrites_night = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        storyteller_role: discord.PermissionOverwrite(view_channel=True, connect=True)
    }
    for _ in range(20):
        await guild.create_voice_channel("Cabaña", overwrites=overwrites_night, category=category_night)

    # Mostrar vista de lobby
    view = LobbyView(town_name, villager_role)
    await ctx.send(f"El pueblo `{town_name}` ha sido creado. Los jugadores pueden unirse usando los botones:", view=view)
