import discord
from utils.messages import send_temp_message

async def delete_town(interaction, town_name):
    guild = interaction.guild
    bot_member = guild.me

    await interaction.response.defer()

    category_names = [town_name, f"{town_name} - Noche"]
    deleted_any = False

    narrator_channel = discord.utils.get(
        guild.text_channels,
        name=f"sala-narrador-{town_name.lower().replace(' ', '-')}"
    )

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
                            narrator_channel,
                            f"❌ No tengo permiso para eliminar el canal: `{channel.name}`.",
                            delay=10
                        )
                else:
                    await send_temp_message(
                        narrator_channel,
                        f"⚠️ No tengo permisos suficientes para eliminar `{channel.name}`.",
                        delay=10
                    )
            try:
                await category.delete()
                deleted_any = True
            except discord.Forbidden:
                await send_temp_message(
                    narrator_channel,
                    f"❌ No tengo permiso para eliminar la categoría `{category.name}`.",
                    delay=10
                )

    if deleted_any:
        await send_temp_message(
            narrator_channel,
            f"🧹 El pueblo `{town_name}` ha sido eliminado correctamente.",
            delay=10
        )
    else:
        await send_temp_message(
            narrator_channel,
            f"⚠️ No encontré ninguna categoría llamada `{town_name}` o no tengo acceso.",
            delay=10
        )
