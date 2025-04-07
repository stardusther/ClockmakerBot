import discord
import asyncio
from utils.members import get_voice_members_with_role

class NightDayControlView(discord.ui.View):
    def __init__(self, town_name):
        super().__init__(timeout=None)
        self.town_name = town_name

    async def move_players(self, interaction: discord.Interaction, to_night: bool):
        guild = interaction.guild
        villager_role = discord.utils.get(guild.roles, name=f"Aldeano {self.town_name}")
        print('Villager role', villager_role, 'town name', self.town_name)
        players = get_voice_members_with_role(guild, villager_role)

        if not players:
            await interaction.response.send_message("⚠️ No hay jugadores conectados a voz.",
                                                    ephemeral=True)
            return

        if to_night:
            category = discord.utils.get(guild.categories, name=f"{self.town_name} - Noche")
            target_name = "una cabaña"
            cabins = [ch for ch in category.voice_channels if "Cabaña" in ch.name]
        else:
            category = discord.utils.get(guild.categories, name=self.town_name)
            target_name = "la Plaza del pueblo"
            plaza = discord.utils.get(category.voice_channels, name="Plaza del pueblo")

        # Canal de texto 'chat' para publicar el aviso
        chat_channel = discord.utils.get(category.text_channels, name="chat")

        if chat_channel:
            if to_night:
                await chat_channel.send(
                    f"🌙 {villager_role.mention} El sol ha caído... Seréis movidos a {target_name} en 10 segundos.")
            else:
                await chat_channel.send(
                    f"☀️ {villager_role.mention} Buenos días. Os trasladamos a {target_name} en 10 segundos.")

        await interaction.response.send_message("🕒 Moviendo jugadores en 10 segundos...",
                                                ephemeral=True)
        await asyncio.sleep(10)

        moved = 0
        for i, player in enumerate(players):
            try:
                destination = cabins[i % len(cabins)] if to_night else plaza
                await player.move_to(destination)
                moved += 1
            except:
                continue

        await interaction.followup.send(f"✅ {moved} jugadores movidos a {target_name}.",
                                        ephemeral=True)


    @discord.ui.button(label="🌙 Noche", style=discord.ButtonStyle.primary)
    async def night_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.move_players(interaction, to_night=True)

    @discord.ui.button(label="☀️ Día", style=discord.ButtonStyle.success)
    async def day_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.move_players(interaction, to_night=False)

    @discord.ui.button(label="💀 Votar", style=discord.ButtonStyle.danger)

    async def vote_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        villager_role = discord.utils.get(guild.roles, name=f"Aldeano {self.town_name}")
        players = [m for m in guild.members if villager_role in m.roles and m.voice]

        if not players:
            await interaction.response.send_message("⚠️ No hay jugadores en canales de voz ahora mismo.", ephemeral=True)
            return

        # Canal Plaza del Pueblo
        category = discord.utils.get(guild.categories, name=self.town_name)
        plaza = discord.utils.get(category.voice_channels, name="Plaza del pueblo")
        chat_channel = discord.utils.get(category.text_channels, name="chat")

        if not plaza or not chat_channel:
            await interaction.response.send_message("❌ No se pudo encontrar la Plaza del pueblo o el canal 'chat'.", ephemeral=True)
            return

        # Aviso en #chat
        await chat_channel.send(
            f"🗳️ {villager_role.mention} Ha llegado la hora de votar. Tenéis 10 segundos para terminar vuestra charla..."
        )

        #await interaction.response.send_message("🕒 Contando 10 segundos para la votación...", ephemeral=True)
        await asyncio.sleep(10)

        # Mover a jugadores a la plaza
        moved = 0
        for player in players:
            try:
                await player.move_to(plaza)
                moved += 1
            except:
                continue

        msg = f"✅ {moved} jugadores han sido llevados a la Plaza del pueblo para votar."
        await interaction.followup.send(msg, ephemeral=False)
        if not interaction.response.is_done():
            await interaction.response.send_message("✅ X jugadores han sido movidos...",
                                                    ephemeral=True)
        else:
            await interaction.followup.send(msg, ephemeral=True)


