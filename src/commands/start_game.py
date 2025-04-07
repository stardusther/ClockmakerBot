from discord.utils import get
from views.night_button import NightButtonView

async def start_game(interaction, town_name):
    guild = interaction.guild

    await interaction.response.defer(ephemeral=True)

    villager_role = get(guild.roles, name=f"Aldeano {town_name}")
    storyteller_role = get(guild.roles, name=f"Narrador {town_name}")

    if not villager_role or not storyteller_role:
        await interaction.followup.send("❌ No se encontraron los roles necesarios para ese pueblo.", ephemeral=True)
        return

    if storyteller_role not in interaction.user.roles:
        await interaction.followup.send("❌ Solo un narrador de este pueblo puede iniciar la partida.", ephemeral=True)
        return

    view = NightButtonView(town_name, villager_role, storyteller_role)
    await interaction.followup.send(
        "🌙 La partida ha comenzado. Usa este botón para iniciar la noche:",
        view=view,
        ephemeral=True
    )
