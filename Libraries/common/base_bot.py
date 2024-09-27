from telegram.ext import ApplicationBuilder
import logging

class BaseBot:
    def __init__(self, token):
        self.application = ApplicationBuilder().token(token).build()
        self.setup_handlers()

    def setup_handlers(self):
        """Méthode à surcharger dans les bots spécifiques pour enregistrer des handlers"""
        raise NotImplementedError("Cette méthode doit être implémentée dans la sous-classe.")

    def run(self):
        """Démarrer le bot"""
        self.application.run_polling()
