from nio.events.room_events import RoomMessageText
from src.commands.command import Command
import simplematrixbotlib as botlib
from src.utils.load_file import load_file
from src.poll import Poll
from src.poll_manager import PollManager
from src.command_structure import CommandStructure


class ClosePollCommand(Command):
    """
    **Closing a Poll**
    **Close a Poll**: Use the `!close` command to close a poll.
    """
    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        await self.poll_manager.handle_close_poll(structure.match.room)
