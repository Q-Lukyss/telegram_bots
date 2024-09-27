from telegram import Update
from telegram.ext import CommandHandler

# Commande spécifique à Blyar
async def blyat_command(update: Update, context) -> None:
    await update.message.reply_text("Blyat!")

def add_blyat_handlers(application):
    application.add_handler(CommandHandler("blyat", blyat_command))
