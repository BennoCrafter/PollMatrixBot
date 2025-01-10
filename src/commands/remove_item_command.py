from nio.events.room_events import RoomMessageText

from src.commands.command import Command
import simplematrixbotlib as botlib
from src.utils.load_file import load_file
from src.poll import Poll
from src.poll_manager import PollManager


class RemoveItemCommand(Command):
    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, message: botlib.MessageMatch, **kwargs) -> None:
        await self.poll_manager.remove_item(message)
