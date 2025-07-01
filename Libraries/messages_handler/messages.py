import json
import os
import random
import redis

# Connexion à Redis pour gérer l'état de l'evil mode
r = redis.Redis(host='redis', port=6379, decode_responses=True)

def load_messages():
    filename = os.path.join(os.path.dirname(__file__), 'messages.json')
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def is_evil_mode_active():
    """Vérifie si le mode evil est activé via Redis"""
    return r.get("evil_mode") == "true"


def toggle_evil_mode():
    """Active/désactive le mode evil"""
    current_mode = r.get("evil_mode")
    if current_mode == "true":
        r.set("evil_mode", "false")
        return False
    else:
        r.set("evil_mode", "true")
        return True


def get_evil_mode_status():
    """Retourne le statut actuel du mode evil"""
    return "activé" if is_evil_mode_active() else "désactivé"


def get_random_daily_messages():
    data = load_messages()
    if is_evil_mode_active():
        random_daily_messages = random.choice(data['daily_evil'])
    else:
        random_daily_messages = random.choice(data['daily'])
    return random_daily_messages


def get_cykablyat_comeback():
    cykablyat_comeback = load_messages()['cykablyat_rocket_return']
    return cykablyat_comeback

def get_random_daily_1337_messages():
    data = load_messages()
    if is_evil_mode_active():
        random_daily_1337_messages = random.choice(data['1337_evil'])
    else:
        random_daily_1337_messages = random.choice(data['1337'])
    return random_daily_1337_messages


def get_random_suce_messages_object():
    data = load_messages()
    return data['suce']