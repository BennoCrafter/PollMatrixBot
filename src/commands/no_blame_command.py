from src.command_structure import CommandStructure
from src.commands.command import Command


class NoBlameCommand(Command):
    """
    **No blame**: Use the `!noblame` command to stop being blamed for the current poll.
    """

    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        p = self.poll_manager.get_recent_poll(structure.match.room.room_id)

        if p is None:
            # when no poll is active react with error
            await self.poll_manager.message_reactor.error(
                structure.match.room.room_id, structure.match.event
            )
            return

        p.pay_reminder_enabled = False
        p.stop_pay_reminder()
        await self.poll_manager.message_reactor.success(
            structure.match.room.room_id, structure.match.event
        )
        return
