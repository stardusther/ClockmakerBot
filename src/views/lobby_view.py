import discord

players = []

class LobbyView(discord.ui.View):
    def __init__(self, town_name, villager_role):
        super().__init__(timeout=None)
        self.town_name = town_name
        self.villager_role = villager_role

    @discord.ui.button(label="Unirse a la partida", style=discord.ButtonStyle.primary)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user

        if user not in players:
            players.append(user)
            await user.add_roles(self.villager_role)
            await interaction.response.send_message(
                f"¡{user.display_name} se ha unido a la partida y ha recibido el rol de Aldeano {self.town_name}!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "¡Ya estás en la partida!", ephemeral=True
            )

    @discord.ui.button(label="Ver jugadores", style=discord.ButtonStyle.secondary)
    async def view_players(self, button: discord.ui.Button, interaction: discord.Interaction):
        if players:
            player_list = "\n".join([f"- {p.display_name}" for p in players])
            await interaction.response.send_message(
                f"🎲 Jugadores actuales:\n{player_list}", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Aún no hay jugadores en la partida.", ephemeral=True
            )
class JoinGameView(discord.ui.View):
    def __init__(self, villager_role):
        super().__init__(timeout=None)
        self.villager_role = villager_role

    @discord.ui.button(label="✅ Unirse a la partida", style=discord.ButtonStyle.success)
    async def toggle_join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.villager_role in interaction.user.roles:
            await interaction.user.remove_roles(self.villager_role)
            await interaction.response.send_message("🚪 Has salido de la partida.", ephemeral=True)
            button.label = "✅ Unirse a la partida"
            button.style = discord.ButtonStyle.success
        else:
            await interaction.user.add_roles(self.villager_role)
            await interaction.response.send_message("✅ Te has unido a la partida.", ephemeral=True)
            button.label = "🚪 Irse de la partida"
            button.style = discord.ButtonStyle.secondary

        await interaction.message.edit(view=self)

