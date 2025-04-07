import discord
from utils.config import get_town_config

class ConfigureTownView(discord.ui.View):
    def __init__(self, town_name, guild):
        super().__init__(timeout=120)
        self.town_name = town_name
        self.guild = guild

        config = get_town_config(town_name)

        self.channel_select = NotifierChannelSelect(guild, config)
        self.clear_toggle = BooleanToggle("🧹 ¿Borrar mensaje de unirse tras terminar la partida?", "delete_join", config.get("delete_join_message_on_end", False))
        self.config_toggle = BooleanToggle("🗑️ ¿Eliminar configuración del pueblo al finalizar?", "clear_config", config.get("clear_config_on_end", False))
        self.delete_roles_toggle = BooleanToggle("🧻 ¿Eliminar roles al borrar el pueblo?", "delete_roles", config.get("delete_roles_on_town_delete", True))

        self.add_item(self.channel_select)
        self.add_item(self.clear_toggle)
        self.add_item(self.config_toggle)
        self.add_item(self.delete_roles_toggle)
        self.add_item(SaveButton(self))


class NotifierChannelSelect(discord.ui.Select):
    def __init__(self, guild: discord.Guild, config: dict):
        default_channel_id = str(config.get("notifier_channel_id"))
        options = []

        for ch in guild.text_channels:
            if ch.permissions_for(guild.me).send_messages:
                options.append(discord.SelectOption(
                    label=ch.name,
                    value=str(ch.id),
                    default=(str(ch.id) == default_channel_id)
                ))

        super().__init__(
            placeholder="📢 Selecciona el canal de notificaciones",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()



class BooleanToggle(discord.ui.Select):
    def __init__(self, label: str, identifier: str, current_value: bool = False):
        self.identifier = identifier
        selected_value = "true" if current_value else "false"

        options = [
            discord.SelectOption(
                label=f"{label} ✅ Sí",
                value="true",
                default=(selected_value == "true")
            ),
            discord.SelectOption(
                label=f"{label} ❌ No",
                value="false",
                default=(selected_value == "false")
            ),
        ]

        super().__init__(
            placeholder="Selecciona una opción...",
            min_values=1,
            max_values=1,
            options=options
        )
        self.selected_value = selected_value

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

        try:
            selected_channel_id = int(self.parent_view.channel_select.values[0])
        except (IndexError, TypeError, ValueError):
            await interaction.response.send_message("❌ Debes seleccionar un canal de notificaciones.", delete_after=10)
            return

        config["notifier_channel_id"] = selected_channel_id
        config["delete_join_message_on_end"] = self.parent_view.clear_toggle.get_value()
        config["clear_config_on_end"] = self.parent_view.config_toggle.get_value()
        config["delete_roles_on_town_delete"] = self.parent_view.delete_roles_toggle.get_value()

        await interaction.response.send_message("✅ Ajustes guardados correctamente.", delete_after=10)
        self.parent_view.stop()
