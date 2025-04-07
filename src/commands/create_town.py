from discord.ext import commands
import discord
from views.narrator_panel import NarratorRoomView
from utils.roles import ensure_role

# Almacén en memoria (temporal): canal narrador -> pueblo
narrator_channel_links = {}

async def create_town(interaction, town_name):
    guild = interaction.guild
    author = interaction.user
    bot_member = guild.me

    await interaction.response.defer(ephemeral=True)

    villager_role = await ensure_role(guild, f"Aldeano {town_name}")
    storyteller_role = await ensure_role(guild, f"Narrador {town_name}")

    await author.add_roles(storyteller_role)

    bot_overwrite = discord.PermissionOverwrite(
        view_channel=True,
        manage_channels=True,
        send_messages=True,
        connect=True
    )

    overwrites_day = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        bot_member: bot_overwrite,
        villager_role: discord.PermissionOverwrite(view_channel=True),
        storyteller_role: discord.PermissionOverwrite(view_channel=True)
    }

    overwrites_night = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        bot_member: bot_overwrite
    }

    category_day = await guild.create_category(town_name, overwrites=overwrites_day)
    category_night = await guild.create_category(f"{town_name} - Noche", overwrites=overwrites_night)

    # Canal exclusivo del narrador
    overwrites_narrator = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        storyteller_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        bot_member: bot_overwrite
    }
    narrator_channel = await guild.create_text_channel(
        f"sala-narrador-{town_name.lower()}",
        overwrites=overwrites_narrator,
        category=category_day
    )

    # Canal de texto público para avisos
    overwrites_chat = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        villager_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        storyteller_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        bot_member: discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }

    chat_channel = await guild.create_text_channel("chat", overwrites=overwrites_chat,
                                                   category=category_day)

    # Guardar asociación canal narrador <-> nombre pueblo
    narrator_channel_links[narrator_channel.id] = town_name

    # Canales públicos (voz y texto para aldeanos)
    await guild.create_voice_channel("Plaza del pueblo", category=category_day)

    voice_channels = [("Pozo", 2), ("Cementerio", 3), ("Granja", 2), ("Bosque", 2), ("Torre", 3)]
    for name, limit in voice_channels:
        await guild.create_voice_channel(name, user_limit=limit, category=category_day)

    for _ in range(20):
        await guild.create_voice_channel("Cabaña", category=category_night)

    # Enviar resumen al narrador
    await narrator_channel.send(
        f"📜 Pueblo `{town_name}` creado.\n"
        f"- Roles: ✅ `{villager_role}`, ✅ `{storyteller_role}`\n"
        f"- Categorías: ✅ {town_name}, ✅ {town_name} - Noche\n"
        f"- Sala del narrador: este canal.\n\n"
        f"Usa los botones de abajo para continuar:",
        view=NarratorRoomView(town_name)
    )

    await interaction.followup.send(f"✅ Pueblo `{town_name}` creado. Puedes gestionar todo desde tu sala privada.", ephemeral=True)
