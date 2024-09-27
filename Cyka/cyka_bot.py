from Libraries.common.base_bot import BaseBot
from Libraries.handlers.commands_common import add_common_handlers
from Libraries.handlers.commands_cyka import add_cyka_handlers

class CykaBot(BaseBot):
    def __init__(self, token):
        super().__init__(token)

    def setup_handlers(self):
        """Enregistrer les commandes spécifiques et communes pour Cyka"""
        add_common_handlers(self.application)  # Commandes communes
        add_cyka_handlers(self.application)    # Commandes spécifiques à Cyka

if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()
    token = os.getenv('CYKA_TOKEN')
    bot = CykaBot(token)
    bot.run()


