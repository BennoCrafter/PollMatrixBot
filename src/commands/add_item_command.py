import random
import asyncio
from src.commands.command import Command
from src.command_structure import CommandStructure
from src.utils.logging_config import setup_logger
from src.const import hawaii_add_responses
from src.utils.pineapple_detection import predict_pineapple

logger = setup_logger(__name__)


class AddCommand(Command):
    """
    **Add Item**: Use the `!lunchy <quantity>x <item>` command to add an item to the poll.
    """

    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        await self.check_triggers(structure)

        poll = self.poll_manager.get_active_poll(structure.match.room.room_id)
        if not poll:
            return

        if structure.args_string is None:
            await self.poll_manager.message_reactor.error(
                structure.match.room.room_id, structure.match.event
            )
            return

        # add passive participant
        if structure.args_string in self.config.get("commands", []).get(
            "no_answer_command", []
        ):
            await poll.add_passive_participant(structure.match.event.sender)
            return

        # dont allow adding active participant if hes already in passive
        if structure.match.event.sender in map(
            lambda x: x.username, poll.passive_participants
        ):
            await self.poll_manager.message_reactor.error(
                structure.match.room.room_id, structure.match.event
            )
            return

        items = await self.poll_manager.process_message_items(structure.args_string)

        for count, item_name in items:
            await poll.add_response(item_name, structure.match.event.sender, count)
            logger.debug(f"Added item '{item_name}' with quantity {count}")

        await self.poll_manager.message_reactor.success(
            structure.match.room.room_id, structure.match.event
        )

    async def check_triggers(self, structure: CommandStructure):
        if structure.args_string is None:
            return

        asyncio.create_task(self._check_pineapple_async(structure))

    async def _check_pineapple_async(self, structure: CommandStructure):
        try:
            if await predict_pineapple(
                self.openAI_client,
                self.config.get("openai_model", ""),
                structure.args_string,
            ):
                logger.info(f"Detected pineapple in '{structure.args_string}'")
                await self.bot.api.send_text_message(
                    structure.match.room.room_id,
                    random.choice(hawaii_add_responses),
                )
        except Exception as e:
            logger.error(f"Error during pineapple detection: {e}")
