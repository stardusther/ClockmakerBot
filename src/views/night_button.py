import discord

class NightButtonView(discord.ui.View):
    def __init__(self, town_name, aldeano_role, narrator_role):
        super().__init__(timeout=None)
        self.town_name = town_name
        self.aldeano_role = aldeano_role
        self.narrador_role = narrator_role

    @discord.ui.button(label="🌙 Noche", style=discord.ButtonStyle.danger)
    async def start_night(self, button: discord.ui.Button, interaction: discord.Interaction):
        user = interaction.user

        if self.narrador_role not in user.roles:
            await interaction.response.send_message("Solo el narrador puede iniciar la noche.", ephemeral=True)
            return

        guild = interaction.guild
        night_category = discord.utils.get(guild.categories, name=f"{self.town_name} - Noche")
        if not night_category:
            await interaction.response.send_message("No se encontró la categoría de noche.", ephemeral=True)
            return

        cabanas = [ch for ch in night_category.voice_channels if "Cabaña" in ch.name]
        if not cabanas:
            await interaction.response.send_message("No hay cabañas creadas.", ephemeral=True)
            return

        # Encontrar todos los miembros con el rol de aldeano
        jugadores = [m for m in guild.members if self.aldeano_role in m.roles and m.voice]

        if not jugadores:
            await interaction.response.send_message("Ningún jugador con rol de aldeano está en un canal de voz.", ephemeral=True)
            return

        # Mover a cada jugador a una cabaña (rotativa)
        moved_count = 0
        for i, jugador in enumerate(jugadores):
            destino = cabanas[i % len(cabanas)]
            try:
                await jugador.move_to(destino)
                moved_count += 1
            except Exception as e:
                print(f"Error al mover {jugador.display_name}: {e}")

        await interaction.response.send_message(f"🌙 Noche iniciada. {moved_count} jugadores fueron movidos a las cabañas.")
