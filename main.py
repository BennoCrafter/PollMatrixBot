from pathlib import Path
import os
from dotenv import load_dotenv
from nio.events.room_events import ReactionEvent, RoomMessageText
from nio.rooms import MatrixRoom
import simplematrixbotlib as botlib

from src.commands.add_command import AddCommand
from src.commands.command import Command
from src.commands.help_command import HelpCommand
from src.commands.create_poll_command import CreatePollCommand
from src.commands.close_poll_command import ClosePollCommand
from src.commands.list_items import ListItemsCommand
from src.commands.remove_item_command import RemoveItemCommand
from src.poll import Poll
from src.utils.load_config import load_config
from src.utils.get_quantity_number import get_quantity_number
from src.utils.load_file import load_file
from src.utils.logging_config import setup_logger
from src.utils.once_decorator import once
from src.utils.poll_manager import PollManager

# Setup logger
logger = setup_logger()

# Load environment variables
load_dotenv()
config = load_config("assets/config.yaml")
session_file_path = Path(config["session_file"])

# Remove session.txt file if required by configuration
if session_file_path.exists() and config.get("delete_session_file_on_start"):
    session_file_path.unlink()

# Setup bot credentials
creds = botlib.Creds(homeserver=os.getenv('HOMESERVER'),
                     username=os.getenv('USERNAME'),
                     password=os.getenv('PASSWORD'))
bot = botlib.Bot(creds)

# Load help message

active_polls = []
PREFIX = config["prefix"]

commands: list[Command] = [
    HelpCommand(config["commands"]["help_command"]),
    CreatePollCommand(config["commands"]["create_poll_command"]),
    AddCommand(config["commands"]["add_item_command"]),
    RemoveItemCommand(config["commands"]["remove_item_command"]),
    ClosePollCommand(config["commands"]["close_poll_command"]),
    ListItemsCommand(config["commands"]["list_items_command"])
]

def load_configuration():
    """Load environment variables and configuration file."""
    load_dotenv()
    return load_config("assets/config.yaml")

def get_active_poll(room_id: str) -> Poll | None:
    """Retrieve the active poll in the given room, if any."""
    return next((poll for poll in active_polls if poll.room.room_id == room_id), None)

async def handle_message(room: MatrixRoom, message: RoomMessageText, match: botlib.MessageMatch, config):
    """Process incoming messages and execute the corresponding command."""

    to_exec_command: Command | None = None
    for command in commands:
        if command.is_valid(match):
            to_exec_command = command
            break

    if to_exec_command is None:
        if not config["use_add_command"]:
            await PollManager.add_item(bot, room, message, match, config)
            return
        return

    await to_exec_command.execute(bot, message.body, room=room, config=config, match=match, message=message)


@bot.listener.on_message_event # type: ignore
async def on_message(room: MatrixRoom, message: RoomMessageText) -> None:
    match = botlib.MessageMatch(room, message, bot, PREFIX)
    if match.is_not_from_this_bot():
        await handle_message(room, message, match, config)

@bot.listener.on_reaction_event # type: ignore
async def on_reaction(room: MatrixRoom, reaction: ReactionEvent, k: str) -> None:
    """Handle reactions; currently no operations defined."""
    pass

@bot.listener.on_startup  # type: ignore
@once
async def on_startup(w) -> None:
    logger.info("Bot started successfully.")

if __name__ == "__main__":
    logger.info("Starting bot...")
    bot.run()
