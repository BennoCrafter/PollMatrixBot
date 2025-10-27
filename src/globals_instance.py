from openai import AsyncOpenAI
import simplematrixbotlib as botlib
import os
from dotenv import load_dotenv
from src.utils.logging_config import setup_logger
from typing import Optional

logger = setup_logger(__name__)

load_dotenv()

bot_instance: Optional[botlib.Bot] = None
openAI_client: Optional[AsyncOpenAI] = None


def initialize_globals():
    global bot_instance, openAI_client
    if bot_instance is None:
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        access_token = os.getenv("ACCESS_TOKEN")

        if username and password:
            creds = botlib.Creds(
                homeserver=os.getenv("HOMESERVER"), username=username, password=password
            )
        elif username and access_token:
            creds = botlib.Creds(
                homeserver=os.getenv("HOMESERVER"),
                username=username,
                access_token=access_token,
            )
        else:
            raise Exception("Neither password nor access token provided.")

        bot = botlib.Bot(creds)
        bot_instance = bot

    if openAI_client is None:
        openAI_client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )


def get_openAI_client() -> AsyncOpenAI:
    if openAI_client is None:
        raise RuntimeError("OpenAI client not initialized!")
    return openAI_client


def get_bot() -> botlib.Bot:
    if bot_instance is None:
        raise RuntimeError("Bot instance not initialized!")
    return bot_instance
