import asyncio
import os
from datetime import datetime
from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import CommandHandler

from Libraries.Emoji_Handler.emoji import load_negative_emoji


def add_blyat_handlers(application):
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("blyat", blyat))
    application.add_handler(CommandHandler("cyka", cyka))
    application.add_handler(CommandHandler("sexeanale", sexeanale))
    application.add_handler(CommandHandler("suce", suce))


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
    if user_id == int(os.getenv("Lukyss_id")):
        await update.message.reply_text('Pas en public maître voyons ^^')
        await context.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction='😈')
    elif user_id == int(os.getenv("Vincent_id")):
        await update.message.reply_text('Si tu trouves une offrande pour mon maître on verra =3')
        await context.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction=load_negative_emoji())
    else:
        await update.message.reply_text('Même pas en rêve nerd')
        await context.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction=load_negative_emoji())
