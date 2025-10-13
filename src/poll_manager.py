from typing import Optional
from collections import deque
import random
from src.command_structure import CommandStructure
from src.bot_instance import get_bot
from src.poll import Poll, PollStatus
from src.utils.logging_config import setup_logger
from src.utils.get_quantity_number import get_quantity_number
import simplematrixbotlib as botlib
from nio.rooms import MatrixRoom
from src.utils.load_config import load_config
from src.message_reactor import MessageReactor

from src.utils.singleton import singleton

# Setup logger
logger = setup_logger(__name__)


@singleton
class PollManager:
    def __init__(self):
        logger.info("Initializing PollManager")
        self.bot = get_bot()
        self.recent_polls: deque[Poll] = deque(maxlen=10)

        # todo: load config
        self.config = load_config("assets/config.yaml")

        self.message_reactor = MessageReactor(self.config)

    async def reopen_poll(self, message_match: botlib.MessageMatch):
        if not self.recent_polls:
            logger.warning("No poll to reopen")
            return

        # last poll with matching room id
        last_poll = None

        for poll in reversed(self.recent_polls):
            if poll.room.room_id == message_match.room.room_id:
                last_poll = poll
                break

        if last_poll is None:
            logger.warning(
                f"No recent poll found in room {message_match.room.room_id} to reopen."
            )
            return

        await last_poll.reopen_poll()

    async def create_poll(self, structure: CommandStructure):
        """
        Creates a poll based on the provided arguments.

        Args:
            room (MatrixRoom): The room where the poll is created.
            match (botlib.MessageMatch): The matched message object with arguments.
            bot (botlib.Bot): The bot instance.
            config (dict): Bot configuration dictionary.
        """
        title = structure.args_string
        if title is None:
            logger.warning("Poll needs at least one option (title)")
            await self.message_reactor.error(
                structure.match.room.room_id, structure.match.event
            )
            return

        p = self.get_active_poll(structure.match.room.room_id)
        if p is not None:
            await p.close_poll()

        poll = Poll(
            id=random.randint(1, 1000000),
            name=title,
            room=structure.match.room,
            item_entries=[],
        )

        # self.active_polls.append(poll)
        self.recent_polls.append(poll)
        logger.info(f"Poll created: {poll}")
        await poll.list_items(structure.match.room.room_id)

    def get_active_poll(self, room_id: str) -> Optional[Poll]:
        """Retrieve the active poll in the given room, if any."""
        for poll in reversed(self.recent_polls):
            if poll.room.room_id == room_id and poll.status == PollStatus.OPEN:
                return poll

        return None

    def get_recent_poll(self, room_id: str) -> Optional[Poll]:
        """Retrieve the most recent poll in the given room, if any. This means the poll can be active or closed."""
        for poll in reversed(self.recent_polls):
            if poll.room.room_id == room_id:
                return poll

    async def process_message_items(self, body_msg: str) -> list[tuple[int, str]]:
        """Process message text into list of quantity/item pairs. Returns for example: [(2, 'apple'), (3, 'banana')]"""
        items = []
        for item in [w.strip() for w in body_msg.split(",")]:
            quantity_num, item_name = get_quantity_number(item)
            count = quantity_num or self.config["default_quantity_number"]
            name = item_name or item
            items.append((count, name))
        return items

    async def add_item(self, struct: CommandStructure):
        """Add an item to an active poll."""
        poll = self.get_active_poll(struct.match.room.room_id)
        if not poll:
            return

        if struct.args_string is None:
            return

        items = await self.process_message_items(struct.args_string)
        for count, item_name in items:
            await poll.add_response(item_name, struct.match.event.sender, count)
            logger.info(f"Added item '{item_name}' with quantity {count}")

        await self.message_reactor.success(
            struct.match.room.room_id, struct.match.event
        )

    async def list_items(self, match: botlib.MessageMatch):
        """List all items in an active poll."""
        poll = self.get_active_poll(match.room.room_id)
        if not poll:
            await self.message_reactor.error(match.room.room_id, match.event)
            return

        await poll.list_items(match.room.room_id)

    async def remove_item(self, structure: CommandStructure):
        """Remove an item from an active poll."""
        poll = self.get_active_poll(structure.match.room.room_id)
        if not poll or structure.args_string is None:
            await self.message_reactor.error(
                structure.match.room.room_id, structure.match.event
            )
            return

        items = await self.process_message_items(structure.args_string)

        for count, item_name in items:
            msg_sender = structure.match.event.sender

            resp = await poll.remove_response(item_name, msg_sender, count)
            if not resp:
                await self.message_reactor.error(
                    structure.match.room.room_id, structure.match.event
                )
                return

            await self.message_reactor.removed(
                structure.match.room.room_id, structure.match.event
            )
            logger.info(f"Removed item '{item_name}' with quantity {count}")

    async def handle_close_poll(self, room: MatrixRoom) -> bool:
        poll = self.get_active_poll(room.room_id)
        if poll is None:
            return False

        await poll.close_poll()

        return True
