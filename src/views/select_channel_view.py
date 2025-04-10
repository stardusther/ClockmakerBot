import discord
from views.lobby_view import JoinGameView, build_lobby_text
from utils.roles import ensure_role

class SelectChannelView(discord.ui.View):
    def __init__(self, town_name, date, time):
        super().__init__(timeout=None)
        self.town_name = town_name
        self.date = date
        self.time = time
        self.selected_channel = None
        self.add_item(ChannelSelect(town_name, self))

class ChannelSelect(discord.ui.Select):
    def __init__(self, town_name, parent_view):
        self.parent_view = parent_view
        options = []

        # Se añadirán en callback dinámicamente
        super().__init__(placeholder="Selecciona un canal para anunciar la partida...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        channel_id = int(self.values[0])
        guild = interaction.guild
        channel = guild.get_channel(channel_id)
        town_name = self.parent_view.town_name
        date = self.parent_view.date
        time = self.parent_view.time
        player_role = discord.utils.get(channel.guild.roles, name="Player")
        mention = player_role.mention if player_role else ""

        if not channel:
            await interaction.response.send_message("❌ Canal no encontrado.", ephemeral=True)
            return

        self.parent_view.selected_channel = channel

        villager_role = await ensure_role(guild, f"Aldeano {self.parent_view.town_name}")
        view = JoinGameView(villager_role)

        message = await channel.send(content=build_lobby_text(villager_role, town_name, date, time, mention),
                                     view=view,
                                     allowed_mentions=discord.AllowedMentions(roles=True))
        view.message = message

        await interaction.response.send_message(f"✅ Partida anunciada en {channel.mention}.", ephemeral=True)

    async def refresh_options(self, guild):
        text_channels = [
            c for c in guild.text_channels
            if c.permissions_for(guild.me).send_messages and not c.is_nsfw()
        ]
        self.options = [
            discord.SelectOption(label=ch.name, value=str(ch.id)) for ch in text_channels
        ]