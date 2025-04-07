import discord

# Configuración en memoria (podrías mover esto a un archivo JSON si quieres persistencia)
town_configs = {}

def get_town_config(town_name):
    return town_configs.setdefault(town_name, {
        "notifier_channel_id": None,
        "delete_join_message_on_end": False
    })

class ConfigureTownModal(discord.ui.Modal, title="⚙️ Configurar Pueblo"):
    def __init__(self, town_name):
        super().__init__()
        self.town_name = town_name

        self.notifier_channel = discord.ui.TextInput(
            label="ID del canal de notificaciones",
            placeholder="Ej: 123456789012345678",
            required=True
        )
        self.delete_join_message = discord.ui.TextInput(
            label="¿Borrar mensaje de unirse tras terminar? (sí/no)",
            placeholder="sí o no",
            required=True
        )

        self.add_item(self.notifier_channel)
        self.add_item(self.delete_join_message)

    async def on_submit(self, interaction: discord.Interaction):
        config = get_town_config(self.town_name)

        # Guardar canal de notificaciones
        try:
            config["notifier_channel_id"] = int(self.notifier_channel.value.strip())
        except ValueError:
            await interaction.response.send_message("❌ El ID del canal debe ser un número.", ephemeral=True)
            return

        # Guardar preferencia de eliminación
        delete_pref = self.delete_join_message.value.strip().lower()
        config["delete_join_message_on_end"] = delete_pref in ["sí", "si", "yes", "true"]

        await interaction.response.send_message(f"✅ Ajustes actualizados para `{self.town_name}`.", ephemeral=True)