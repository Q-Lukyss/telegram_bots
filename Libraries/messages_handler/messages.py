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


def is_evil_mode_active(bot_name):
    """Vérifie si le mode evil est activé pour un bot spécifique"""
    return r.get(f"evil_mode_{bot_name.lower()}") == "true"


def toggle_evil_mode(bot_name):
    """Active/désactive le mode evil pour un bot spécifique"""
    key = f"evil_mode_{bot_name.lower()}"
    current_mode = r.get(key)
    if current_mode == "true":
        r.set(key, "false")
        return False
    else:
        r.set(key, "true")
        return True


def get_evil_mode_status(bot_name):
    """Retourne le statut actuel du mode evil pour un bot spécifique"""
    return "activé" if is_evil_mode_active(bot_name) else "désactivé"


def get_random_daily_messages(bot_name=None):
    """Récupère un message journalier en fonction du mode evil du bot qui envoie"""
    data = load_messages()
    if bot_name and is_evil_mode_active(bot_name):
        random_daily_messages = random.choice(data['daily_evil'])
    else:
        random_daily_messages = random.choice(data['daily'])
    return random_daily_messages


def get_cykablyat_comeback():
    cykablyat_comeback = load_messages()['cykablyat_rocket_return']
    return cykablyat_comeback


def get_random_daily_1337_messages(bot_name=None):
    """Récupère un message 1337 en fonction du mode evil du bot qui envoie"""
    data = load_messages()
    if bot_name and is_evil_mode_active(bot_name):
        random_daily_1337_messages = random.choice(data['1337_evil'])
    else:
        random_daily_1337_messages = random.choice(data['1337'])
    return random_daily_1337_messages


def get_random_suce_messages_object():
    data = load_messages()
    return data['suce']