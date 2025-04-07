import discord
from discord.ext import commands
from views.main_menu import MainMenuView


def setup(bot):
    @bot.command()
    async def start(ctx):
        author = ctx.author
        storyteller_roles = [role for role in author.roles if role.name.startswith("Narrador")]

        if not storyteller_roles:
            await ctx.send("❌ Este panel solo está disponible para narradores de un pueblo.")
            return

        await ctx.send(
            "🎛️ Panel del Narrador:\n\nElige una opción para comenzar:",
            view=MainMenuView()
        )

