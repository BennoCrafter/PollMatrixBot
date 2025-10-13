from nio.schemas import UserIdRegex
from src.item import ItemEntry
from src.user import User

from nio import MatrixRoom
from nio.responses import RoomSendResponse
from src.bot_instance import get_bot
from src.utils.logging_config import setup_logger
import markdown
from typing import Optional

from enum import Enum


class PollStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"


logger = setup_logger(__name__)


class Poll:
    def __init__(
        self, id: int, name: str, room: MatrixRoom, item_entries: list[ItemEntry]
    ) -> None:
        self.id: int = id
        self.name: str = name
        self.room: MatrixRoom = room
        self.item_entries: list[ItemEntry] = item_entries
        self.involved_users: list[User] = []
        #  List of the !status messages, where all items are listed --> [{"room_id": room_id, "event_id": event_id}, ...]
        self.status_messages: list[dict] = []

        self.status: PollStatus = PollStatus.OPEN
        self.bot = get_bot()

    async def add_response(self, item_name: str, username: str, count: int) -> None:
        user = self.username_to_user(username)
        item_entry = self.get_item(item_name)

        if item_entry:
            item_entry.add(user, count)
        else:
            self.item_entries.append(ItemEntry(item_name, [(user, count)]))

        await self.update_status_messages()

    async def remove_response(self, item_name: str, username: str, count: int) -> bool:
        if not self.is_username_involved(username):
            return False

        user = self.username_to_user(username)
        item_entry = self.get_item(item_name)

        if (
            item_entry is None
            or (not item_entry.contains_user(user))
            or count > item_entry.get_count_for_user(user)
        ):
            return False

        if item_entry:
            item_entry.decrease(user, count)
            if item_entry.get_total_count() == 0:
                await self.remove_item(item_entry)
            await self.update_status_messages()
            return True
        else:
            logger.warn(f"Could not find item '{item_name}' in poll '{self.name}'")
            return False

    def username_to_user(self, username: str) -> User:
        """Returns the user with the given username, or creates a new one if it doesn't exist."""
        for user in self.involved_users:
            if user.username == username:
                return user
        self.involved_users.append(User(username))
        return self.involved_users[-1]

    def is_username_involved(self, username: str) -> bool:
        """Returns True if the given username is involved in the poll, False otherwise."""
        for user in self.involved_users:
            if user.username == username:
                return True
        return False

    async def close_poll(self) -> None:
        self.status = PollStatus.CLOSED
        await self.list_items(self.room.room_id)
        await self.update_status_messages()
        logger.info(f"Poll closed: {self}")

    async def reopen_poll(self) -> None:
        if self.status == PollStatus.OPEN:
            await self.bot.api.send_text_message(
                self.room.room_id, "Poll is already open"
            )
            return
        self.status = PollStatus.OPEN
        await self.delete_close_summary(
            self.status_messages[-1]["room_id"], self.status_messages[-1]["event_id"]
        )
        await self.list_items(self.room.room_id)
        await self.update_status_messages()
        logger.info(f"Poll reopened: {self}")

    async def delete_close_summary(self, room_id: str, event_id: str) -> None:
        await self.bot.api.redact(room_id, event_id)
        logger.info("Poll closed summary deleted")

    async def list_items(self, room_id: str, title: Optional[str] = None) -> None:
        text = await self.formatted_markdown(title or f"## {self.name}")
        content = {
            "msgtype": "m.text",
            "body": text,
            "format": "org.matrix.custom.html",
            "formatted_body": markdown.markdown(
                text, extensions=["fenced_code", "nl2br"]
            ),
        }
        resp = await self.bot.async_client.room_send(
            room_id=room_id, message_type="m.room.message", content=content
        )
        if not isinstance(resp, RoomSendResponse):
            logger.error(f"Failed to send message: {resp}")
            return
        self.status_messages.append(
            {"room_id": resp.room_id, "event_id": resp.event_id}
        )

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
                "body": "* " + mekr,
                "format": "org.matrix.custom.html",
                "formatted_body": "* "
                + markdown.markdown(mekr, extensions=["fenced_code", "nl2br"]),
                "m.relates_to": {"rel_type": "m.replace", "event_id": event_id},
                "m.new_content": {
                    "msgtype": "m.text",
                    "body": mekr,
                    "format": "org.matrix.custom.html",
                    "formatted_body": markdown.markdown(
                        mekr, extensions=["fenced_code", "nl2br"]
                    ),
                },
            }
            await self.bot.async_client.room_send(room_id, "m.room.message", co)

    def equals(self, item_name1: str, item_name2: str) -> bool:
        return item_name1.lower() == item_name2.lower()

    async def formatted_markdown(self, title) -> str:
        status = "(closed)" if self.status == PollStatus.CLOSED else ""
        r = f"## {self.name} {status}\n"

        for item_entry in self.sorted_entries():
            r += f"- {item_entry.get_total_count()}x {item_entry.name} ({await item_entry.format_users()})\n"
        return r

    def sorted_entries(self) -> list[ItemEntry]:
        return sorted(self.item_entries, key=lambda x: x.name)

    def __str__(self) -> str:
        return f"Poll ID = {self.id}, Name = '{self.name}'"
