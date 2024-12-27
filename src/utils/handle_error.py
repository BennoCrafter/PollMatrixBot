async def handle_error(bot, room, event, config) -> None:
    """Send an error reaction to the given event in the room."""
    await bot.api.send_reaction(room.room_id, event, config["reaction"]["error"])
