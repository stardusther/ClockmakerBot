import discord

players = []

class LobbyView(discord.ui.View):
    def __init__(self, town_name, aldeano_role):
        super().__init__(timeout=None)
        self.town_name = town_name
        self.aldeano_role = aldeano_role

    @discord.ui.button(label="Unirse a la partida", style=discord.ButtonStyle.primary)
    async def join_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        user = interaction.user

        if user not in players:
            players.append(user)
            await user.add_roles(self.aldeano_role)
            await interaction.response.send_message(
                f"¡{user.display_name} se ha unido a la partida y ha recibido el rol de aldeano de {self.town_name}!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "¡Ya estás en la partida!", ephemeral=True
            )

    @discord.ui.button(label="Ver jugadores", style=discord.ButtonStyle.secondary)
    async def view_players(self, button: discord.ui.Button, interaction: discord.Interaction):
        if players:
            lista = "\n".join([f"- {p.display_name}" for p in players])
            await interaction.response.send_message(
                f"🎲 Jugadores actuales:\n{lista}", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Aún no hay jugadores en la partida.", ephemeral=True
            )
