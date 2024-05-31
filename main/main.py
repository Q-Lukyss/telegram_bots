import asyncio
from datetime import time

from telegram import Bot
from telegram.ext import Updater

group_id = '-1002123068573' # pour TSA
bot_token = '6327890203:AAEA9yPZe8oAtYLFxf9RRZzUJ0lPAmPr2gc'


async def get_chat_id(bot_token):
    # bot = Bot(token=bot_token)
    # # Essayer plusieurs fois pour obtenir des mises à jour
    # for _ in range(5):  # Essayer 5 fois
    #     updates = await bot.get_updates()
    #     for update in updates:
    #         if update.message and update.message.chat.type in ['group', 'supergroup']:
    #             chat_id = update.message.chat_id
    #             print(f"Group Chat ID: {chat_id}")
    #             return chat_id
    #     print("Aucune mise à jour trouvée, nouvelle tentative dans 2 secondes...")
    #     time.sleep(2)
    #
    # print("Aucun chat de groupe trouvé. Envoie un message dans le groupe d'abord.")
    # return None
    return group_id


async def send_telegram_message(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)
    print(f"Message envoyé à {chat_id}")


async def main():
    # Configuration
    bot_token = '6327890203:AAEA9yPZe8oAtYLFxf9RRZzUJ0lPAmPr2gc'  # Cyka
    message = "https://www.domgrav.com/"
    group_id = '-1002123068573' # pour TSA

    # Obtenir le chat_id
    chat_id = await get_chat_id(bot_token)

    if chat_id:
        # Envoyer le message
        await send_telegram_message(bot_token, chat_id, message)


if __name__ == "__main__":
    asyncio.run(main())
