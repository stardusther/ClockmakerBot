# 🧙 ClockmakerBot

Bot de Discord para asistir a partidas de **Blood on the Clocktower**, gestionado desde interfaz con botones y modales.  
Compatible con [Clocktower.online](https://clocktower.online).

## 🤖 Invitación del bot

Para invitar el bot a tu servidor con todos los permisos necesarios (gestionar canales, mover usuarios, gestionar roles, etc.), usa el siguiente enlace:

👉 [Invitar a The Clockmaker](https://discord.com/oauth2/authorize?client_id=1358515367953170695&scope=bot+applications.commands&permissions=286329872)

> Este enlace otorga los permisos mínimos requeridos por el bot. Si prefieres configurar los permisos manualmente, puedes hacerlo en el panel de Discord Developer Portal.


---

## 🚀 Requisitos

- Python 3.10 o superior ✅
- `pip`
- Acceso a un servidor de Discord donde tengas permisos para gestionar canales y roles

---

## 🔧 Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/stardusther/ClockmakerBot.git
cd ClockmakerBot
```

2. Crea un entorno virtual (recomendado):

```bash
python3.10 -m venv venv
source venv/bin/activate  # o `source venv/bin/activate.fish` si usas fish shell
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuración del Token

1. Ve al [Discord Developer Portal](https://discord.com/developers/applications)
2. Crea una nueva aplicación y agrega un **bot**
3. Copia el token y pégalo en un archivo `.env` así:

```
DISCORD_BOT_TOKEN=tu_token_aquí
```

⚠️ ¡Nunca subas este archivo a GitHub!

---

## ▶️ Uso

1. Ejecuta el bot:

```bash
python bot.py
```

2. En tu servidor, usa:

```bash
!start
```

Aparecerá una **interfaz visual** con botones para:

- Crear Pueblo
- Eliminar Pueblo
- Comenzar Partida
- Ajustes

---

## 🧼 Comandos internos

| Acción              | Se activa desde la interfaz        |
|---------------------|------------------------------------|
| Crear pueblo        | Modal que pide el nombre del pueblo |
| Eliminar pueblo     | Modal de confirmación              |
| Comenzar partida    | Habilita el botón de "Noche"       |
| Mover jugadores     | Al pulsar "🌙 Noche" los lleva a cabañas |

---

## 📦 Dependencias

- `discord.py` (v2.5.2 o superior)
- `python-dotenv`

---

## 🤝 Créditos

Hecho por Esther García para facilitar partidas de **Blood on the Clocktower**.  
Apoya el juego original en: https://bloodontheclocktower.com/