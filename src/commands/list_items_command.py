from src.commands.command import Command
from src.command_structure import CommandStructure


class ListItemsCommand(Command):
    """
    **List Poll Items**: Use the `!status` command to list all items in the poll.
    """

    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        poll = self.poll_manager.get_active_poll(structure.match.room.room_id)

        if not poll:
            await self.poll_manager.message_reactor.error(
                structure.match.room.room_id, structure.match.event
            )
            return

        await poll.list_items(structure.match.room.room_id)
