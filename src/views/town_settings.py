import discord
from utils.config import get_town_config

class TownSettingsMenu(discord.ui.View):
    def __init__(self, town_name):
        super().__init__(timeout=60)
        self.town_name = town_name

    @discord.ui.button(label="🗂 Categorías de Día/Noche", style=discord.ButtonStyle.secondary)
    async def change_categories(self, interaction: discord.Interaction, button: discord.ui.Button):
        from views.town_settings import CategorySelectView  # si no está ya importado arriba
        await interaction.response.send_message(
            "📂 Selecciona las nuevas categorías:",
            view=CategorySelectView(self.town_name, interaction.guild),
            ephemeral=True
        )

    @discord.ui.button(label="📢 Notificaciones y limpieza", style=discord.ButtonStyle.secondary)
    async def config_modal_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from views.configure_town_modal import ConfigureTownModal
        await interaction.response.send_modal(ConfigureTownModal(self.town_name, interaction.guild))


class CategorySelectView(discord.ui.View):
    def __init__(self, town_name, guild):
        super().__init__(timeout=60)
        self.add_item(CategorySelect(town_name, is_day=True, guild=guild))
        self.add_item(CategorySelect(town_name, is_day=False, guild=guild))



class CategorySelect(discord.ui.Select):
    def __init__(self, town_name, is_day, guild):
        self.town_name = town_name
        self.is_day = is_day

        placeholder = "Categoría de Día" if is_day else "Categoría de Noche"

        # ✅ Generar opciones al crear el componente
        options = [
            discord.SelectOption(label=c.name, value=str(c.id))
            for c in guild.categories
            if c.permissions_for(guild.me).view_channel
        ]

        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options)
        self.selected_value = None

    async def callback(self, interaction: discord.Interaction):
        self.selected_value = self.values[0]
        config = get_town_config(self.town_name)
        key = "category_day_id" if self.is_day else "category_night_id"
        config[key] = int(self.selected_value)

        category = interaction.guild.get_channel(int(self.selected_value))
        label = "día" if self.is_day else "noche"

        await interaction.response.send_message(
            f"✅ Categoría de **{label}** actualizada a `{category.name}`.",
            ephemeral=True
        )

