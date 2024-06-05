# Fonction pour lire les emojis depuis le fichier emoji.json
import json
import os
import random


def load_emojis():
    filename = os.path.join(os.path.dirname(__file__), 'emoji.json')
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def load_positive_emoji():
    random_emoji = random.choice(load_emojis()['positive'])
    return random_emoji


def load_negative_emoji():
    random_emoji = random.choice(load_emojis()['negative'])
    return random_emoji