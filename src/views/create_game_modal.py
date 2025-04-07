import discord
from views.select_channel_view import SelectChannelView

class CreateGameModal(discord.ui.Modal, title="🧙 Crear una nueva partida"):
    def __init__(self, town_name):
        super().__init__()
        self.town_name = town_name

    date = discord.ui.TextInput(label="Fecha", placeholder="Ej: 10/04/2025")
    time = discord.ui.TextInput(label="Hora", placeholder="Ej: 19:00")

    async def on_submit(self, interaction: discord.Interaction):
        view = SelectChannelView(self.town_name, self.date.value, self.time.value)

        # Llenar dinámicamente las opciones del dropdown
        for item in view.children:
            if isinstance(item, discord.ui.Select):
                await item.refresh_options(interaction.guild)

        await interaction.response.send_message(
            "📢 Elige el canal donde anunciar la partida:",
            view=view,
            ephemeral=True
        )