import logging
import os

log_file = '/app/logs/logs.txt'  # Chemin du fichier de log partagé

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

def log_action(action):
    logger.info(f"{os.getenv('BOT_NAME')} - {action}")
