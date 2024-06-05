import asyncio
import json
import logging
import random
import sys

import requests
import os
import locale

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from datetime import datetime

from Libraries.Emoji_Handler.emoji import load_positive_emoji

# Configurer le locale en français
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'fr_FR')

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()
CYKA = os.getenv('CYKA_TOKEN')

# Configurez le journal
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Définissez les fonctions de gestion des commandes
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Bonjour! Cyka votre parfaite assistante, comment puis-je vous servir?')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Je suis une délicieuse esclave prête à vous servir.')


async def cyka(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Blyat !')


async def blyat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Cyka ! tel est mon nom en plus aha <3')


async def sexeanale(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Sexe AnalE ?\nSIIIIIIIIIIIIIIIIIIIIIIIIIIIIII !!!')


async def blague(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = "https://official-joke-api.appspot.com/jokes/random"
    response = requests.get(url)
    if response.status_code == 200:
        joke_data = response.json()
        joke_text = f"{joke_data['setup']} - {joke_data['punchline']}"
        await update.message.reply_text(joke_text)
    else:
        await update.message.reply_text("Désolé, je n'ai pas pu obtenir une blague pour le moment.")


async def trivia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(url)
    if response.status_code == 200:
        fact_data = response.json()
        fact_text = fact_data['text']
        await update.message.reply_text(fact_text)
    else:
        await update.message.reply_text("Désolé, je n'ai pas pu obtenir un fait intéressant pour le moment.")


async def jours_feries(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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


async def villes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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


async def get_my_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    print(f"User ID: {user_id}")
    await update.message.reply_text(f"Votre id : {user_id}")


# Fonction pour réagir aux messages
async def like_lukyss_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = update.message.message_id
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    if user_id == int(os.getenv("Lukyss_id")):
        await context.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction=load_positive_emoji())


# Fonction pour envoyer un message tous les jours pairs
async def message_journalier(context: ContextTypes.DEFAULT_TYPE):
    chat_id = os.getenv('TSA_GROUP_ID')
    today = datetime.now().day
    if today % 2 == 0:
        await context.bot.send_message(chat_id=chat_id, text="Hello les boyz !!!\nBon courage pour aujourd'hui <3")


# Fonction synchrone pour appeler une coroutine
# Besoin de ceci car les APScheduler appelle des functions synchrones et non asynchrones
def run_async(func, *args):
    asyncio.run(func(*args))


# Fonction principale du bot
def main() -> None:
    # Créez l'application avec votre token
    application = ApplicationBuilder().token(CYKA).build()

    # Ajoutez les gestionnaires de commandes
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("blyat", blyat))
    application.add_handler(CommandHandler("cyka", cyka))
    application.add_handler(CommandHandler("sexeanale", sexeanale))
    application.add_handler(CommandHandler("blague", blague))
    application.add_handler(CommandHandler("trivia", trivia))
    application.add_handler(CommandHandler("jours_feries", jours_feries))
    application.add_handler(CommandHandler("villes", villes))
    application.add_handler(CommandHandler("id", get_my_id))

    # Add a handler to react to text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, like_lukyss_messages))

    # Gérer les tâches programmées Pour Le message journalier
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_async, 'cron', hour=8, minute=0, second=0, args=[message_journalier, application])
    scheduler.start()

    # Démarrez le bot
    application.run_polling()


if __name__ == '__main__':
    main()
