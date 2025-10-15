import random
from src.commands.command import Command
from src.command_structure import CommandStructure


class NoAnswerCommand(Command):
    """
    **No Answer**: Use the `!lunchy no` command to indicate that you won't be joining the poll.
    """

    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        p = self.poll_manager.get_active_poll(structure.match.room.room_id)
        if p is None:
            # no active poll in room
            return

        await p.add_passive_participant(structure.match.event.sender)
