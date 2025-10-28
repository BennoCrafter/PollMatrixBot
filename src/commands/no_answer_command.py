from src.commands.command import Command
from src.command_structure import CommandStructure


class NoAnswerCommand(Command):
    """
    **No Answer**: Use the `!no` command to indicate that you won't be joining the poll.
    """

    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        p = self.poll_manager.get_active_poll(structure.match.room.room_id)

        if p is None:
            # when no poll is active react with error
            await self.poll_manager.message_reactor.error(
                structure.match.room.room_id, structure.match.event
            )
            return

        await p.add_passive_participant(structure.match.event.sender)
