import simplematrixbotlib as botlib
import os
from dotenv import load_dotenv

from src.poll import Poll
from src.utils.insert_invisible_char import insert_invisible_char
from src.utils.load_config import load_config
# Load environment variables
load_dotenv()

# Delete session.txt file to prevent message looping
session_file = "session.txt"
if os.path.exists(session_file):
    os.remove(session_file)

# Initialize bot credentials from environment variables
creds = botlib.Creds(homeserver=os.getenv('HOMESERVER'),
                     username=os.getenv('USERNAME'),
                     password=os.getenv('PASSWORD'))
bot = botlib.Bot(creds)
PREFIX = '!'
active_polls: list[Poll] = []
config = load_config("assets/config.yaml")


def is_valid(match: botlib.MessageMatch, command_name: str) -> bool:
    """Check if the message matches the given command."""
    return (match.is_not_from_this_bot() and match.prefix()
            and match.command(command_name))


def get_active_poll_in_room(room_id: str) -> Poll | None:
    """Check if there is an active poll in the given room and return it."""
    for poll in active_polls:
        if room_id == poll.room.room_id:
            return poll
    return None


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

    if is_valid(match, "help"):
        await bot.api.send_markdown_message(room.room_id, config["help_message_file"])

    if is_valid(match, "create") or is_valid(match, "lunchy"):
        if not match.args():
            await bot.api.send_reaction(room.room_id, message, config["reaction"]["error"])
        
        title = ' '.join(match.args())
        await bot.api.send_markdown_message(room.room_id, f"## {title}")
        active_polls.append(
            Poll(id=len(active_polls), name=title, room=room, items=[]))
        return

    if is_valid(match, "close"):
        poll = get_active_poll_in_room(room.room_id)
        if poll:
            await bot.api.send_markdown_message(room.room_id,
                                                poll.formated_markdown())
            active_polls.remove(poll)
        return

    if is_valid(match, "status"):
        poll = get_active_poll_in_room(room.room_id)
        if poll:
            await bot.api.send_markdown_message(room.room_id,
                                                poll.formated_markdown())
        return

    if is_valid(match, "remove"):
        poll = get_active_poll_in_room(room.room_id)

        if not poll or not match.args():
            await handle_error(room, message)
            return

        name = str(" ".join(match.args()))
        item = poll.get_item(name)
        msg_sender = await get_sender_name(message.sender)

        if not item:
            # item not found
            await handle_error(room, message)
            return

        if msg_sender not in item.users:
            # user didnt add the item
            await handle_error(room, message)
            return

        item.remove(msg_sender)
        if len(item.users) == 0:
            poll.remove_item(item)

        await bot.api.send_reaction(room.room_id, message, config["reaction"]["removed"])
        return

    poll = get_active_poll_in_room(room.room_id)
    if poll:
        sender_name = await get_sender_name(message.sender)
        poll.add_response(message.body, sender_name)
        await bot.api.send_reaction(room.room_id, message, config["reaction"]["sucess"])


@bot.listener.on_reaction_event
async def on_reaction(room, reaction, k):
    pass


bot.run()
