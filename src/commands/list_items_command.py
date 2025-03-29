from nio.events.room_events import RoomMessageText

from src.commands.command import Command
import simplematrixbotlib as botlib
from src.utils.load_file import load_file
from src.poll import Poll
from src.poll_manager import PollManager
from src.command_structure import CommandStructure


class ListItemsCommand(Command):
    """
    **List Poll Items**: Use the `!status` command to list all items in the poll.
    """
    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        await self.poll_manager.list_items(structure.match)
