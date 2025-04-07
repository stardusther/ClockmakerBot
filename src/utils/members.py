import discord

def get_voice_members_with_role(guild: discord.Guild, role: discord.Role) -> list[discord.Member]:
    players = [
        member for member in guild.members
        if role in member.roles and member.voice is not None
    ]
    print(f"[DEBUG] Jugadores en voz con rol {role.name}: {[m.display_name for m in players]}")
    return players
