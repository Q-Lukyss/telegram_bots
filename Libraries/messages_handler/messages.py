import json
import os
import random


def load_messages():
    filename = os.path.join(os.path.dirname(__file__), 'messages.json')
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def get_random_daily_messages():
    random_daily_messages = random.choice(load_messages()['daily'])
    return random_daily_messages

def get_cykablyat_comeback():
    cykablyat_comeback = load_messages()['cykablyat_rocket_return']
    return cykablyat_comeback

def get_random_daily_1337_messages():
    random_daily_1337_messages = random.choice(load_messages()['1337'])
    return random_daily_1337_messages

def get_random_suce_messages():
    random_suce_messages = random.choice(load_messages()['suce'])
    return random_suce_messages