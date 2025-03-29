from src.commands.command import Command
from src.command_structure import CommandStructure


class ClosePollCommand(Command):
    """
    **Close a Poll**: Use the `!close` command to close a poll.
    """
    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        await self.poll_manager.handle_close_poll(structure.match.room)
