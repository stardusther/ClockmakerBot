# En memoria, podrías sustituirlo por persistencia luego
town_configs = {}

def get_town_config(town_name: str) -> dict:
    return town_configs.setdefault(town_name, {
        "notifier_channel_id": None,
        "delete_join_message_on_end": False,
        "clear_config_on_end": False,
        "category_day_id": None,
        "category_night_id": None
    })

def set_town_config(town_name: str, key: str, value):
    config = get_town_config(town_name)
    config[key] = value

def clear_town_config(town_name: str):
    """Elimina la configuración de un pueblo (por ejemplo al borrar el pueblo)."""
    if town_name in town_configs:
        del town_configs[town_name]
