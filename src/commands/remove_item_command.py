import random

from src.commands.command import Command
from src.command_structure import CommandStructure
from src.utils.logging_config import setup_logger
from src.const import hawaii_remove_responses

logger = setup_logger(__name__)


class RemoveItemCommand(Command):
    """
    **Remove Item**: Use the `!remove <quantity>x <item>` command to remove an item from the poll.
    """

    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        await self.check_triggers(structure)
        poll = self.poll_manager.get_active_poll(structure.match.room.room_id)

        if not poll or structure.args_string is None:
            # when no poll is active or no arguments are provided react with error
            await self.poll_manager.message_reactor.error(
                structure.match.room.room_id, structure.match.event
            )
            return

        if structure.args_string in self.config.get("commands", []).get(
            "no_answer_command", []
        ):
            await poll.remove_passive_participant(structure.match.event.sender)
            return

        items = await self.poll_manager.process_message_items(structure.args_string)

        for count, item_name in items:
            msg_sender = structure.match.event.sender

            resp = await poll.remove_response(item_name, msg_sender, count)

            if not resp:
                # return with error reaction when e.g. user not involved, or items not exist
                await self.poll_manager.message_reactor.error(
                    structure.match.room.room_id, structure.match.event
                )
                return

            await self.poll_manager.message_reactor.removed(
                structure.match.room.room_id, structure.match.event
            )
            logger.debug(f"Removed item '{item_name}' with quantity {count}")

    async def check_triggers(self, structure: CommandStructure):
        if structure.args_string and "hawaii" in structure.args_string.lower():
            await self.bot.api.send_text_message(
                structure.match.room.room_id,
                random.choice(hawaii_remove_responses),
            )
            return
