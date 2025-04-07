import discord
from utils.config import get_town_config

async def end_game(interaction: discord.Interaction, town_name: str):
    guild = interaction.guild
    config = get_town_config(town_name)

    villager_role = discord.utils.get(guild.roles, name=f"Aldeano {town_name}")
    narrator_role = discord.utils.get(guild.roles, name=f"Narrador {town_name}")
    removed = 0

    # Eliminar roles de los jugadores
    for member in guild.members:
        to_remove = []
        if villager_role and villager_role in member.roles:
            to_remove.append(villager_role)
        if narrator_role and narrator_role in member.roles:
            to_remove.append(narrator_role)
        if to_remove:
            await member.remove_roles(*to_remove)
            removed += 1

    # Opcional: eliminar mensaje de unirse a la partida
    if config.get("delete_join_message_on_end") and "join_message_id" in config:
        try:
            channel = guild.get_channel(config["notifier_channel_id"])
            msg = await channel.fetch_message(config["join_message_id"])
            await msg.delete()
        except:
            pass  # no importa si falla

    # Mensaje de notificación al canal configurado
    target_channel = guild.get_channel(config.get("notifier_channel_id", interaction.channel.id))
    if target_channel:
        await target_channel.send(f"🛑 La partida del pueblo `{town_name}` ha finalizado. Se han limpiado los roles de `{removed}` usuarios.")

    await interaction.response.send_message("✅ Partida terminada.", ephemeral=True)
