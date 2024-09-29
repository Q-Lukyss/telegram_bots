import asyncio
import os
import random
from datetime import datetime, timedelta
from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder

from Libraries.Emoji_Handler.emoji import load_negative_emoji
from Libraries.messages_handler.messages import get_cykablyat_comeback, get_random_suce_messages


def add_blyat_handlers(application):
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("blyat", blyat))
    application.add_handler(CommandHandler("cyka", cyka))
    application.add_handler(CommandHandler("sexeanale", sexeanale))
    application.add_handler(CommandHandler("suce", suce))

    # Planificateur APScheduler
    scheduler = BackgroundScheduler()
    run_time = datetime.now() + timedelta(minutes=1, seconds=21)
    # Utiliser le déclencheur 'date' pour exécuter une tâche une seule fois
    scheduler.add_job(run_async, 'date', run_date=run_time, args=[send_one_shot_message, application])
    # Programmer les messages en boucle avec un index
    delay_seconds = 2
    for i in range(1, len(get_cykablyat_comeback()), 2):
        scheduled_time = run_time + timedelta(seconds=5 + i * delay_seconds)
        scheduler.add_job(lambda i=i: asyncio.run(send_cykablyat_message(i)), 'date', run_date=scheduled_time)
    scheduler.start()


# Commande spécifique à Blyar
async def help_command(update: Update, context) -> None:
    await update.message.reply_text(
        "Euh... alors Voici mes Commandes :\n"
        "/start pour commencer\n"
        "/help pour obtenir cette aide\n"
        "/info pour en apprendre davantage à mon sujet\n"
        "/cyka /blyat Pour rigoler\n"
        "A vous d'explorer le reste hihi\n"
    )


async def info(update: Update, context) -> None:
    await update.message.reply_text('Je suis Blyat une timide esclave prête à vous servir.')


async def cyka(update: Update, context) -> None:
    await update.message.reply_text('Blyat !!! Comme Moi aha ;)')


async def blyat(update: Update, context) -> None:
    await update.message.reply_text('Oui ?')


async def sexeanale(update: Update, context) -> None:
    await update.message.reply_text('Ahah Vous êtes des obsédés UwU')


async def suce(update: Update, context) -> None:
    message_id = update.message.message_id
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    message_suce_object = get_random_suce_messages
    if user_id == int(os.getenv("Lukyss_id")):
        await update.message.reply_text(random(message_suce_object['moi']))
        await context.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction='😈')
    elif user_id == int(os.getenv("Vincent_id")):
        await update.message.reply_text(random(message_suce_object['vincent'] + message_suce_object["default"]))
        await context.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction=load_negative_emoji())
    elif user_id == int(os.getenv("Florian_id")):
        await update.message.reply_text(random(message_suce_object['florian'] + message_suce_object["default"]))
        await context.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction=load_negative_emoji())
    elif user_id == int(os.getenv("Guillaume_id")):
        await update.message.reply_text(random(message_suce_object['guillaume'] + message_suce_object["default"]))
        await context.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction=load_negative_emoji())
    else:
        await update.message.reply_text(random(message_suce_object["default"]))
        await context.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction=load_negative_emoji())


async def send_one_shot_message(context):
    chat_id = os.getenv('TSA_GROUP_ID')
    text = "M.. Moi aussi ! 🥳🥳🥳"
    application = ApplicationBuilder().token(os.getenv('BLYAT_TOKEN')).build()
    await application.bot.send_message(chat_id=chat_id, text=text)


# Fonction générique pour envoyer les messages
async def send_cykablyat_message(index):
    chat_id = os.getenv('TSA_GROUP_ID')
    text = get_cykablyat_comeback()[index]
    application = ApplicationBuilder().token(os.getenv('BLYAT_TOKEN')).build()
    await application.bot.send_message(chat_id=chat_id, text=text)


def run_async(func, *args):
    asyncio.run(func(*args))
