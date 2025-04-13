import discord
import asyncio
from discord.ui import View
from utils.config import get_town_config
from utils.members import get_voice_members_with_role
from utils.messages import send_temp_message

class NightDayControlView(View):
    def __init__(self, town_name):
        super().__init__(timeout=900)
        self.town_name = town_name

    @discord.ui.button(label="🌙 Noche", style=discord.ButtonStyle.primary)
    async def night_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.move_players(interaction, to_night=True, voting=False)

    @discord.ui.button(label="☀️ Día", style=discord.ButtonStyle.success)
    async def day_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.move_players(interaction, to_night=False, voting=False)

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

        # Canal narrador
        narrator_channel = discord.utils.get(
            guild.text_channels,
            name=f"sala-narrador-{self.town_name.lower().replace(' ', '-')}"
        )

        if not isinstance(category, discord.CategoryChannel):
            await send_temp_message(
                narrator_channel,
                "❌ No se pudo acceder a la categoría correspondiente.",
                delay=10
            )
            return

        # Obtener rol de aldeanos
        villager_role = discord.utils.get(guild.roles, name=f"Aldeano {self.town_name}")
        if not villager_role:
            await send_temp_message(
                narrator_channel,
                "❌ Rol de aldeanos no encontrado.",
                delay=10
            )
            return

        # Obtener jugadores en voz con ese rol
        players = get_voice_members_with_role(guild, villager_role)
        if not players:
            await interaction.channel.send("⚠️ No hay jugadores conectados a voz.",
                                                    delete_after=5)
            return

        # Obtener destinos
        plaza = discord.utils.get(category.voice_channels, name="Plaza del pueblo")
        cabins = [vc for vc in category.voice_channels if "Cabaña" in vc.name]
        chat_channel = discord.utils.get(category.text_channels, name="chat")

        # Mensaje previo en el canal de texto
        if chat_channel:
            if to_night:
                await chat_channel.send(
                    f"🌙 {villager_role.mention} El sol ha caído... Seréis movidos a una cabaña en 5 segundos.")
            elif voting:
                await chat_channel.send(
                    f"💀 {villager_role.mention} Ha llegado la hora de votar. Tenéis 5 segundos para terminar vuestra charla...")
            else:
                await chat_channel.send(
                    f"☀️ {villager_role.mention} Buenos días. Os trasladamos a la Plaza del pueblo en 5 segundos.")

        await interaction.channel.send("🕒 Moviendo jugadores en 5 segundos...",
                                                delete_after=5)
        await asyncio.sleep(5)

        moved = 0
        for i, player in enumerate(players):
            try:
                destination = cabins[i % len(cabins)] if to_night else plaza
                await player.move_to(destination)
                moved += 1
            except Exception as err:
                print(f"[ERROR] Could not move player {player} due to: {err}")
                continue

        await interaction.channel.send(f"✅ {moved} jugadores han sido movidos.",
                                       delete_after=5)
