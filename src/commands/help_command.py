from src.commands.command import Command
import simplematrixbotlib as botlib
from src.utils.load_file import load_file
from nio.events.room_events import RoomMessageText


class HelpCommand(Command):
    """
    **Help**
    **Help**: Use the `!help` command to get a list of all available commands.
    """
    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)
        self.help_message = load_file(self.config["help_message_file"])

    async def execute(self, message: botlib.MessageMatch, **kwargs) -> None:
        await self.bot.api.send_markdown_message(message.room.room_id, self.help_message)
