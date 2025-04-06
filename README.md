# 🤙 Clockmaker Bot

Un bot de Discord en Python para organizar partidas de **Blood on the Clocktower** con soporte para Clocktower.online.

---

## 🚀 Requisitos

- Python 3.8+
- `pip`
- Cuenta de Discord
- Permisos para gestionar un servidor de Discord

---

## 🛠 Instalación

1. Clona este repositorio o descárgalo como `.zip`.

```bash
git clone https://github.com/stardusther/bloodtownbot.git
cd bloodtownbot
```

2. Instala las dependencias (usa un entorno virtual si quieres):

```bash
pip install -r requirements.txt
```

---

## 🔐 Cómo obtener y configurar tu token de bot

1. Ve a [Discord Developer Portal](https://discord.com/developers/applications) y haz clic en **New Application**.
2. Nómbralo (por ejemplo: `BloodTownBot`), luego ve a **Bot** → **Add Bot**.
3. En **Bot > Token**, haz clic en **Reset Token** y cópialo.
4. En **Bot > Privileged Gateway Intents**, activa:
   - ✅ `MESSAGE CONTENT INTENT`
   - ✅ `SERVER MEMBERS INTENT`

5. En tu máquina, crea un archivo `.env` con este contenido:

```env
DISCORD_BOT_TOKEN=tu_token_pegado_aquí
```

**⚠️ Nunca compartas este token. Es tu clave privada.**

---

## 🥪 Uso

1. Ejecuta el bot:

```bash
python bot.py
```

2. En tu servidor de Discord (donde hayas invitado al bot):

```bash
!create_town VillaRosa
```

3. Los jugadores podrán unirse con un botón, y tú puedes iniciar la partida con:

```bash
!start_game VillaRosa
```

---

## 🧼 Comandos disponibles

| Comando                  | Descripción                                        |
|--------------------------|----------------------------------------------------|
| `!crear_pueblo <nombre>` | Crea roles y canales temáticos para un pueblo      |
| `!start_game <nombre>`   | Inicia la partida y muestra botón para iniciar noche |
| `!delete_town <nombre>`  | Elimina todas las categorías y canales del pueblo |

---

## 🤝 Créditos

Hecho con amor por Esther García para facilitar partidas de **Blood on the Clocktower**.  
Apoya el juego original en: https://bloodontheclocktower.com/

---