from src.commands.command import Command
from src.command_structure import CommandStructure


class ReopenPollCommand(Command):
    """
    **Reopen a Poll**: Use the `!reopen` command to reopen the last closed poll.
      - Example: `!reopen`
    """

    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        await self.poll_manager.reopen_poll()
