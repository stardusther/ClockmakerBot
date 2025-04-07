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
    def __init__(self, role: discord.Role, member: discord.Member):
        super().__init__(timeout=None)
        self.add_item(ToggleJoinButton(role, member))


class ToggleJoinButton(discord.ui.Button):
    def __init__(self, role: discord.Role, member: discord.Member):
        self.role = role
        self.member = member
        has_role = role in member.roles

        label = "🚪 Irse de la partida" if has_role else "🙋 Unirse a la partida"
        style = discord.ButtonStyle.danger if has_role else discord.ButtonStyle.success

        super().__init__(label=label, style=style)

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        has_role = self.role in member.roles

        if has_role:
            await member.remove_roles(self.role)
            await interaction.response.send_message("🚪 Has salido de la partida.", ephemeral=True)
        else:
            await member.add_roles(self.role)
            await interaction.response.send_message("✅ Te has unido a la partida.", ephemeral=True)

        # Actualizar botón después del cambio
        self.label = "🚪 Irse de la partida" if self.role in member.roles else "🙋 Unirse a la partida"
        self.style = discord.ButtonStyle.danger if self.role in member.roles else discord.ButtonStyle.success

        # Recrear la vista con el nuevo estado del usuario
        new_view = JoinGameView(self.role, interaction.user)
        await interaction.message.edit(view=new_view)


