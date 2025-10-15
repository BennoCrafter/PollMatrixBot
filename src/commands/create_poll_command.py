import random
from src.commands.command import Command
from src.command_structure import CommandStructure
from src.poll import Poll


class CreatePollCommand(Command):
    """
    **Start a Poll**: Use the `!lunchy <name>` command to start a new poll.
      - Example: `!lunchy Eating list`
    """

    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        title = structure.args_string

        if title is None:
            self.logger.warning("Poll needs at least one option (title)")
            await self.poll_manager.message_reactor.error(
                structure.match.room.room_id, structure.match.event
            )
            return

        p = self.poll_manager.get_active_poll(structure.match.room.room_id)
        if p is not None:
            await p.close_poll()

        poll = Poll(
            id=random.randint(1, 1000000),
            name=title,
            room=structure.match.room,
            item_entries=[],
        )

        self.poll_manager.recent_polls.append(poll)
        self.logger.info(f"Poll created: {poll}")
        await poll.list_items(structure.match.room.room_id)
