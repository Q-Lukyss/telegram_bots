import asyncio
import logging
import requests
import os
import locale

from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from datetime import datetime

# Configurer le locale en français
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'fr_FR')

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()
BLYAT = os.getenv('BLYAT_TOKEN')

# Configurez le journal
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Définissez les fonctions de gestion des commandes
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Coucou, moi c\'est Blyat je suis un peu timide mais je vous servirai de mon mieux.')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Euh... alors Voici mes Commandes :\n"
        "/start pour commencer\n"
        "/help pour obtenir cette aide\n"
        "/info pour en apprendre davantage à mon sujet\n"
        "/cyka /blyat Pour rigoler\n"
        "A vous d'explorer le reste hihi\n"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Je suis Blyat une timide esclave prête à vous servir.')


async def cyka(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Blyat !!! Comme Moi aha ;)')


async def blyat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Oui ?')


async def sexeanale(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Ahah Vous êtes des obsédés UwU')


async def suce(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id == int(os.getenv("Lukyss_id")):
        await update.message.reply_text('Pas en public maître voyons ^^')
    else:
        await update.message.reply_text('Même pas en rêve nerd')


async def message_journalier(context: ContextTypes.DEFAULT_TYPE):
    chat_id = os.getenv('TSA_GROUP_ID')
    today = datetime.now().day
    if today % 2 == 1:
        await context.bot.send_message(chat_id=chat_id, text="Coucou les mecs <3\nPassez une bonne journée :)")


def run_async(func, *args):
    asyncio.run(func(*args))


# Fonction principale du bot
def main() -> None:
    # Créez l'application avec votre token
    application = ApplicationBuilder().token(BLYAT).build()

    # Ajoutez les gestionnaires de commandes
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("blyat", blyat))
    application.add_handler(CommandHandler("cyka", cyka))
    application.add_handler(CommandHandler("sexeanale", sexeanale))
    application.add_handler(CommandHandler("suce", suce))

    # Répétez les messages texte
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Gérer les tâches programmées Pour Le message journalier
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_async, 'cron', hour=8, minute=0, second=0, args=[message_journalier, application])
    scheduler.start()

    # Démarrez le bot
    application.run_polling()


if __name__ == '__main__':
    main()
