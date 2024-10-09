import asyncio
import os
from datetime import datetime, timedelta

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder

import logging

from Libraries.messages_handler.messages import get_cykablyat_comeback

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Ajout de l'Handler
def add_cyka_handlers(application):
    application.add_handler(CommandHandler("cyka", cyka))
    application.add_handler(CommandHandler("help", help_command_cyka))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("blyat", blyat))
    application.add_handler(CommandHandler("sexeanale", sexeanale))
    application.add_handler(CommandHandler("blague", blague))
    application.add_handler(CommandHandler("trivia", trivia))
    application.add_handler(CommandHandler("jours_feries", jours_feries))
    application.add_handler(CommandHandler("ville", villes))
    application.add_handler(CommandHandler("id", get_my_id))

    # Planificateur APScheduler
    scheduler = BackgroundScheduler()
    run_time = datetime.now() + timedelta(minutes=1, seconds=20)
    # Utiliser le déclencheur 'date' pour exécuter une tâche une seule fois
    scheduler.add_job(run_async, 'date', run_date=run_time, args=[send_one_shot_message, application])
    scheduler.start()


# Commande spécifique à Cyka
async def help_command_cyka(update: Update, context) -> None:
    await update.message.reply_text(
        "Je vais vous guider ;)\n"
        "/start pour commencer\n"
        "/help pour obtenir cette aide\n"
        "/info pour en apprendre davantage à mon sujet\n"
        "/cyka /blyat Pour rigoler\n"
        "/ville Nom de Ville pour en apprendre plus sur une ville Française\n"
        "/blague et /trivia sont assez explicites\n"
        "/jours_feries annee aussi\n"
        "/id Pour connaître votre Id Telegram\n"
        "Et bien d'autres commandes Top secrètes dans le futur aha :P\n"
    )



async def info(update: Update, context) -> None:
    await update.message.reply_text('Je suis une délicieuse esclave prête à vous servir.')


async def cyka(update: Update, context) -> None:
    await update.message.reply_text('Blyat !')


async def blyat(update: Update, context) -> None:
    await update.message.reply_text('Cyka ! tel est mon nom en plus aha <3')


async def sexeanale(update: Update, context) -> None:
    await update.message.reply_text('Sexe AnalE ?\nSIIIIIIIIIIIIIIIIIIIIIIIIIIIIII !!!')


async def blague(update: Update, context) -> None:
    url = "https://official-joke-api.appspot.com/jokes/random"
    response = requests.get(url)
    if response.status_code == 200:
        joke_data = response.json()
        joke_text = f"{joke_data['setup']} - {joke_data['punchline']}"
        await update.message.reply_text(joke_text)
    else:
        await update.message.reply_text("Désolé, je n'ai pas pu obtenir une blague pour le moment.")


async def trivia(update: Update, context) -> None:
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(url)
    if response.status_code == 200:
        fact_data = response.json()
        fact_text = fact_data['text']
        await update.message.reply_text(fact_text)
    else:
        await update.message.reply_text("Désolé, je n'ai pas pu obtenir un fait intéressant pour le moment.")


async def jours_feries(update: Update, context) -> None:
    if len(context.args) != 1:
        await update.message.reply_text("Veuillez fournir une année. Par exemple : /jours_feries 2024")
        return
    annee = context.args[0]
    url = f"https://calendrier.api.gouv.fr/jours-feries/metropole/{annee}.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        jour_ferie_data = response.json()
        jour_ferie_texts = []
        for date, nom in jour_ferie_data.items():
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date_formatted = date_obj.strftime("%A %d %B %Y").capitalize()
            jour_ferie_texts.append(f"{date_formatted} : {nom}")
        jour_ferie_text = '\n'.join(jour_ferie_texts)
        await update.message.reply_text(jour_ferie_text)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching jours fériés: {e}")
        await update.message.reply_text(f"Désolé, je n'ai pas pu obtenir la liste des jours fériés pour {annee}.")


async def villes(update: Update, context) -> None:
    if len(context.args) == 0:
        await update.message.reply_text("Veuillez fournir le nom d'une ville. Par exemple : /villes Reims")
        return

    city_name = ' '.join(context.args)
    url = f"https://geo.api.gouv.fr/communes?nom={city_name}&fields=nom,code,codesPostaux,siren,codeEpci,codeDepartement,codeRegion,population&_limit=5"
    try:
        response = requests.get(url)
        response.raise_for_status()
        city_data = response.json()
        if not city_data:
            await update.message.reply_text(f"Je n'ai trouvé aucune information pour la ville '{city_name}'.")
            return

        city_texts = []
        for city_info in city_data:
            city_text = (
                f"Nom: {city_info['nom']}\n"
                f"Code: {city_info['code']}\n"
                f"Codes Postaux: {', '.join(city_info['codesPostaux'])}\n"
                f"SIREN: {city_info['siren']}\n"
                f"Code EPCI: {city_info['codeEpci']}\n"
                f"Code Département: {city_info['codeDepartement']}\n"
                f"Code Région: {city_info['codeRegion']}\n"
                f"Population: {city_info['population']}\n"
            )
            city_texts.append(city_text)

        await update.message.reply_text('\n\n'.join(city_texts))
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching city information: {e}")
        await update.message.reply_text(f"Désolé, je n'ai pas pu obtenir les informations pour la ville '{city_name}'.")


async def get_my_id(update: Update, context) -> None:
    user_id = update.message.from_user.id
    print(f"User ID: {user_id}")
    await update.message.reply_text(f"Votre id : {user_id}")


async def send_one_shot_message(context):
    chat_id = os.getenv('TSA_GROUP_ID')
    text="Je suis de Retour Motherfuckers, je vous ai manqué (c'est pas une question 😛) !"
    application = ApplicationBuilder().token(os.getenv('CYKA_TOKEN')).build()
    await application.bot.send_message(chat_id=chat_id, text=text)


# Fonction générique pour envoyer les messages
async def send_cykablyat_message(index):
    chat_id = os.getenv('TSA_GROUP_ID')
    text = get_cykablyat_comeback()[index]
    application = ApplicationBuilder().token(os.getenv('CYKA_TOKEN')).build()
    await application.bot.send_message(chat_id=chat_id, text=text)


def run_async(func, *args):
    asyncio.run(func(*args))