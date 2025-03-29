from nio.events.room_events import RoomMessageText

from src.commands.command import Command
import simplematrixbotlib as botlib
from src.utils.load_file import load_file
from src.poll import Poll
from src.poll_manager import PollManager
from src.command_structure import CommandStructure


class CreatePollCommand(Command):
    """
    **Start a Poll**: Use the `!lunchy <name>` command to start a new poll.
      - Example: `!lunchy Eating list`
    """

    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        await self.poll_manager.create_poll(structure)
