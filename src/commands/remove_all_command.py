import asyncio
import random

from src.command_structure import CommandStructure
from src.commands.command import Command
from src.const import hawaii_remove_responses
from src.utils.logging_config import setup_logger
from src.utils.pineapple_detection import predict_pineapple

logger = setup_logger(__name__)


class RemoveAllItemsCommand(Command):
    """
    **Remove all Items**: Use the `!removeall` command to remove all items from the poll that you have added.
    """

    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        poll = self.poll_manager.get_active_poll(structure.match.room.room_id)

        if poll is None:
            # when no poll is active
            await self.poll_manager.message_reactor.error(
                structure.match.room.room_id, structure.match.event
            )
            return

        if structure.args_string in self.config.get("commands", []).get(
            "no_answer_command", []
        ):
            await poll.remove_passive_participant(structure.match.event.sender)
            return

        username: str = structure.match.event.sender
        if username is None:
            return

        for item_entry in list(poll.item_entries):
            for user, count in list(item_entry.user_counts):
                if user.username != username:
                    continue

                await poll.remove_response(
                    item_entry.name, user.username, count, send_update=False
                )
                logger.debug(f"Removed item '{item_entry.name}' with quantity {count}")

        await poll.update_status_messages()
        await self.poll_manager.message_reactor.success(
            structure.match.room.room_id, structure.match.event
        )
