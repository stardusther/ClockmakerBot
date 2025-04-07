import discord

# 🎨 Colores personalizados por tipo de rol
ROLE_COLORS = {
    "Aldeano": discord.Colour.green(),
    "Narrador": discord.Colour.purple(),
    # Puedes añadir más si quieres
}

async def ensure_role(guild: discord.Guild, role_name: str, ctx: discord.Interaction = None) -> discord.Role:
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        # Detectar color según prefijo
        color = discord.Colour.default()
        for prefix, assigned_color in ROLE_COLORS.items():
            if role_name.startswith(prefix):
                color = assigned_color
                break

        role = await guild.create_role(name=role_name, colour=color)

        if ctx:
            await ctx.response.send_message(f"🆕 Rol creado: `{role.name}`", ephemeral=True)

    return role
