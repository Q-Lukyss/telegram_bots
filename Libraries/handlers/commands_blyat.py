import asyncio
import os
import random
from datetime import datetime, timedelta
from pytz import timezone
from services.logger import logger
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder

from Libraries.Emoji_Handler.emoji import load_negative_emoji
from Libraries.messages_handler.messages import get_cykablyat_comeback, get_random_suce_messages_object, toggle_evil_mode, get_evil_mode_status


def add_blyat_handlers(application):
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("blyat", blyat))
    application.add_handler(CommandHandler("cyka", cyka))
    application.add_handler(CommandHandler("sexeanale", sexeanale))
    application.add_handler(CommandHandler("suce", suce))
    application.add_handler(CommandHandler("evil", toggle_evil_mode_command_blyat))

    # Planificateur APScheduler
    scheduler = BackgroundScheduler()
    run_time = datetime.now() + timedelta(minutes=1, seconds=21)
    # Utiliser le déclencheur 'date' pour exécuter une tâche une seule fois
    scheduler.add_job(run_async, 'date', run_date=run_time, args=[send_one_shot_message, application])
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
    message_suce_object = get_random_suce_messages_object()
    if user_id == int(os.getenv("Lukyss_id")):
        await update.message.reply_text(random.choice(message_suce_object['moi']))
        await context.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction='😈')
    elif user_id == int(os.getenv("Vincent_id")):
        await update.message.reply_text(random.choice(message_suce_object['vincent'] + message_suce_object["defaut"]))
        await context.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction=load_negative_emoji())
    elif user_id == int(os.getenv("Florian_id")):
        await update.message.reply_text(random.choice(message_suce_object['florian'] + message_suce_object["defaut"]))
        await context.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction=load_negative_emoji())
    elif user_id == int(os.getenv("Guillaume_id")):
        await update.message.reply_text(random.choice(message_suce_object['guillaume'] + message_suce_object["defaut"]))
        await context.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction=load_negative_emoji())
    else:
        await update.message.reply_text(random.choice(message_suce_object["default"]))
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


# Commande pour activer/désactiver l'evil mode de Blyat
async def toggle_evil_mode_command_blyat(update: Update, context) -> None:
    user_id = update.message.from_user.id
    master_id = int(os.getenv("Lukyss_id"))

    if user_id != master_id:
        await update.message.reply_text("🚫 Seul le maître peut contrôler mon evil mode !")
        return

    evil_activated = toggle_evil_mode("Blyat")

    if evil_activated:
        await update.message.reply_text(
            "😈 MON EVIL MODE ACTIVÉ ! \n\n🔥 Je vais maintenant envoyer des messages... *diaboliques* \n\n💀 - Blyat")
        logger.info(f"[{datetime.now()}] 😈 Evil mode ACTIVÉ pour Blyat par {update.message.from_user.username}")
    else:
        await update.message.reply_text("😇 Mon evil mode désactivé.\n\n🕊️ Retour à la normale...\n\n✅ - Blyat")
        logger.info(f"[{datetime.now()}] 😇 Evil mode DÉSACTIVÉ pour Blyat par {update.message.from_user.username}")


def run_async(func, *args):
    asyncio.run(func(*args))
