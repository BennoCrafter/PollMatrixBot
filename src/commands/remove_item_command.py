from nio.events.room_events import RoomMessageText

from src.commands.command import Command
import simplematrixbotlib as botlib
from src.utils.load_file import load_file
from src.poll import Poll
from src.poll_manager import PollManager
from src.command_structure import CommandStructure


class RemoveItemCommand(Command):
    """
    **Removing Poll Items**
    **Remove Item**: Use the `!remove <quantity>x <item>` command to remove an item from the poll.
    """
    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        await self.poll_manager.remove_item(structure)
