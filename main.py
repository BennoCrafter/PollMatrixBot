import os
from dotenv import load_dotenv
import simplematrixbotlib as botlib

from src.poll import Poll
from src.utils.insert_invisible_char import insert_invisible_char
from src.utils.load_config import load_config

# Load environment variables
load_dotenv()

# Load config file
config = load_config("assets/config.yaml")

# Extract config values
session_file = config["session_file"]
PREFIX = config["prefix"]

active_polls: list[Poll] = []

# Delete session.txt file to prevent message looping
if os.path.exists(session_file) and config.get("delete_session_file_on_start"):
    os.remove(session_file)

# Initialize bot credentials from environment variables
creds = botlib.Creds(
    homeserver=os.getenv('HOMESERVER'),
    username=os.getenv('USERNAME'),
    password=os.getenv('PASSWORD')
)
bot = botlib.Bot(creds)

def is_valid(match: botlib.MessageMatch, valid_commands: list[str]) -> bool:
    """Check if the message matches the given command."""
    # check if the message starts with the prefix
    if match._prefix == match.event.body[0:len(match._prefix)]:
        body_without_prefix = match.event.body[len(match._prefix):]
    else:
        return False

    command = body_without_prefix.split()[0]

    return command in valid_commands

def get_active_poll_in_room(room_id: str) -> Poll | None:
    """Check if there is an active poll in the given room and return it."""
    return next((poll for poll in active_polls if room_id == poll.room.room_id), None)

async def handle_error(room, event) -> None:
    await bot.api.send_reaction(room.room_id, event, config["reaction"]["error"])

async def get_sender_name(sender: str) -> str:
    """Get the display name of the sender."""
    displayname_response = await bot.async_client.get_displayname(sender)
    return displayname_response.displayname

@bot.listener.on_message_event
async def on_message(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if not match.is_not_from_this_bot():
        return

    if is_valid(match, config["commands"]["help_command"]):
        await bot.api.send_markdown_message(room.room_id, config["help_message_file"])
        return

    if is_valid(match, config["commands"]["create_poll_command"]):
        if not match.args():
            await handle_error(room, message)
            return

        title = ' '.join(match.args())
        await bot.api.send_markdown_message(room.room_id, f"## {title}")
        active_polls.append(Poll(id=len(active_polls), name=title, room=room, item_entries=[]))
        return

    if is_valid(match, config["commands"]["close_poll_command"]):
        poll = get_active_poll_in_room(room.room_id)
        if poll:
            await bot.api.send_markdown_message(room.room_id, poll.formated_markdown())
            active_polls.remove(poll)
        return

    if is_valid(match, config["commands"]["list_items_command"]):
        poll = get_active_poll_in_room(room.room_id)
        if poll:
            await bot.api.send_markdown_message(room.room_id, poll.formated_markdown())
        return

    if is_valid(match, config["commands"]["remove_item_command"]):
        poll = get_active_poll_in_room(room.room_id)

        if not poll or not match.args():
            await handle_error(room, message)
            return

        name = " ".join(match.args())
        item = poll.get_item(name)
        msg_sender = await get_sender_name(message.sender)

        if not item:
            await handle_error(room, message)
            return

        if msg_sender not in item.user_count:
            await handle_error(room, message)
            return

        item.remove(msg_sender)
        if not item.user_count:
            poll.remove_item(item)

        await bot.api.send_reaction(room.room_id, message, config["reaction"]["removed"])
        return

    poll = get_active_poll_in_room(room.room_id)
    if poll:
        sender_name = await get_sender_name(message.sender)
        poll.add_response(message.body, sender_name)
        await bot.api.send_reaction(room.room_id, message, config["reaction"]["success"])

@bot.listener.on_reaction_event
async def on_reaction(room, reaction, k):
    pass

bot.run()
