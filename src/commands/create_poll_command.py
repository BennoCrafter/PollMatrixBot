from nio.events.room_events import RoomMessageText

from src.commands.command import Command
import simplematrixbotlib as botlib
from src.utils.load_file import load_file
from src.poll import Poll
from src.poll_manager import PollManager
from src.command_structure import CommandStructure


class CreatePollCommand(Command):
    """
    **Creating a Poll**
    **Start a Poll**: Use the `!lunchy <name>, <end_date>(optional)` command to start a new poll.
      - Date: hh.mm (24-hour)
      - Example: `!lunchy Eating list 25.1.2025 13.30`
    """

    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        await self.poll_manager.create_poll(structure)
