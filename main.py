from pathlib import Path
import asyncio
import os
import time
from dotenv import load_dotenv
import simplematrixbotlib as botlib

from src.poll import Poll
from src.utils.insert_invisible_char import insert_invisible_char
from src.utils.load_config import load_config
from src.utils.get_quantity_number import get_quantity_number
from src.utils.load_file import load_file

load_dotenv()
config = load_config("assets/config.yaml")
session_file_path = Path(config["session_file"])
# Delete session.txt file if required by configuration.
if session_file_path.exists() and config.get("delete_session_file_on_start"):
    session_file_path.unlink()

creds = botlib.Creds(homeserver=os.getenv('HOMESERVER'),
                     username=os.getenv('USERNAME'),
                     password=os.getenv('PASSWORD'))
bot = botlib.Bot(creds)

help_message = load_file(config["help_message_file"])
active_polls = []
PREFIX = config["prefix"]


def load_configuration():
    """Load environment variables and configuration file."""
    load_dotenv()
    config = load_config("assets/config.yaml")
    return config


def initialize_bot(config):
    """Initialize bot credentials and return bot instance."""
    creds = botlib.Creds(homeserver=os.getenv('HOMESERVER'),
                         username=os.getenv('USERNAME'),
                         password=os.getenv('PASSWORD'))
    return botlib.Bot(creds)


async def handle_error(room, event) -> None:
    await bot.api.send_reaction(room.room_id, event,
                                config["reaction"]["error"])


async def get_sender_name(sender: str) -> str:
    """Get the display name of the sender."""
    displayname_response = await bot.async_client.get_displayname(sender)
    return displayname_response.displayname


def is_valid(match: botlib.MessageMatch, valid_commands: list[str]) -> bool:
    """Check if the message matches any of the valid commands."""
    body_without_prefix = match.event.body[len(match._prefix):]
    command = body_without_prefix.split()[0]
    return command in valid_commands


def get_active_poll_in_room(room_id: str) -> Poll | None:
    """Check if there is an active poll in the given room and return it."""
    return next(
        (poll for poll in active_polls if room_id == poll.room.room_id), None)


async def handle_message(room, message, match, config):
    """Handle incoming messages based on the command."""
    # todo
    if is_valid(match, config["commands"]["help_command"]):
        await bot.api.send_markdown_message(room.room_id, help_message)
    elif is_valid(match, config["commands"]["create_poll_command"]):
        await create_poll(room, message, match)
    elif is_valid(match, config["commands"]["close_poll_command"]):
        await close_poll(room)
    elif is_valid(match, config["commands"]["list_items_command"]):
        await list_items(room)
    elif is_valid(match, config["commands"]["remove_item_command"]):
        await remove_item(room, message, match)
    else:
        await add_item_to_poll(room, message, match, config)


async def create_poll(room, message, match):
    if not match.args():
        await handle_error(room, message)
        return

    title = ' '.join(match.args())
    await bot.api.send_markdown_message(room.room_id, f"## {title}")
    active_polls.append(
        Poll(id=len(active_polls), name=title, room=room, item_entries=[]))


async def close_poll(room):
    poll = get_active_poll_in_room(room.room_id)
    if poll:
        await bot.api.send_markdown_message(
            room.room_id,
            poll.formated_markdown(
                f"## {config['status_title']} {poll.name} (closed):"))
        active_polls.remove(poll)


async def list_items(room):
    poll = get_active_poll_in_room(room.room_id)
    if poll:
        await bot.api.send_markdown_message(
            room.room_id,
            poll.formated_markdown(f"## {config['status_title']} {poll.name}:")
        )


async def remove_item(room, message, match):
    poll = get_active_poll_in_room(room.room_id)
    if not poll or not match.args():
        await handle_error(room, message)
        return

    body_msg = ' '.join(match.args()).strip()
    quantity_num, item_name = get_quantity_number(body_msg)

    count = quantity_num or config["default_quantity_number"]
    item_name = item_name or body_msg

    item = poll.get_item(item_name)
    msg_sender = await get_sender_name(message.sender)

    if not item or msg_sender not in item.user_count or count > item.user_count[
            msg_sender]:
        await handle_error(room, message)
        return

    item.decrease(msg_sender, count)
    if not item.user_count:
        poll.remove_item(item)

    await bot.api.send_reaction(room.room_id, message,
                                config["reaction"]["removed"])


async def add_item_to_poll(room, message, match, config):
    poll = get_active_poll_in_room(room.room_id)
    if not poll:
        return

    body_msg = (message.body.strip() if not config["use_add_command"] else
                ' '.join(match.args()).strip())

    if not body_msg:
        return

    quantity_num, item_name = get_quantity_number(body_msg)

    count = quantity_num or config["default_quantity_number"]
    item_name = item_name or body_msg
    sender_name = await get_sender_name(message.sender)

    poll.add_response(item_name, sender_name, count)
    await bot.api.send_reaction(room.room_id, message,
                                config["reaction"]["success"])


@bot.listener.on_message_event
async def on_message(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot():
        await handle_message(room, message, match, config)


@bot.listener.on_reaction_event
async def on_reaction(room, reaction, k):
    pass  # Reaction handler


if __name__ == "__main__":
    print("Starting Bot...")
    bot.run()
