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
from Libraries.messages_handler.messages import get_random_daily_messages, get_random_daily_1337_messages, \
    get_evil_mode_status

from services.email import send_log_email
from services.logger import logger

# Connexion à Redis
r = redis.Redis(host='redis', port=6379, decode_responses=True)


def add_common_handlers(application, bot_name="unknown"):
    """Ajouter les handlers communs à l'application"""
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("getlogs", send_log))
    application.add_handler(CommandHandler("evilstatus", evil_mode_status_command))

    # Add a handler to react to text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, love_lukyss_messages))

    # Chaque bot initialise son propre scheduler
    setup_scheduler_for_bot(application, bot_name)
    logger.info(f"[{datetime.now()}] Scheduler initialisé pour {bot_name}")


def setup_scheduler_for_bot(application, bot_name):
    """Configurer le scheduler pour chaque bot individuellement"""
    scheduler = BackgroundScheduler(timezone=timezone('Europe/Paris'))

    # Messages journaliers à 8h00
    scheduler.add_job(
        run_async_with_bot_selection,
        'cron',
        hour=8,
        minute=0,
        second=0,
        args=[send_daily_message_with_selection, bot_name],
        id=f'daily_message_{bot_name}',
        replace_existing=True
    )

    # Messages 1337 à 13h37
    scheduler.add_job(
        run_async_with_bot_selection,
        'cron',
        hour=13,
        minute=37,
        second=5,
        args=[send_daily_1337_message_with_selection, bot_name],
        id=f'1337_message_{bot_name}',
        replace_existing=True
    )

    scheduler.start()
    logger.info(f"[{datetime.now()}] Scheduler démarré pour {bot_name}")


async def start_command(update: Update, context) -> None:
    await update.message.reply_text("... Alea Jacta est !\nAucun retour n'est possible !")


async def love_lukyss_messages(update: Update, context):
    message_id = update.message.message_id
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    if user_id == int(os.getenv("Lukyss_id")):
        await context.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction=load_positive_emoji())


async def send_log(update: Update, context) -> None:
    chat_id = os.getenv('TSA_GROUP_ID')
    log_file = '/app/logs/logs.txt'

    if r.set("log_lock", "locked", ex=60, nx=True):
        try:
            if os.path.exists(log_file):
                await send_log_email()
                await update.message.reply_text("Données en cours de transfert...")
                with open(log_file, 'rb') as file:
                    await context.bot.send_document(chat_id=chat_id, document=file)

                os.remove(log_file)
                logger.info(f"[{datetime.now()}] Fichier de log envoyé et supprimé.")
            else:
                await update.message.reply_text("Le fichier de log n'existe pas.")
                logger.warning(f"[{datetime.now()}] Fichier de log non trouvé.")
        finally:
            r.delete("log_lock")
            logger.info(f"[{datetime.now()}] Verrou de log supprimé.")
    else:
        logger.info(f"[{datetime.now()}] Tentative d'envoi de log annulée, un autre bot est déjà en train d'envoyer.")


# Fonction pour la sélection aléatoire du bot qui envoie
async def send_message_with_random_bot(get_message_func, log_prefix, requesting_bot):
    """Fonction qui permet à un bot d'être sélectionné aléatoirement pour envoyer un message"""
    chat_id = os.getenv('TSA_GROUP_ID')
    lock_key = f"message_lock_{log_prefix.replace(' ', '_').replace('[', '').replace(']', '').lower()}"

    # Seulement le bot choisi aléatoirement peut envoyer le message
    chosen_bot = random.choice(['Cyka', 'Blyat'])

    if requesting_bot != chosen_bot:
        logger.info(f"[{datetime.now()}] {log_prefix} {requesting_bot} n'a pas été choisi (choisi: {chosen_bot})")
        return

    # Le bot choisi essaie de prendre le verrou
    if r.set(lock_key, f"locked_by_{requesting_bot}", ex=60, nx=True):
        logger.info(f"[{datetime.now()}] {log_prefix} {requesting_bot} sélectionné et verrou obtenu")

        try:
            # Passer le nom du bot pour récupérer le bon message selon son evil mode
            text = get_message_func(requesting_bot)

            # Utiliser le token du bot qui a été sélectionné
            if requesting_bot == 'Cyka':
                token = os.getenv('CYKA_TOKEN')
            else:
                token = os.getenv('BLYAT_TOKEN')

            temp_application = ApplicationBuilder().token(token).build()
            await temp_application.bot.send_message(chat_id=chat_id, text=text)

            logger.info(f"[{datetime.now()}] {log_prefix} Message envoyé par {requesting_bot}")

            # Log spécial pour l'evil mode
            evil_indicators = ['😈', '💀', '🔥', '💣', '⚡', '🖕', '☠️', '🌚', '🥊', '🔩', '💥', '⚔️', '🏛️', '🦠', '🔨', '🧠', '🦾',
                               '🔪', '🧨']
            if any(indicator in text for indicator in evil_indicators):
                logger.info(f"[{datetime.now()}] {log_prefix} 😈 MESSAGE EVIL ENVOYÉ par {requesting_bot} !")

        except Exception as e:
            logger.error(f"[{datetime.now()}] {log_prefix} Erreur lors de l'envoi par {requesting_bot}: {e}")
        finally:
            r.delete(lock_key)
            logger.info(f"[{datetime.now()}] {log_prefix} Verrou supprimé par {requesting_bot}")
    else:
        logger.info(f"[{datetime.now()}] {log_prefix} {requesting_bot} choisi mais message déjà envoyé")


# Fonctions spécifiques pour chaque type de message
async def send_daily_message_with_selection(requesting_bot):
    await send_message_with_random_bot(get_random_daily_messages, "[Message Journalier]", requesting_bot)


async def send_daily_1337_message_with_selection(requesting_bot):
    await send_message_with_random_bot(get_random_daily_1337_messages, "[Message 1337]", requesting_bot)


# Commande pour vérifier le statut de l'evil mode (les deux bots répondent)
async def evil_mode_status_command(update: Update, context) -> None:
    # Déterminer quel bot répond
    bot_name = "Cyka" if "cyka" in str(context.bot.token).lower() else "Blyat"

    cyka_status = get_evil_mode_status("Cyka")
    blyat_status = get_evil_mode_status("Blyat")

    cyka_emoji = "😈🔥" if cyka_status == "activé" else "😇✨"
    blyat_emoji = "😈🔥" if blyat_status == "activé" else "😇✨"

    await update.message.reply_text(
        f"📊 **STATUT EVIL MODE**\n\n"
        f"{cyka_emoji} **Cyka** : {cyka_status.upper()}\n"
        f"{blyat_emoji} **Blyat** : {blyat_status.upper()}\n\n"
        f"🤖 Statut vérifié par : {bot_name}"
    )


def run_async_with_bot_selection(func, bot_name):
    """Wrapper pour exécuter les fonctions async avec le nom du bot"""
    asyncio.run(func(bot_name))


def run_async(func, *args):
    asyncio.run(func(*args))