import asyncio
import os
import random
import redis
from datetime import datetime
from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder

from Libraries.Emoji_Handler.emoji import load_positive_emoji
from Libraries.handlers.commands_cyka import logger
from Libraries.messages_handler.messages import get_random_daily_messages, get_random_daily_1337_messages


def add_common_handlers(application):
    application.add_handler(CommandHandler("start", start_command))

    # Add a handler to react to text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, love_lukyss_messages))

    # Gérer les tâches programmées Pour Le message journalier
    scheduler = BackgroundScheduler(timezone=timezone('Europe/Paris'))
    scheduler.add_job(run_async, 'cron', hour=8, minute=0, second= 0, args=[send_daily_message, application])
    scheduler.add_job(run_async, 'cron', hour=13, minute=37, second= 5, args=[send_daily_1337_message, application])

    scheduler.start()


# Commande commune d'aide
async def help_command(update: Update, context) -> None:
    await update.message.reply_text("Voici comment je peux vous aider!")


# Commande commune start
async def start_command(update: Update, context) -> None:
    await update.message.reply_text("... Alea Jacta est !\nAucun retour n'est possible !")

async def love_lukyss_messages(update: Update, context):
    message_id = update.message.message_id
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    if user_id == int(os.getenv("Lukyss_id")):
        await context.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction=load_positive_emoji())


# Connexion à Redis
r = redis.Redis(host='redis', port=6379, decode_responses=True)


async def message_journalier(context):
    chat_id = os.getenv('TSA_GROUP_ID')
    today = datetime.now().day
    if today % 2 == 1:
        await context.bot.send_message(chat_id=chat_id, text="Coucou les mecs <3\nPassez une bonne journée :)")


# Fonction générique pour envoyer des messages
async def send_message(context, get_message_func, log_prefix):
    chat_id = os.getenv('TSA_GROUP_ID')

    # Utiliser SETNX pour créer le verrou uniquement si aucun autre ne l'a créé
    if r.set("message_lock", "locked", ex=60, nx=True):  # Verrou avec expiration de 60 secondes
        logger.info(f"[{datetime.now()}] {log_prefix} Verrou créé, envoi du message")

        try:
            # Choisir aléatoirement entre Cyka et Blyat
            bot_choice = random.choice(['Cyka', 'Blyat'])
            text = get_message_func()  # Récupérer le message avec la fonction passée en argument

            if bot_choice == 'Cyka':
                application = ApplicationBuilder().token(os.getenv('CYKA_TOKEN')).build()
            else:
                application = ApplicationBuilder().token(os.getenv('BLYAT_TOKEN')).build()

            await application.bot.send_message(chat_id=chat_id, text=text)
            logger.info(f"[{datetime.now()}] {log_prefix} Message envoyé par {bot_choice}")
        finally:
            # Supprimer le verrou après l'envoi du message
            r.delete("message_lock")
            logger.info(f"[{datetime.now()}] {log_prefix} Verrou supprimé après envoi du message")
    else:
        logger.info(f"[{datetime.now()}] {log_prefix} Un autre bot envoie déjà un message. Annulation.")


# Fonction pour le message journalier classique
async def send_daily_message(context):
    await send_message(context, get_random_daily_messages, "[Message Journalier]")

# Fonction pour le message 1337
async def send_daily_1337_message(context):
    await send_message(context, get_random_daily_1337_messages, "[Message 1337]")


def run_async(func, *args):
    asyncio.run(func(*args))