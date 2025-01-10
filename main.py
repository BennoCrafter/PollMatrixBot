from src.bot_instance import get_bot, initialize_bot
from pathlib import Path
import os
from dotenv import load_dotenv
from nio.events.room_events import ReactionEvent, RoomMessageText
from nio.rooms import MatrixRoom
import simplematrixbotlib as botlib
import datetime
from src.command_system import register_command_from_path

from src.commands.command import Command
from src.poll import Poll
from src.utils.load_config import load_config
from src.utils.get_quantity_number import get_quantity_number
from src.utils.load_file import load_file
from src.utils.logging_config import setup_logger
from src.utils.once_decorator import once
from src.poll_manager import PollManager

# Setup logger
logger = setup_logger(__name__)

# Load environment variables
load_dotenv()
config = load_config("assets/config.yaml")
session_file_path = Path(config["session_file"])

# Remove session.txt file if required by configuration
if session_file_path.exists() and config.get("delete_session_file_on_start"):
    session_file_path.unlink()

PREFIX = config["prefix"]

# init bot instance
initialize_bot()
bot = get_bot()

async def handle_message(match: botlib.MessageMatch, config):
    """Process incoming messages and execute the corresponding command."""

    to_exec_command: Command | None = None
    for command in commands:
        if command.is_valid(match):
            to_exec_command = command
            break

    if to_exec_command is None:
        if not config["use_add_command"]:
            await poll_manager.add_item(match)
            return
        return
    await to_exec_command.execute(message=match)


@bot.listener.on_message_event # type: ignore
async def on_message(room: MatrixRoom, message: RoomMessageText) -> None:
    match = botlib.MessageMatch(room, message, bot, PREFIX)
    if match.is_not_from_this_bot():
        await handle_message(match, config)

@bot.listener.on_reaction_event # type: ignore
async def on_reaction(room: MatrixRoom, reaction: ReactionEvent, k: str) -> None:
    """Handle reactions; currently no operations defined."""
    pass

@bot.listener.on_startup  # type: ignore
@once
async def on_startup(w) -> None:
    logger.info("Bot started successfully.")

def get_all_extensions(for_path: Path) -> list[Path]:
    """Get all extensions for a folder path"""
    paths: list[Path] = []

    for path in for_path.iterdir():
        if path.is_dir() and path.stem not in ["__pycache__"]:
            paths += get_all_extensions(path)
            continue

        if path.suffix != ".py" or path.name.startswith("_") or path.stem in ["command"]:
            continue

        paths.append(path)
    return paths

def load_commands(for_path: Path) -> list[Command]:
    """Load all commands from a folder path"""
    commands: list[Command] = []

    for path in get_all_extensions(for_path):
        tn: list[str] = config["commands"].get(path.stem, [])

        c = register_command_from_path(path, tn)
        if c is not None:
            commands.append(c)

    return commands


if __name__ == "__main__":
    poll_manager = PollManager()
    commands: list[Command] = load_commands(Path("src/commands"))

    logger.info("Starting bot...")
    bot.run()
