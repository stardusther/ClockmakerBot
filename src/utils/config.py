import json
import os

CONFIG_FILE = "data/config.json"
town_configs = {}

# 📥 Cargar configuración al arrancar
if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            town_configs = json.load(f)
            print("✅ Configuración cargada desde config.json")
    except json.JSONDecodeError:
        print("⚠️ Archivo de configuración corrupto. Usando configuración vacía.")
        town_configs = {}
else:
    print("📄 No se encontró config.json. Se creará uno nuevo al guardar.")

# 💾 Guardar en disco
def save_config():
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(town_configs, f, indent=2, ensure_ascii=False)
        print("💾 Configuración guardada correctamente.")
    except Exception as e:
        print(f"❌ Error al guardar config.json: {e}")

# ✅ Obtener la configuración de un pueblo
def get_town_config(town_name: str) -> dict:
    return town_configs.setdefault(town_name, {
        "notifier_channel_id": None,
        "delete_join_message_on_end": False,
        "clear_config_on_end": False,
        "category_day_id": None,
        "category_night_id": None,
        "delete_roles_on_town_delete": True
    })

# 🔹 Establecer un valor concreto
def set_town_config(town_name: str, key: str, value):
    config = get_town_config(town_name)
    config[key] = value
    save_config()

# 🔹 Establecer varios valores a la vez
def set_town_config_bulk(town_name: str, values: dict):
    config = get_town_config(town_name)
    config.update(values)
    save_config()

# ❌ Borrar la configuración de un pueblo
def clear_town_config(town_name: str):
    if town_name in town_configs:
        del town_configs[town_name]
        save_config()
