import discord

class NightButtonView(discord.ui.View):
    def __init__(self, town_name, villager_role, storyteller_role):
        super().__init__(timeout=None)
        self.town_name = town_name
        self.villager_role = villager_role
        self.storyteller_role = storyteller_role

    @discord.ui.button(label="🌙 Noche", style=discord.ButtonStyle.danger)
    async def start_night(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user

        if self.storyteller_role not in user.roles:
            await interaction.response.send_message("Solo el narrador puede iniciar la noche.", ephemeral=True)
            return

        guild = interaction.guild
        night_category = discord.utils.get(guild.categories, name=f"{self.town_name} - Noche")
        if not night_category:
            await interaction.response.send_message("No se encontró la categoría de noche.", ephemeral=True)
            return

        cabins = [ch for ch in night_category.voice_channels if "Cabaña" in ch.name]
        if not cabins:
            await interaction.response.send_message("No hay cabañas creadas.", ephemeral=True)
            return

        players_to_move = [m for m in guild.members if self.villager_role in m.roles and m.voice]

        if not players_to_move:
            await interaction.response.send_message("Ningún jugador con rol de aldeano está en un canal de voz.", ephemeral=True)
            return

        moved_count = 0
        for i, player in enumerate(players_to_move):
            target_cabin = cabins[i % len(cabins)]
            try:
                await player.move_to(target_cabin)
                moved_count += 1
            except Exception as e:
                print(f"Error al mover {player.display_name}: {e}")

        await interaction.response.send_message(f"🌙 Noche iniciada. {moved_count} jugadores fueron movidos a las cabañas.")
