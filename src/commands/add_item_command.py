
from src.commands.command import Command
import simplematrixbotlib as botlib
from src.utils.load_file import load_file
from src.poll import Poll
from src.poll_manager import PollManager
from nio.events.room_events import RoomMessageText
from src.command_structure import CommandStructure


class AddCommand(Command):
    """
    **Add Item**: Use the `!lunchy <quantity>x <item>` command to add an item to the poll.
    """
    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        await self.poll_manager.add_item(structure)
