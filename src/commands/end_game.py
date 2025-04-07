import discord
from utils.config import get_town_config
from utils.messages import send_temp_message

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

    # Eliminar mensaje de unirse si está configurado
    if config.get("delete_join_message_on_end") and "join_message_id" in config:
        try:
            channel = guild.get_channel(config["notifier_channel_id"])
            msg = await channel.fetch_message(config["join_message_id"])
            await msg.delete()
        except:
            pass  # no pasa nada si falla

    # Canal narrador
    narrator_channel = discord.utils.get(
        guild.text_channels,
        name=f"sala-narrador-{town_name.lower().replace(' ', '-')}"
    )

    if narrator_channel:
        await send_temp_message(
            narrator_channel,
            f"🛑 La partida del pueblo `{town_name}` ha finalizado.\n"
            f"Se han limpiado los roles de `{removed}` usuarios.",
            delay=10
        )

    # Eliminar config si está activado
    if config.get("clear_config_on_end"):
        from utils.config import clear_town_config
        clear_town_config(town_name)
