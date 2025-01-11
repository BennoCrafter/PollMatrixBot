from src.item import ItemEntry
from src.utils.insert_invisible_char import insert_invisible_char
import datetime
from nio import MatrixRoom
import simplematrixbotlib as botlib
from simplematrixbotlib import MessageMatch
from nio.responses import RoomSendResponse
from nio.events import Event
from src.bot_instance import get_bot
from src.utils.logging_config import setup_logger
import markdown
from nio.events.room_events import RoomMessageText
from nio.rooms import MatrixRoom
from typing import Optional

from enum import Enum

class PollStatus(Enum):
    OPEN = 'open'
    CLOSED = 'closed'

logger = setup_logger(__name__)


class Poll:
    def __init__(self, id: int, close_date: datetime.datetime, name: str, room: MatrixRoom,
                 item_entries: list[ItemEntry]) -> None:
        self.id: int = id
        self.name: str = name
        self.close_date = close_date
        self.room = room
        self.item_entries: list[ItemEntry] = item_entries
        # [{"room_id": room_id, "event_id": event_id}, ...]
        self.status_messages: list[dict] = []

        self.status: PollStatus = PollStatus.OPEN
        self.bot = get_bot()

    async def add_response(self, item_name: str, user: str, count: int) -> None:
        item_entry = self.get_item(item_name)
        if item_entry:
            item_entry.add(user, count)
        else:
            self.item_entries.append(ItemEntry(item_name, {user: count}))

        await self.update_status_messages()

    async def remove_response(self, item_name: str, user: str, count: int) -> bool:
        item_entry = self.get_item(item_name)
        if item_entry is None or (user not in item_entry.user_count) or count > item_entry.user_count[user]:
            return False
        if item_entry:
            item_entry.decrease(user, count)
            if not item_entry.user_count:
                await self.remove_item(item_entry)
            await self.update_status_messages()
            return True
        else:
            logger.warn(f"Could not find item '{item_name}' in poll '{self.name}'")
            return False

    async def close_poll(self) -> None:
        self.status = PollStatus.CLOSED
        await self.bot.api.send_markdown_message(self.room.room_id, await self.formatted_markdown(f"## {self.name}"))
        await self.update_status_messages()
        logger.info(f"Poll closed: {self}")

    async def list_items(self, room_id: str, title: Optional[str] = None) -> None:
        text = await self.formatted_markdown(title or f"## {self.name}")
        content = {
                "msgtype": "m.text",
                "body": text,
                "format": "org.matrix.custom.html",
                "formatted_body": markdown.markdown(text,
                                                    extensions=['fenced_code', 'nl2br'])
            }
        resp = await self.bot.async_client.room_send(room_id = room_id, message_type = "m.room.message", content = content)
        if not isinstance(resp, RoomSendResponse):
            logger.error(f"Failed to send message: {resp}")
            return
        self.status_messages.append({"room_id": resp.room_id, "event_id": resp.event_id})

    async def open_poll(self, title: str) -> None:
        self.status = PollStatus.OPEN
        await self.list_items(self.room.room_id, title)

    def get_item(self, item_name: str) -> ItemEntry | None:
        for item_entry in self.item_entries:
            if self.equals(item_entry.name, item_name):
                return item_entry
        return None

    async def remove_item(self, item_entry: ItemEntry) -> None:
        self.item_entries.remove(item_entry)
        await self.update_status_messages()

    async def update_status_messages(self) -> None:
        for msg in self.status_messages:
            event_id = msg.get("event_id", "")
            room_id = msg.get("room_id", "")
            mekr = await self.formatted_markdown(f"## {self.name}")
            co = {
                "msgtype": "m.text",
                "body": "* "+mekr,
                "format": "org.matrix.custom.html",
                "formatted_body": "* "+ markdown.markdown(mekr,
                                                    extensions=['fenced_code', 'nl2br']),
                "m.relates_to": {
                    "rel_type": "m.replace",
                    "event_id": event_id
                },
                "m.new_content": {
                    "msgtype": "m.text",
                    "body": mekr,
                    "format": "org.matrix.custom.html",
                    "formatted_body": markdown.markdown(mekr,
                                                        extensions=['fenced_code', 'nl2br'])
                }
            }
            await self.bot.async_client.room_send(room_id, "m.room.message", co)

    def equals(self, item_name1: str, item_name2: str) -> bool:
        return item_name1.lower() == item_name2.lower()

    async def formatted_markdown(self, title) -> str:
        d = f"until {self.close_date.strftime('%H:%M') if self.close_date.date() == datetime.datetime.now().date() else self.close_date.strftime('%d.%m.%Y %H:%M')}"
        status = "(closed)" if self.status == PollStatus.CLOSED else None
        r = f"## {self.name} {d if status is None else status}\n"

        for item_entry in self.sorted_entries():
            r += f"- {item_entry.get_total_count()}x {item_entry.name} ({await item_entry.format_users()})\n"
        return r

    def sorted_entries(self) -> list[ItemEntry]:
        return sorted(self.item_entries, key=lambda x: x.name)

    def __str__(self) -> str:
        return f"Poll ID = {self.id}, Name = '{self.name}', Close Date = {self.close_date}"
