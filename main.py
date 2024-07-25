import os
import simplematrixbotlib as botlib
from src.poll import Poll
from dotenv import load_dotenv

load_dotenv()
# deleting session.txt file, to prevent message looping
if os.path.exists("session.txt"):
    os.remove("session.txt")
# Initialize bot credentials from environment variables
creds = botlib.Creds(homeserver=os.getenv('HOMESERVER'),
                     username=os.getenv('USERNAME'),
                     password=os.getenv('PASSWORD'))
bot = botlib.Bot(creds)
PREFIX = '!'
active_polls: list[Poll] = []


def is_valid(match: botlib.MessageMatch, command_name: str) -> bool:
    """Check if the message matches the given command."""
    return match.is_not_from_this_bot() and match.prefix() and match.command(
        command_name)


def get_active_poll_in_room(room_id: str) -> Poll | None:
    """Check if there is an active poll in the given room."""
    for poll in active_polls:
        if room_id == poll.room.room_id:
            return poll
    return None


def unicode_to_emoji(unicode_str: str) -> str:
    """Convert a Unicode string to an emoji."""
    return unicode_str.encode('utf-8').decode('unicode_escape')

async def get_sender_name(sender: str):
    """Get the name of the sender."""
    w = await bot.async_client.get_displayname(sender)
    return w

@bot.listener.on_message_event
async def on_message(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
    # return if message is from this bot
    if not match.is_not_from_this_bot():
        return
    if is_valid(match, "create") and match.args():
        title = ' '.join(match.args())
        await bot.api.send_markdown_message(room.room_id, f"## {title}")

        response = await bot.async_client.room_messages(room_id=room.room_id,
                                                        start="",
                                                        limit=1)
        messages = response.chunk
        active_polls.append(
            Poll(id=len(active_polls), event=messages[0], room=room,
                 items=[]))
        return

    if is_valid(match, "close"):
        poll = get_active_poll_in_room(room.room_id)
        if poll:
            # send results
            await bot.api.send_markdown_message(
                room_id=room.room_id, message=poll.formated_markdown())
            active_polls.remove(poll)
        return

    poll = get_active_poll_in_room(room.room_id)
    if poll:
        se = await get_sender_name(message.sender)
        poll.add_response(message.body, se)
        await bot.api.send_reaction(room.room_id, message, "✅")
        print(poll.formated())
        # await bot.api.edit(poll.room.room_id, poll.event.event_id, poll.formated())

@bot.listener.on_reaction_event
async def on_reaction(room, reaction, k):
    print(reaction)

bot.run()

# Example of sending a reaction (commented out in original)
# await bot.api.send_reaction(room.room_id, message, "👍")
