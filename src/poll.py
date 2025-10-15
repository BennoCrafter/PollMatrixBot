from src.item import ItemEntry
from src.user import User
import random
from nio import MatrixRoom
from nio.responses import RoomSendResponse
from src.bot_instance import get_bot
from src.utils.logging_config import setup_logger
import markdown
from typing import Any, Optional
from src.utils.load_config import load_config
from enum import Enum
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from src.utils.parse_time import parse_time


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

        self.passive_participants: list[User] = []
        #  List of the !status messages, where all event ids are listed
        self.status_messages: list[str] = []

        self.status: PollStatus = PollStatus.OPEN
        self.bot = get_bot()
        self.config = load_config("assets/config.yaml")

        self.pay_reminder_scheduler = AsyncIOScheduler()
        self.pay_reminder_scheduler.start()
        self.pay_reminder_job_id: Any | None = None

    async def add_response(self, item_name: str, username: str, count: int) -> None:
        user = self.username_to_user(username)
        item_entry = self.get_item(item_name)

        if item_entry:
            item_entry.add(user, count)
        else:
            self.item_entries.append(ItemEntry(item_name, [(user, count)]))

        await self.update_status_messages()

    async def add_passive_participant(self, username: str) -> None:
        if self.username_in_passive_participants(username):
            return

        user = self.username_to_user(username)
        self.passive_participants.append(user)
        await self.update_status_messages()

    def username_in_passive_participants(self, username: str) -> bool:
        return any(user.username == username for user in self.passive_participants)

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

        paying_feature: dict = self.config.get("paying_feature", {})
        if not paying_feature.get("enabled", False):
            return

        # pay reminder feature
        pay_emoji: str = paying_feature.get("emoji", "💸")
        if paying_feature.get("auto_send_emoji", True):
            poll_summary_event_id = self.status_messages[-1]
            if poll_summary_event_id:
                content = {
                    "m.relates_to": {
                        "event_id": poll_summary_event_id,
                        "key": pay_emoji,
                        "rel_type": "m.annotation",
                    }
                }

                resp = await self.bot.async_client.room_send(
                    room_id=self.room.room_id,
                    message_type="m.reaction",
                    content=content,
                )

                if not isinstance(resp, RoomSendResponse):
                    logger.error(f"Failed to send message: {resp}")
                    return

        reminder_delay = paying_feature.get("reminder_delay", "1h")
        reminder_delay_timedelta = parse_time(reminder_delay)
        if reminder_delay_timedelta is None:
            logger.error(
                f"Invalid reminder delay in config: {reminder_delay}  Using default 1 hour"
            )
            reminder_delay_timedelta = timedelta(hours=1)

        run_time = datetime.now() + reminder_delay_timedelta
        job = self.pay_reminder_scheduler.add_job(
            self.send_pay_reminder,
            "date",
            run_date=run_time,
            args=[],
        )
        self.pay_reminder_job_id = job.id
        logger.info(f"Pay reminder job scheduled for {run_time}")

    async def send_pay_reminder(self) -> None:
        not_payed_users = [user for user in self.involved_users if not user.has_payed]
        for user in not_payed_users:
            display_name = await user.display_name()
            content = {
                "msgtype": "m.text",
                "body": (
                    random.choice(
                        [
                            "Hey %s! Why not paying?",
                            "Hey %s! Better watch out, next time you will need to take the orders...",
                            "Ordering but not paying? Boooh %s!",
                            "One blame for %s! Did not payed until now.",
                        ]
                    )
                    % display_name
                ),
            }

            resp = await self.bot.async_client.room_send(
                room_id=self.room.room_id,
                message_type="m.room.message",
                content=content,
            )
            if not isinstance(resp, RoomSendResponse):
                logger.error(f"Failed to send message: {resp}")
                return

            user.pay_reminder_mention_event_id = resp.event_id

        logger.info(
            "Pay reminder sent to the following users:\n"
            + "\n".join([f"- {user.username}" for user in not_payed_users])
        )

    async def reopen_poll(self) -> None:
        if self.status == PollStatus.OPEN:
            await self.bot.api.send_text_message(
                self.room.room_id, "Poll is already open"
            )
            return
        self.status = PollStatus.OPEN
        await self.delete_close_summary(self.room.room_id, self.status_messages[-1])
        await self.list_items(self.room.room_id)
        await self.update_status_messages()
        logger.info(f"Poll reopened: {self}")

        if self.pay_reminder_job_id is None:
            return

        self.pay_reminder_scheduler.remove_job(self.pay_reminder_job_id)
        self.pay_reminder_job_id = None

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
        self.status_messages.append(resp.event_id)

    def get_item(self, item_name: str) -> ItemEntry | None:
        for item_entry in self.item_entries:
            if self.equals(item_entry.name, item_name):
                return item_entry
        return None

    async def remove_item(self, item_entry: ItemEntry) -> None:
        self.item_entries.remove(item_entry)
        await self.update_status_messages()

    async def update_status_messages(self) -> None:
        for event_id in self.status_messages:
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
            await self.bot.async_client.room_send(
                self.room.room_id, "m.room.message", co
            )

    def equals(self, item_name1: str, item_name2: str) -> bool:
        return item_name1.lower() == item_name2.lower()

    async def formatted_markdown(self, title) -> str:
        status = "(closed)" if self.status == PollStatus.CLOSED else ""
        r = f"## {self.name} {status}\n"

        for item_entry in self.sorted_entries():
            r += f"- {item_entry.get_total_count()}x {item_entry.name} ({await item_entry.format_users()})\n"

        # add passive users
        if self.passive_participants:
            r += "\n---\n"
            r += f"Passive Users: {await self.format_passive_users()}\n"
        return r

    async def format_passive_users(self) -> str:
        return ", ".join(
            [
                f"`{await user.formatted_display_name()}`"
                for user in self.passive_participants
            ]
        )

    def sorted_entries(self) -> list[ItemEntry]:
        return sorted(self.item_entries, key=lambda x: x.name)

    async def add_payment_for_user(self, username: str, pay_reaction_event_id: str):
        if self.is_username_involved(username):
            user = self.username_to_user(username)
            user.has_payed = True
            user.pay_reaction_event_id = pay_reaction_event_id

            if user.pay_reminder_mention_event_id is not None:
                # user didnt pay on time
                # delete mention reminder message
                await self.bot.api.redact(
                    self.room.room_id, user.pay_reminder_mention_event_id
                )

            if user.pay_bash_event_id is not None:
                # delete bash message
                await self.bot.api.redact(self.room.room_id, user.pay_bash_event_id)
                user.pay_bash_event_id = None

        else:
            # user who reacted to poll hadnt even added something to the poll
            return

    async def remove_payment_for_user(self, username: str):
        if self.is_username_involved(username):
            user = self.username_to_user(username)
            user.has_payed = False
            user.pay_reaction_event_id = None
        else:
            # user who reacted to poll hadnt even added something to the poll
            return

    async def bash_user_for_not_paying(self, username: str):
        if self.is_username_involved(username):
            user = self.username_to_user(username)
            user.has_payed = False

            reply = random.choice(
                [
                    "You can’t get around paying.",
                    "You can’t dodge the payment.",
                    "Nice try, but the bill always finds you.",
                    "You can run, but you can’t hide from the payment.",
                ]
            )

            display_name = await user.display_name()
            content = {
                "msgtype": "m.text",
                "body": f"{reply} {display_name}",
            }

            resp = await self.bot.async_client.room_send(
                room_id=self.room.room_id,
                message_type="m.room.message",
                content=content,
            )

            if not isinstance(resp, RoomSendResponse):
                logger.error(f"Failed to send message: {resp}")
                return

            user.pay_bash_event_id = resp.event_id

            await self.remove_payment_for_user(user.username)

        else:
            # user who reacted to poll hadnt even added something to the poll
            # this case shouldt happen. checked before in on redact
            return

    def __str__(self) -> str:
        return f"Poll ID = {self.id}, Name = '{self.name}'"
