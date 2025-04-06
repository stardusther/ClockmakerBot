from discord.ext import commands
import discord

async def delete_town(ctx, town_name):
    guild = ctx.guild
    bot_member = guild.me

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
                        await ctx.send(f"❌ No tengo permiso para eliminar el canal: `{channel.name}`.")
                else:
                    await ctx.send(f"⚠️ No tengo permisos suficientes para eliminar `{channel.name}`.")
            try:
                await category.delete()
                deleted_any = True
            except discord.Forbidden:
                await ctx.send(f"❌ No tengo permiso para eliminar la categoría `{category.name}`.")

    if deleted_any:
        await ctx.send(f"🧹 El pueblo `{town_name}` ha sido eliminado.")
    else:
        await ctx.send(f"⚠️ No se encontró ninguna categoría llamada `{town_name}` o `{town_name} - Noche`, o no tengo acceso.")
