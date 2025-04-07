import discord
import asyncio
from discord.ui import View
from utils.config import get_town_config
from utils.members import get_voice_members_with_role

class NightDayControlView(View):
    def __init__(self, town_name):
        super().__init__(timeout=900)
        self.town_name = town_name

    @discord.ui.button(label="🌙 Noche", style=discord.ButtonStyle.primary)
    async def night_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.move_players(interaction, to_night=True)

    @discord.ui.button(label="☀️ Día", style=discord.ButtonStyle.success)
    async def day_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.move_players(interaction, to_night=False)

    @discord.ui.button(label="💀 Votar", style=discord.ButtonStyle.danger)
    async def vote_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.move_players(interaction, to_night=False, voting=True)

    async def move_players(self, interaction: discord.Interaction, to_night: bool,
                           voting: bool = False):
        guild = interaction.guild
        config = get_town_config(self.town_name)

        # Debug útil
        print(f"[DEBUG] move_players called — to_night={to_night}, voting={voting}")

        # Obtener categoría
        category_id = config.get("category_night_id") if to_night else config.get("category_day_id")
        category = guild.get_channel(category_id)

        if not isinstance(category, discord.CategoryChannel):
            await interaction.response.send_message(
                "❌ No se pudo acceder a la categoría correspondiente.", ephemeral=True)
            return

        # Obtener rol de aldeanos
        villager_role = discord.utils.get(guild.roles, name=f"Aldeano {self.town_name}")
        if not villager_role:
            await interaction.response.send_message("❌ Rol de aldeanos no encontrado.",
                                                    ephemeral=True)
            return

        # Obtener jugadores en voz con ese rol
        players = get_voice_members_with_role(guild, villager_role)
        if not players:
            await interaction.response.send_message("⚠️ No hay jugadores conectados a voz.",
                                                    ephemeral=True)
            return

        # Obtener destinos
        plaza = discord.utils.get(category.voice_channels, name="Plaza del pueblo")
        cabins = [vc for vc in category.voice_channels if "Cabaña" in vc.name]
        chat_channel = discord.utils.get(category.text_channels, name="chat")

        # Mensaje previo en el canal de texto
        if chat_channel:
            if to_night:
                await chat_channel.send(
                    f"🌙 {villager_role.mention} El sol ha caído... Seréis movidos a una cabaña en 10 segundos.")
            elif voting:
                await chat_channel.send(
                    f"💀 {villager_role.mention} Ha llegado la hora de votar. Tenéis 10 segundos para terminar vuestra charla...")
            else:
                await chat_channel.send(
                    f"☀️ {villager_role.mention} Buenos días. Os trasladamos a la Plaza del pueblo en 10 segundos.")

        await interaction.response.send_message("🕒 Moviendo jugadores en 10 segundos...",
                                                ephemeral=True)
        await asyncio.sleep(10)

        moved = 0
        for i, player in enumerate(players):
            try:
                destination = cabins[i % len(cabins)] if to_night else plaza
                await player.move_to(destination)
                moved += 1
            except Exception as err:
                print(f"[ERROR] Could not move player {player} due to: {err}")
                continue

        await interaction.channel.send(f"✅ {moved} jugadores han sido movidos.", delete_after=5)
        # else:
        #     await interaction.response.send_message(f"✅ {moved} jugadores han sido movidos.", delete_after=5)
