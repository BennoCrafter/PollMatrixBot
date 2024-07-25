import os
import simplematrixbotlib as botlib
from src.poll import Poll
from dotenv import load_dotenv

load_dotenv()
# deleting session.txt file, to prevent message looping
if os.path.exists("session.txt"):
    os.remove("session.txt")
# Initialize bot credentials from environment variables
creds = botlib.Creds(
    homeserver=os.getenv('HOMESERVER'),
    username=os.getenv('USERNAME'),
    password=os.getenv('PASSWORD')
)
bot = botlib.Bot(creds)
PREFIX = '!'
active_polls: list[Poll] = []

def is_valid(match: botlib.MessageMatch, command_name: str) -> bool:
    """Check if the message matches the given command."""
    return match.is_not_from_this_bot() and match.prefix() and match.command(command_name)

def get_active_poll_in_room(room_id: str) -> Poll | None:
    """Check if there is an active poll in the given room."""
    for poll in active_polls:
        if room_id == poll.room.room_id:
            return poll
    return None

def unicode_to_emoji(unicode_str: str) -> str:
    """Convert a Unicode string to an emoji."""
    return unicode_str.encode('utf-8').decode('unicode_escape')


@bot.listener.on_message_event
async def on_message(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if is_valid(match, "create") and match.args():
        title = ' '.join(match.args())
        await bot.api.send_markdown_message(room.room_id, f"## {title}")

        response = await bot.async_client.room_messages(room_id=room.room_id, start="", limit=1)
        messages = response.chunk
        active_polls.append(Poll(id=len(active_polls), event=messages[0], room=room, result={}))
        return

    if is_valid(match, "close"):
        poll = get_active_poll_in_room(room.room_id)
        if poll:
            # send results
            await bot.api.send_markdown_message(room_id=room.room_id, message=poll.formated_markdown())
            active_polls.remove(poll)
        return

    poll = get_active_poll_in_room(room.room_id)
    if poll and poll.event.event_id != message.event_id:
        poll.add_response(message.body)
        await bot.api.send_reaction(room.room_id, message, "✅")
        print(poll.formated())
        # await bot.api.edit(poll.room.room_id, poll.event.event_id, poll.formated())

bot.run()

# Example of sending a reaction (commented out in original)
# await bot.api.send_reaction(room.room_id, message, "👍")
