import asyncio
from typing import Optional
from src.bot_instance import get_bot, initialize_bot
from pathlib import Path
from dotenv import load_dotenv
from nio.events.room_events import ReactionEvent, RoomMessageText
from nio.responses import DirectRoomsErrorResponse, RoomCreateError
from nio.rooms import MatrixRoom
import simplematrixbotlib as botlib
from src.command_system import register_command_from_path

from src.commands.command import Command
from src.utils.load_config import load_config
from src.utils.logging_config import setup_logger
from src.utils.once_decorator import once
from src.poll_manager import PollManager
from src.command_manager import CommandManager

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

    command_match = command_manager.get_matching_command(match)
    if command_match is None:
        return
    # if command_match is None:
    #     if not config["use_add_command"]:
    #         await poll_manager.add_from_match_item(match)
    #         return
    #     return

    command, struct = command_match
    await command.execute(struct)


@bot.listener.on_message_event  # type: ignore
async def on_message(room: MatrixRoom, message: RoomMessageText) -> None:
    match = botlib.MessageMatch(room, message, bot, PREFIX)
    if match.is_not_from_this_bot():
        await handle_message(match, config)


@bot.listener.on_reaction_event  # type: ignore
async def on_reaction(room: MatrixRoom, event: ReactionEvent, reaction: str) -> None:
    """Handle reactions; currently no operations defined."""
    logger.info(
        f"Received from user {event.sender} reaction: {reaction} --> reacts to event id {event.reacts_to}"
    )
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

        if (
            path.suffix != ".py"
            or path.name.startswith("_")
            or path.stem in ["command"]
        ):
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
    for c in commands:
        c.load()

    return commands


async def create_direct_room(user_id: str) -> Optional[str]:
    resp = await bot.async_client.room_create(
        invite=[user_id],
        is_direct=True,
    )
    if isinstance(resp, RoomCreateError):
        logger.error(f"Could not create DM with {user_id}: {resp.message}")
        return

    return resp.room_id


def main():
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt detected, shutting down...")
        asyncio.run(bot.async_client.close())
    finally:
        logger.info("Bot shut down successfully")


if __name__ == "__main__":
    poll_manager = PollManager()
    commands: list[Command] = load_commands(Path("src/commands"))
    command_manager = CommandManager(commands, config.get("prefix", "!"))

    logger.info("Starting bot...")
    main()
