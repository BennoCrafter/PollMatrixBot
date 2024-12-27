from src.poll import Poll
import logging
from src.utils.get_quantity_number import get_quantity_number
from src.utils.handle_error import handle_error


# Setup logger
logger = logging.getLogger(__name__)

active_polls = []

class PollManager:
    """Centralized manager for handling polls."""

    @staticmethod
    async def create_poll(room, match, bot, config):
        """
        Creates a poll based on the provided arguments.

        Args:
            room (botlib.Room): The room where the poll is created.
            match (botlib.MessageMatch): The matched message object with arguments.
            bot (botlib.Bot): The bot instance.
        """
        # Ensure the message contains arguments
        if not match.args():
            await handle_error(bot, room, match.event, config)
            return

        # Create a poll title from the message arguments
        title = ' '.join(match.args())

        # Create a new poll object
        poll = Poll(id=len(active_polls), name=title, room=room, item_entries=[])

        # Add the poll to active polls
        active_polls.append(poll)
        logger.info(f"Poll created: {poll}")

        # Send a confirmation message to the room
        await bot.api.send_markdown_message(room.room_id, f"## Poll Created: {title}")

    @staticmethod
    def get_active_poll(room_id: str) -> Poll | None:
        """Retrieve the active poll in the given room, if any."""
        return next((poll for poll in active_polls if poll.room.room_id == room_id), None)

    @staticmethod
    async def close_poll(bot, room_id: str) -> None:
        """Close and remove a poll."""
        poll = PollManager.get_active_poll(room_id)
        if poll is None:
            logger.warn("No pol found to close")
            return

        markdown = poll.formatted_markdown(f"## {poll.name}")
        await bot.api.send_markdown_message(room_id, markdown)
        active_polls.remove(poll)
        logger.info(f"Poll closed: {poll}")

    @staticmethod
    async def add_item(room, message, match, bot, config):
        """Add an item to an active poll."""
        poll = PollManager.get_active_poll(room.room_id)
        if not poll:
            return

        body_msg = ' '.join(match.args()).strip() if config["use_add_command"] else message.body.strip()
        if not body_msg:
            return

        quantity_num, item_name = get_quantity_number(body_msg)
        count = quantity_num or config["default_quantity_number"]
        item_name = item_name or body_msg
        sender_name = await PollManager.get_sender_name(bot, message.sender)

        poll.add_response(item_name, sender_name, count)
        await bot.api.send_reaction(room.room_id, message, config["reaction"]["success"])
        logger.info(f"Added item '{item_name}' with quantity {quantity_num}")

    @staticmethod
    async def get_sender_name(bot, sender: str) -> str:
        """Retrieve the display name of the message sender."""
        displayname_response = await bot.async_client.get_displayname(sender)
        return displayname_response.displayname

    @staticmethod
    async def list_items(room, match, bot):
        """List all items in an active poll."""
        poll = PollManager.get_active_poll(room.room_id)
        if not poll:
            return

        markdown = poll.formatted_markdown(f"## {poll.name}")
        await bot.api.send_markdown_message(room.room_id, markdown)
        logger.info("Listed poll items")

    @staticmethod
    async def remove_item(bot, room, message, match, config):
        """Remove an item from an active poll."""
        poll = PollManager.get_active_poll(room.room_id)
        if not poll or not match.args():
            await handle_error(bot, room, message, config)
            return

        body_msg = ' '.join(match.args()).strip()
        quantity_num, item_name = get_quantity_number(body_msg)
        count = quantity_num or config["default_quantity_number"]
        item_name = item_name or body_msg

        item = poll.get_item(item_name)
        msg_sender = await PollManager.get_sender_name(bot, message.sender)

        if not item or msg_sender not in item.user_count or count > item.user_count[msg_sender]:
            await handle_error(bot, room, message, config)
            return

        item.decrease(msg_sender, count)
        if not item.user_count:
            poll.remove_item(item)

        await bot.api.send_reaction(room.room_id, message, config["reaction"]["removed"])
        logger.info(f"Removed item '{item_name}' with quantity {quantity_num}")
