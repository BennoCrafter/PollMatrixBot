from datetime import datetime
import datetime
from typing import Optional
import pytz
import asyncio

from src.async_job_scheduler import AsyncJobScheduler
from src.bot_instance import get_bot
from src.poll import Poll
from src.utils.logging_config import setup_logger
from src.utils.get_quantity_number import get_quantity_number
import simplematrixbotlib as botlib
from nio.rooms import MatrixRoom
from nio.events.room_events import RoomMessageText
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
        self.scheduler = AsyncJobScheduler()
        self.active_polls = []

        # todo: load config
        self.config = load_config("assets/config.yaml")

        self.message_reactor = MessageReactor(self.config)

    def schedule_close(self, poll: Poll):
        async def close_wrapper():
            await self.close_poll(poll)

        self.scheduler.add_job(job_id=str(poll.id), run_at=poll.close_date, function=close_wrapper)
        logger.info(f"Scheduled poll '{poll.name}' to close at {poll.close_date}")

    async def close_poll(self, poll: Poll):
        await poll.close_poll()
        self.scheduler.remove_job(poll.name)
        self.active_polls.remove(poll)

    async def create_poll(self, match: botlib.MessageMatch):
        """
        Creates a poll based on the provided arguments.

        Args:
            room (MatrixRoom): The room where the poll is created.
            match (botlib.MessageMatch): The matched message object with arguments.
            bot (botlib.Bot): The bot instance.
            config (dict): Bot configuration dictionary.
        """
        close_date: datetime.datetime | None = None

        # if no args return
        if not match.args():
            await self.message_reactor.error(match.room.room_id, match.event)
            return

        p = self.get_active_poll(match.room.room_id)
        if p is not None:
            await self.close_poll(p)

        # options todo: make func or class for this
        options: list[str] = ' '.join(match.args()).strip().split(",")

        if len(options) < 1:
            logger.warn("Poll needs at least one option (title)")
            await self.message_reactor.error(match.room.room_id, match.event)
            return

        title = options[0]

        if len(options) > 1:
            try:
                close_date = datetime.datetime.strptime(options[1].strip(), self.config.get("date_format", "%H:%M"))
            except ValueError:
                logger.warn(f"Could not parse date: {options[1].strip()}")
                await self.message_reactor.error(match.room.room_id, match.event)
                return

        if close_date is None:
            # if close date is None, close date is set to eob
            close_date = datetime.datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
            if datetime.datetime.now().hour >= 18:
                close_date = close_date + datetime.timedelta(days=1)


        # todo make config
        # Convert to UTC
        local_tz = pytz.timezone("Europe/Berlin")
        close_date = local_tz.localize(close_date)
        logger.info(close_date)


        poll = Poll(id=len(self.active_polls), name=title, close_date=close_date, room=match.room, item_entries=[])

        self.active_polls.append(poll)
        logger.info(f"Poll created: {poll}")
        await poll.list_items(match.room.room_id)
        self.schedule_close(poll)

    def get_active_poll(self, room_id: str) -> Optional[Poll]:
        """Retrieve the active poll in the given room, if any."""
        for poll in self.active_polls:
            if poll.room.room_id == room_id:
                return poll

        return None

    async def update_auto_poll_closing(self, match: botlib.MessageMatch):
        poll = self.get_active_poll(match.room.room_id)
        if not poll:
            await self.message_reactor.error(match.room.room_id, match.event)
            return

        options: list[str] = ' '.join(match.args()).strip().split(",")
        if len(options) < 1:
            return

        close_date: datetime.datetime | None = None
        try:
            close_date = datetime.datetime.strptime(options[0].strip(), self.config.get("date_format", "%H:%M"))
        except ValueError:
            logger.warn(f"Could not parse date: {options[0].strip()}")
            await self.message_reactor.error(match.room.room_id, match.event)
            return


        # todo make config
        # Convert to UTC
        local_tz = pytz.timezone("Europe/Berlin")
        close_date = local_tz.localize(close_date)

        self.scheduler.update_job_time(poll.name, close_date)
        await self.message_reactor.success(match.room.room_id, match.event)
        poll.close_date = close_date
        await poll.update_status_messages()

    async def process_message_items(self, body_msg: str) -> list[tuple[int, str]]:
        """Process message text into list of quantity/item pairs."""
        items = []
        for item in [w.strip() for w in body_msg.split(",")]:
            quantity_num, item_name = get_quantity_number(item)
            count = quantity_num or self.config["default_quantity_number"]
            name = item_name or item
            items.append((count, name))
        return items

    async def add_item(self, match: botlib.MessageMatch):
        """Add an item to an active poll."""
        poll = self.get_active_poll(match.room.room_id)
        if not poll:
            return

        body_msg = ' '.join(match.args()).strip() if self.config["use_add_command"] else match.event.body.strip()
        if not body_msg:
            return

        items = await self.process_message_items(body_msg)
        for count, item_name in items:
            await poll.add_response(item_name, match.event.sender, count)
            logger.info(f"Added item '{item_name}' with quantity {count}")

        await self.message_reactor.success(match.room.room_id, match.event)

    async def list_items(self, match: botlib.MessageMatch):
        """List all items in an active poll."""
        poll = self.get_active_poll(match.room.room_id)
        if not poll:
            await self.message_reactor.error(match.room.room_id, match.event)
            return

        await poll.list_items(match.room.room_id)

    async def remove_item(self, match: botlib.MessageMatch):
        """Remove an item from an active poll."""
        poll = self.get_active_poll(match.room.room_id)
        if not poll or not match.args():
            await self.message_reactor.error(match.room.room_id, match.event)
            return

        body_msg = ' '.join(match.args()).strip()
        items = await self.process_message_items(body_msg)

        for count, item_name in items:
            item = poll.get_item(item_name)
            msg_sender = match.event.sender

            resp = await poll.remove_response(item_name, msg_sender, count)
            if not resp:
                await self.message_reactor.error(match.room.room_id, match.event)
                return

            await self.bot.api.send_reaction(match.room.room_id, match.event, self.config["reaction"]["removed"])
            logger.info(f"Removed item '{item_name}' with quantity {count}")

    async def handle_close_poll(self, room: MatrixRoom) -> bool:
        poll = self.get_active_poll(room.room_id)
        if poll is None:
            return False

        await self.close_poll(poll)
        return True
