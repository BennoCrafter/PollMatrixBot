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
        if not self.poll_manager.recent_polls:
            return

        # last poll with matching room id
        last_poll = self.poll_manager.get_last_closed_poll(structure.match.room.room_id)

        if last_poll is None:
            return

        await last_poll.reopen_poll()
