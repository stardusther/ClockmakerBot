import discord

async def send_temp_message(
    channel: discord.TextChannel,
    content: str = None,
    delay: int = 10,
    embed: discord.Embed = None,
    **kwargs
):
    """
    Envía un mensaje temporal (se elimina tras `delay` segundos).

    Parámetros:
    - channel: Canal donde se envía
    - content: Texto del mensaje (opcional si se usa `embed`)
    - delay: Tiempo en segundos antes de eliminarlo
    - embed: discord.Embed opcional
    - kwargs: Otros argumentos de `channel.send()`
    """
    try:
        await channel.send(content=content, embed=embed, delete_after=delay, **kwargs)
    except discord.Forbidden:
        print(f"[WARN] No tengo permiso para enviar o borrar mensajes en: {channel.name}")
    except Exception as e:
        print(f"[ERROR] Error al enviar mensaje temporal: {e}")
