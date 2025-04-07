import discord
from utils.config import get_town_config

class ConfigureTownModal(discord.ui.Modal, title="⚙️ Configurar Pueblo"):
    def __init__(self, town_name, guild):
        super().__init__()
        self.town_name = town_name
        self.guild = guild

        self.channel_select = NotifierChannelSelect(guild)
        self.delete_join_toggle = BooleanToggle("¿Borrar mensaje de unirse tras terminar?", "delete_join")
        self.clear_config_toggle = BooleanToggle("¿Eliminar configuración al terminar?", "clear_config")

        self.add_item(self.channel_select)
        self.add_item(self.delete_join_toggle)
        self.add_item(self.clear_config_toggle)

    async def on_submit(self, interaction: discord.Interaction):
        config = get_town_config(self.town_name)

        # Canal de notificaciones
        config["notifier_channel_id"] = int(self.channel_select.values[0])

        # Toggles booleanos
        config["delete_join_message_on_end"] = self.delete_join_toggle.get_value()
        config["clear_config_on_end"] = self.clear_config_toggle.get_value()

        await interaction.response.send_message("✅ Ajustes actualizados para el pueblo.", ephemeral=True)


class NotifierChannelSelect(discord.ui.Select):
    def __init__(self, guild: discord.Guild):
        options = [
            discord.SelectOption(label=ch.name, value=str(ch.id))
            for ch in guild.text_channels
            if ch.permissions_for(guild.me).send_messages
        ]

        super().__init__(
            placeholder="Selecciona canal de notificaciones",
            min_values=1,
            max_values=1,
            options=options
        )


class BooleanToggle(discord.ui.Select):
    def __init__(self, label: str, identifier: str):
        self.identifier = identifier
        options = [
            discord.SelectOption(label="✅ Sí", value="true"),
            discord.SelectOption(label="❌ No", value="false")
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

    def get_value(self):
        return self.selected_value == "true"
