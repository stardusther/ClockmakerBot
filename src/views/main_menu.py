import discord
from discord.ui import View, button
from views.modals import CreateTownModal, DeleteTownModal, StartGameModal

class MainMenuView(View):
    def __init__(self):
        super().__init__(timeout=None)

    def is_storyteller(self, user: discord.Member):
        return any(role.name.startswith("Narrador ") for role in user.roles)

    async def deny_access(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "❌ Solo un narrador puede usar esta opción.",
            ephemeral=True
        )

    @button(label="🏡 Crear Pueblo", style=discord.ButtonStyle.success)
    async def create_town_button(self, interaction, button):
        if not self.is_storyteller(interaction.user):
            return await self.deny_access(interaction)
        await interaction.response.send_modal(CreateTownModal())

    @button(label="🗑️ Eliminar Pueblo", style=discord.ButtonStyle.danger)
    async def delete_town_button(self, interaction, button):
        if not self.is_storyteller(interaction.user):
            return await self.deny_access(interaction)
        await interaction.response.send_modal(DeleteTownModal())

    @button(label="🧙 Comenzar Partida", style=discord.ButtonStyle.primary)
    async def start_game_button(self, interaction, button):
        if not self.is_storyteller(interaction.user):
            return await self.deny_access(interaction)
        await interaction.response.send_modal(StartGameModal())

    @button(label="⚙️ Ajustes", style=discord.ButtonStyle.secondary)
    async def settings_button(self, interaction, button):
        if not self.is_storyteller(interaction.user):
            return await self.deny_access(interaction)
        await interaction.response.send_message("🔧 Función de ajustes aún no implementada.", ephemeral=True)
