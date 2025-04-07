import discord

async def ensure_role(guild, role_name, ctx=None):
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        role = await guild.create_role(name=role_name)
        if ctx:
            await ctx.response.send(f"🆕 Rol creado: `{role.name}`")
    return role
