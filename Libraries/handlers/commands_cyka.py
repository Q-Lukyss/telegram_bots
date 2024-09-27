from telegram import Update
from telegram.ext import CommandHandler

# Commande spécifique à Cyka
async def cyka_command(update: Update, context) -> None:
    await update.message.reply_text("Cyka Blyat!")

def add_cyka_handlers(application):
    application.add_handler(CommandHandler("cyka", cyka_command))
