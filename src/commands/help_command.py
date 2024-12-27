from src.commands.command import Command
import simplematrixbotlib as botlib
from src.utils.load_file import load_file


class HelpCommand(Command):
    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)
        self.help_message = load_file(self.config["help_message_file"])

    async def execute(self, bot: botlib.Bot, msg_content: str, **kwargs) -> None:
        room = kwargs.get("room")
        if room is None:
            return

        await bot.api.send_markdown_message(room.room_id, self.help_message)
