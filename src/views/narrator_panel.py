import discord
from views.night_day_controls import NightDayControlView

class NarratorRoomView(discord.ui.View):
    def __init__(self, town_name):
        super().__init__(timeout=None)
        self.town_name = town_name

    @discord.ui.button(label="🧙 Crear Partida", style=discord.ButtonStyle.primary)
    async def create_game_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not any(role.name == f"Narrador {self.town_name}" for role in interaction.user.roles):
            await interaction.response.send_message("❌ Solo un narrador de este pueblo puede crear partidas.", ephemeral=True)
            return

        # 👇 Importar aquí para evitar el ciclo
        from views.create_game_modal import CreateGameModal
        await interaction.response.send_modal(CreateGameModal(self.town_name))

    @discord.ui.button(label="🚀 Comenzar Partida", style=discord.ButtonStyle.success)
    async def start_game_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not any(role.name == f"Narrador {self.town_name}" for role in interaction.user.roles):
            await interaction.response.send_message("❌ Solo un narrador puede comenzar la partida.", ephemeral=True)
            return
        await interaction.response.send_message(
            "🎬 ¡La partida ha comenzado! Usa los botones abajo para gestionar el día, la noche y las votaciones.",
            view=NightDayControlView(self.town_name),
            ephemeral=True
        )

    @discord.ui.button(label="🛑 Terminar partida", style=discord.ButtonStyle.danger)
    async def end_game_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        villager_role = discord.utils.get(guild.roles, name=f"Aldeano {self.town_name}")
        

        if not villager_role:
            await interaction.response.send_message(
                "❌ No encontré el rol de Aldeanos para este pueblo.", ephemeral=True)
            return

        # Quitar rol a todos los usuarios
        count = 0
        for member in guild.members:
            if villager_role in member.roles:
                try:
                    await member.remove_roles(villager_role)
                    count += 1
                except:
                    pass

        await interaction.response.send_message(
            f"🧹 Partida finalizada. Se ha eliminado el rol de **{count}** jugador(es).",
            ephemeral=True)

    @discord.ui.button(label="⚙️ Ajustes", style=discord.ButtonStyle.secondary)
    async def config_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not any(role.name == f"Narrador {self.town_name}" for role in interaction.user.roles):
            await interaction.response.send_message(
                "❌ Solo un narrador puede modificar los ajustes.", ephemeral=True)
            return

        # Importa internamente para evitar import circular
        from views.configure_town_modal import ConfigureTownModal
        await interaction.response.send_modal(ConfigureTownModal(self.town_name))

