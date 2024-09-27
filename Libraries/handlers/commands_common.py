from telegram import Update
from telegram.ext import CommandHandler

# Commande commune d'aide
async def help_command(update: Update, context) -> None:
    await update.message.reply_text("Voici comment je peux vous aider!")

# Commande commune start
async def start_command(update: Update, context) -> None:
    await update.message.reply_text("Bonjour! Je suis votre assistant commun.")

def add_common_handlers(application):
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
