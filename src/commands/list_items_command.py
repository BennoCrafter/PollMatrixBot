
from src.commands.command import Command
from src.command_structure import CommandStructure


class ListItemsCommand(Command):
    """
    **List Poll Items**: Use the `!status` command to list all items in the poll.
    """
    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        await self.poll_manager.list_items(structure.match)
