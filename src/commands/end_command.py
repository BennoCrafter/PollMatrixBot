from src.commands.command import Command
import simplematrixbotlib as botlib
from src.utils.load_file import load_file
from src.poll import Poll
from src.poll_manager import PollManager
from nio.events.room_events import RoomMessageText


class EndCommand(Command):
    """
    **Ending a Poll**
    **End a Poll**: Use the `!end dd.mm.yyyy hh:mm` command to configure the end date of a poll.
    """
    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, message: botlib.MessageMatch, **kwargs) -> None:
        await self.poll_manager.update_auto_poll_closing(message)
