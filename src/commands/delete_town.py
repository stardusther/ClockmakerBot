from discord.ext import commands
import discord

async def delete_town(interaction, town_name):
    guild = interaction.guild
    bot_member = guild.me

    # ⚠️ Responder de forma diferida para evitar timeout
    await interaction.response.defer(ephemeral=True)

    category_names = [town_name, f"{town_name} - Noche"]
    deleted_any = False

    for name in category_names:
        category = discord.utils.get(guild.categories, name=name)
        if category:
            for channel in category.channels:
                perms = channel.permissions_for(bot_member)
                if perms.manage_channels:
                    try:
                        await channel.delete()
                    except discord.Forbidden:
                        await interaction.followup.send(f"❌ No tengo permiso para eliminar el canal: `{channel.name}`.", ephemeral=True)
                else:
                    await interaction.followup.send(f"⚠️ No tengo permisos suficientes para eliminar `{channel.name}`.", ephemeral=True)
            try:
                await category.delete()
                deleted_any = True
            except discord.Forbidden:
                await interaction.followup.send(f"❌ No tengo permiso para eliminar la categoría `{category.name}`.", ephemeral=True)

    if deleted_any:
        await interaction.followup.send(f"🧹 El pueblo `{town_name}` ha sido eliminado correctamente.", ephemeral=True)
    else:
        await interaction.followup.send(f"⚠️ No encontré ninguna categoría llamada `{town_name}` o no tengo acceso.", ephemeral=True)
