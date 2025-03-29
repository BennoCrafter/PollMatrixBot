from src.bot_instance import get_bot

async def get_sender_name(sender: str) -> str:
    """Retrieve the display name of the message sender."""
    displayname_response = await get_bot().async_client.get_displayname(sender)
    return displayname_response.displayname # type: ignore
