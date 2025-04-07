import discord
from utils.config import get_town_config

class ConfigureTownView(discord.ui.View):
    def __init__(self, town_name, guild):
        super().__init__(timeout=120)
        self.town_name = town_name
        self.guild = guild

        self.channel_select = NotifierChannelSelect(guild)
        BooleanToggle("🧹 ¿Borrar mensaje de unirse tras terminar la partida?", "delete_join")
        BooleanToggle("🗑️ ¿Eliminar configuración del pueblo al finalizar?", "clear_config")

        self.add_item(self.channel_select)
        self.add_item(self.clear_toggle)
        self.add_item(self.config_toggle)
        self.add_item(SaveButton(self))

class NotifierChannelSelect(discord.ui.Select):
    def __init__(self, guild: discord.Guild):
        options = [
            discord.SelectOption(label=ch.name, value=str(ch.id))
            for ch in guild.text_channels
            if ch.permissions_for(guild.me).send_messages
        ]

        super().__init__(
            placeholder="📢 Canal de notificaciones (mensajes para jugadores)",
            min_values=1,
            max_values=1,
            options=options
        )
        self.value = None

    async def callback(self, interaction: discord.Interaction):
        self.value = self.values[0]
        await interaction.response.defer()

class BooleanToggle(discord.ui.Select):
    def __init__(self, label: str, identifier: str):
        self.identifier = identifier
        options = [
            discord.SelectOption(label="✅ Sí", value="true", description="Activar esta opción"),
            discord.SelectOption(label="❌ No", value="false", description="Dejar como está")
        ]

        super().__init__(
            placeholder=label,
            min_values=1,
            max_values=1,
            options=options
        )
        self.selected_value = "false"

    async def callback(self, interaction: discord.Interaction):
        self.selected_value = self.values[0]
        await interaction.response.defer()

    def get_value(self):
        return self.selected_value == "true"

class SaveButton(discord.ui.Button):
    def __init__(self, view: ConfigureTownView):
        super().__init__(label="💾 Guardar ajustes", style=discord.ButtonStyle.success)
        self.parent_view = view

    async def callback(self, interaction: discord.Interaction):
        config = get_town_config(self.parent_view.town_name)

        config["notifier_channel_id"] = int(self.parent_view.channel_select.value)
        config["delete_join_message_on_end"] = self.parent_view.clear_toggle.get_value()
        config["clear_config_on_end"] = self.parent_view.config_toggle.get_value()

        await interaction.response.send_message("✅ Ajustes guardados correctamente.", ephemeral=True)
        self.parent_view.stop()
