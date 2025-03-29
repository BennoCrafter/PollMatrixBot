from src.commands.command import Command
import simplematrixbotlib as botlib
from src.utils.load_file import load_file
from nio.events.room_events import RoomMessageText
from src.command_system import command_descriptions
from src.command_structure import CommandStructure

class HelpCommand(Command):
    """
    **Help**: Use the `!help` command to get a list of all available commands.
    """
    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)
        self.help_message = load_file(self.config["help_message_file"])
        self.md = ""

    def load(self):
        self.command_descriptions: dict[str, str] = command_descriptions
        self.md = ""
        for name, des in self.command_descriptions.items():
            self.md += f"**{name}**: {des}\n"

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        await self.bot.api.send_markdown_message(structure.match.room.room_id, self.md)
