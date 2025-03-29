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
        await self.poll_manager.add_item(structure)

    async def check_triggers(self, structure: CommandStructure):
        if structure.args_string and "hawaii" in structure.args_string.lower():
            await self.bot.api.send_text_message(structure.match.room.room_id, random.choice(["Yummy! 😋", "Pineapple perfection! 🍍", "Aloha! 🏝️"]))
