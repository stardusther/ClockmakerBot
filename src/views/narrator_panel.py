import discord
from discord.ui import View
from views.night_day_controls import NightDayControlView
from views.town_settings import TownSettingsMenu

class NarratorRoomView(View):
    def __init__(self, town_name):
        super().__init__(timeout=None)
        self.town_name = town_name

    @discord.ui.button(label="🎮 Crear partida", style=discord.ButtonStyle.success)
    async def create_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not any(role.name == f"Narrador {self.town_name}" for role in interaction.user.roles):
            await interaction.response.send_message("❌ Solo el narrador puede crear partidas.", ephemeral=True)
            return

        from views.create_game_modal import CreateGameModal
        await interaction.response.send_modal(CreateGameModal(self.town_name))

    @discord.ui.button(label="🎬 Comenzar partida", style=discord.ButtonStyle.primary)
    async def start_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not any(role.name == f"Narrador {self.town_name}" for role in interaction.user.roles):
            await interaction.response.send_message("❌ Solo el narrador puede comenzar la partida.", ephemeral=True)
            return

        await interaction.response.send_message("🎬 ¡La partida ha comenzado!", ephemeral=True)
        await interaction.channel.send("🕹 Panel de control del día y la noche:", view=NightDayControlView(self.town_name))

    @discord.ui.button(label="⚙️ Ajustes", style=discord.ButtonStyle.secondary)
    async def config_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not any(role.name == f"Narrador {self.town_name}" for role in interaction.user.roles):
            await interaction.response.send_message("❌ Solo un narrador puede modificar los ajustes.", ephemeral=True)
            return

        await interaction.response.send_message(
            f"🔧 Ajustes de `{self.town_name}`:",
            view=TownSettingsMenu(self.town_name),
            ephemeral=True
        )

    @discord.ui.button(label="🛑 Terminar partida", style=discord.ButtonStyle.danger)
    async def end_game_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from commands.end_game import end_game
        await end_game(interaction, self.town_name)
