# 🐍 Imagen base con Python 3.10
FROM python:3.10-slim

# 📁 Directorio de trabajo
WORKDIR /app

# 🧩 Instala dependencias del sistema necesarias para discord.py / py-cord
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# 📝 Copiar requirements e instalar dependencias
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 📦 Copiar el resto del código del bot
COPY ./src .

# 🌱 Carga las variables de entorno desde `.env`
# (opcional, también puedes usar docker-compose para esto)
ENV PYTHONUNBUFFERED=1

# 🚀 Comando para lanzar el bot
CMD ["python", "src/bot.py"]
