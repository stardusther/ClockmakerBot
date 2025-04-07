import discord
from commands.create_town import create_town
from commands.delete_town import delete_town

class CreateTownModal(discord.ui.Modal, title="🏡 Crear Pueblo"):
    town_name = discord.ui.TextInput(label="Nombre del pueblo", placeholder="Ej: VillaRosa")

    async def on_submit(self, interaction: discord.Interaction):
        await create_town(interaction, self.town_name.value)

class DeleteTownModal(discord.ui.Modal, title="🗑️ Eliminar Pueblo"):
    town_name = discord.ui.TextInput(label="Nombre del pueblo", placeholder="Ej: VillaRosa")

    async def on_submit(self, interaction: discord.Interaction):
        await delete_town(interaction, self.town_name.value)

