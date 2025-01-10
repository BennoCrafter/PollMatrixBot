import simplematrixbotlib as botlib
import os
from dotenv import load_dotenv
from src.utils.logging_config import setup_logger

logger = setup_logger(__name__)

load_dotenv()

bot_instance: botlib.Bot | None = None


def initialize_bot():
    global bot_instance
    if bot_instance is None:
        creds = botlib.Creds(homeserver=os.getenv('HOMESERVER'),
                             username=os.getenv('USERNAME'),
                             password=os.getenv('PASSWORD'))
        bot = botlib.Bot(creds)
        bot_instance = bot

def get_bot() -> botlib.Bot:
    if bot_instance is None:
        raise RuntimeError("Bot instance not initialized!")
    return bot_instance
