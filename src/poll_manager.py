from typing import Optional
from collections import deque
from src.globals_instance import get_bot
from src.poll import Poll, PollStatus
from src.utils.logging_config import setup_logger
from src.utils.get_quantity_number import get_quantity_number
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

    def get_last_closed_poll(self, room_id: str) -> Optional[Poll]:
        """Retrieve the most recent closed poll in the given room, if any."""
        for poll in reversed(self.recent_polls):
            if poll.room.room_id == room_id and poll.status == PollStatus.CLOSED:
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
