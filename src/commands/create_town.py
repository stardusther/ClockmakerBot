from discord.ext import commands
import discord
from views.lobby_view import LobbyView
from utils.roles import ensure_role

def setup(bot):
    @bot.command()
    async def create_town(ctx, *, nombre_pueblo):
        guild = ctx.guild
        author = ctx.author

        aldeano_role = await ensure_role(guild, f"Aldeano {nombre_pueblo}", ctx)
        narrador_role = await ensure_role(guild, f"Narrador {nombre_pueblo}", ctx)

        await author.add_roles(narrador_role)

        # Categorías
        category_day = await guild.create_category(nombre_pueblo)
        category_night = await guild.create_category(f"{nombre_pueblo} - Noche")

        # Canal de voz público
        await guild.create_voice_channel("Plaza del Pueblo", category=category_day)

        # Canal de texto privado para jugadores
        overwrites_text = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            aldeano_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            narrador_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        await guild.create_text_channel("charla-privada", overwrites=overwrites_text, category=category_day)

        # Canales de voz temáticos
        voice_channels = [("Pozo", 2), ("Cementerio", 3), ("Granja", 2), ("Bosque", 2), ("Torre", 3)]
        overwrites_voice = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            aldeano_role: discord.PermissionOverwrite(view_channel=True, connect=True),
            narrador_role: discord.PermissionOverwrite(view_channel=True, connect=True)
        }
        for name, limit in voice_channels:
            await guild.create_voice_channel(name, user_limit=limit, overwrites=overwrites_voice, category=category_day)

        # Canales de noche
        overwrites_night = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            narrador_role: discord.PermissionOverwrite(view_channel=True, connect=True)
        }
        for _ in range(20):
            await guild.create_voice_channel("Cabaña", overwrites=overwrites_night, category=category_night)

        # Vista con botones
        view = LobbyView(nombre_pueblo, aldeano_role)
        await ctx.send(f"Pueblo `{nombre_pueblo}` creado. ¡Jugadores pueden unirse abajo!", view=view)
