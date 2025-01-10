from src.bot_instance import get_bot
import simplematrixbotlib as botlib


async def handle_error(match: botlib.MessageMatch, config: dict) -> None:
    """Send an error reaction to the given event in the room."""
    await get_bot().api.send_reaction(match.room.room_id, match.event, config["reaction"]["error"])
