import random
from src.commands.command import Command
from src.command_structure import CommandStructure


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

        items = await self.poll_manager.process_message_items(structure.args_string)

        for count, item_name in items:
            await poll.add_response(item_name, structure.match.event.sender, count)
            self.logger.debug(f"Added item '{item_name}' with quantity {count}")

        await self.poll_manager.message_reactor.success(
            structure.match.room.room_id, structure.match.event
        )

    async def check_triggers(self, structure: CommandStructure):
        if structure.args_string and "hawaii" in structure.args_string.lower():
            await self.bot.api.send_text_message(
                structure.match.room.room_id,
                random.choice(["Yummy! 😋", "Pineapple perfection! 🍍", "Aloha! 🏝️"]),
            )
