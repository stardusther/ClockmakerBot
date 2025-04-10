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


def build_lobby_text(role: discord.Role, town_name: str = "Pueblo", date: str = None,
                     time: str = None, mention: discord.Role = None) -> str:
    members = [member.display_name for member in role.members if not member.bot]

    if not members:
        player_list = "*Nadie se ha unido todavía.*"
    else:
        player_list = "\n".join(f"• {name}" for name in members)

    lines = [
        f"{mention}\n\n"
        f"🎭 ¡Nueva partida en **{town_name}!",
        f"👥 Jugadores apuntados: `{len(members)}`\n\n"
    ]

    if date:
        lines.append(f"📅 Fecha: `{date}`")
    if time:
        lines.append(f"🕒 Hora: `{time}`")

    lines.append("\n **Participantes:**")
    lines.append(player_list)
    lines.append("\nElige una opción 👇")

    return "\n".join(lines)


class JoinGameView(discord.ui.View):
    def __init__(self, role: discord.Role):
        super().__init__(timeout=None)
        self.role = role
        self.message = None  # se seteará más tarde

        self.add_item(JoinButton(role, self))
        self.add_item(LeaveButton(role, self))


class JoinButton(discord.ui.Button):
    def __init__(self, role: discord.Role, parent_view: JoinGameView):
        super().__init__(label="🙋 Unirse a la partida", style=discord.ButtonStyle.success)
        self.role = role
        self.parent_view = parent_view


    async def callback(self, interaction: discord.Interaction):
        member = interaction.user

        if self.role in member.roles:
            await interaction.response.send_message("⚠️ Ya estás en la partida.", ephemeral=True)
        else:
            await member.add_roles(self.role)
            await interaction.response.send_message("✅ Te has unido a la partida.", ephemeral=True)

            if self.parent_view.message:
                await self.parent_view.message.edit(
                    content=build_lobby_text(self.role),
                    view=self.parent_view
                )



class LeaveButton(discord.ui.Button):
    def __init__(self, role: discord.Role, parent_view: JoinGameView):
        super().__init__(label="🚪 Irse de la partida", style=discord.ButtonStyle.danger)
        self.role = role
        self.parent_view = parent_view

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user

        if self.role not in member.roles:
            await interaction.response.send_message("⚠️ No estás en la partida.", ephemeral=True)
        else:
            await member.remove_roles(self.role)
            await interaction.response.send_message("🚪 Has salido de la partida.", ephemeral=True)

            if self.parent_view.message:
                await self.parent_view.message.edit(
                    content=build_lobby_text(self.role),
                    view=self.parent_view
                )




