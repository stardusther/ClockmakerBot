import discord
from utils.messages import send_temp_message
from utils.config import get_town_config, clear_town_config


async def delete_town(interaction, town_name):
    guild = interaction.guild
    bot_member = guild.me
    config = get_town_config(town_name)

    await interaction.response.defer()

    category_names = [town_name, f"{town_name} - Noche"]
    deleted_any = False

    # Usar el canal desde donde se hace la interacción
    response_channel = interaction.channel

    for name in category_names:
        category = discord.utils.get(guild.categories, name=name)
        if category:
            for channel in category.channels:
                perms = channel.permissions_for(bot_member)
                if perms.manage_channels:
                    try:
                        await channel.delete()
                    except discord.Forbidden:
                        await send_temp_message(
                            response_channel,
                            f"❌ No tengo permiso para eliminar el canal: `{channel.name}`.",
                            delay=10
                        )
                else:
                    await send_temp_message(
                        response_channel,
                        f"⚠️ No tengo permisos suficientes para eliminar `{channel.name}`.",
                        delay=10
                    )
            try:
                await category.delete()
                deleted_any = True
            except discord.Forbidden:
                await send_temp_message(
                    response_channel,
                    f"❌ No tengo permiso para eliminar la categoría `{category.name}`.",
                    delay=10
                )

    if deleted_any:
        await send_temp_message(
            response_channel,
            f"🧹 El pueblo `{town_name}` ha sido eliminado correctamente.",
            delay=10
        )
    else:
        await send_temp_message(
            response_channel,
            f"⚠️ No encontré ninguna categoría llamada `{town_name}` o no tengo acceso.",
            delay=10
        )

    if config.get("delete_roles_on_town_delete", True):
        villager_role = discord.utils.get(guild.roles, name=f"Aldeano {town_name}")
        narrator_role = discord.utils.get(guild.roles, name=f"Narrador {town_name}")

        for role in (villager_role, narrator_role):
            if role:
                try:
                    await role.delete()
                except discord.Forbidden:
                    await send_temp_message(
                        response_channel,
                        f"⚠️ No tengo permiso para eliminar el rol `{role.name}`.",
                        delay=10
                    )

    clear_town_config(town_name)