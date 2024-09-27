from Libraries.common.base_bot import BaseBot
from Libraries.handlers.commands_common import add_common_handlers
from Libraries.handlers.commands_blyat import add_blyat_handlers

class BlyatBot(BaseBot):
    def __init__(self, token):
        super().__init__(token)

    def setup_handlers(self):
        """Enregistrer les commandes spécifiques et communes pour Blyat"""
        add_common_handlers(self.application)  # Commandes communes
        add_blyat_handlers(self.application)   # Commandes spécifiques à Blyat

if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()
    token = os.getenv('BLYAT_TOKEN')
    bot = BlyatBot(token)
    bot.run()
