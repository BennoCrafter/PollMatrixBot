
from src.commands.command import Command
from src.command_structure import CommandStructure


class RemoveItemCommand(Command):
    """
    **Remove Item**: Use the `!remove <quantity>x <item>` command to remove an item from the poll.
    """
    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        await self.poll_manager.remove_item(structure)
