from discord.ext import commands
from discord.utils import get
from views.night_button import NightButtonView

def setup(bot):
    @bot.command()
    async def start_game(ctx, *, nombre_pueblo):
        guild = ctx.guild

        aldeano_role = get(guild.roles, name=f"Aldeano {nombre_pueblo}")
        narrador_role = get(guild.roles, name=f"Narrador {nombre_pueblo}")

        if not aldeano_role or not narrador_role:
            await ctx.send("❌ No se encontraron los roles necesarios para ese pueblo.")
            return

        if narrador_role not in ctx.author.roles:
            await ctx.send("❌ Solo un narrador de este pueblo puede iniciar la partida.")
            return

        # Mostrar el botón de Noche
        view = NightButtonView(nombre_pueblo, aldeano_role, narrador_role)
        await ctx.send("🌙 La partida ha comenzado. Usa este botón para iniciar la noche:", view=view)
