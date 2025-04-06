from discord.ext import commands
import discord

def setup(bot):
    @bot.command()
    async def delete_town(ctx, *, nombre_pueblo):
        guild = ctx.guild
        categorias = [nombre_pueblo, f"{nombre_pueblo} - Noche"]
        encontrado = False

        for name in categorias:
            category = discord.utils.get(guild.categories, name=name)
            if category:
                for channel in category.channels:
                    await channel.delete()
                await category.delete()
                encontrado = True

        if encontrado:
            await ctx.send(f"🧹 Pueblo `{nombre_pueblo}` eliminado.")
        else:
            await ctx.send(f"No encontré ninguna categoría llamada `{nombre_pueblo}`.")
