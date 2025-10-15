from src.commands.command import Command
from src.command_structure import CommandStructure


class ClosePollCommand(Command):
    """
    **Close a Poll**: Use the `!close` command to close a poll.
    """

    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        poll = self.poll_manager.get_active_poll(structure.match.room.room_id)

        if poll is None:
            return

        await poll.close_poll()
