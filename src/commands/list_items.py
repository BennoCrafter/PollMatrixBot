
from src.commands.command import Command
import simplematrixbotlib as botlib
from src.utils.load_file import load_file
from src.poll import Poll
from src.utils.poll_manager import PollManager


class ListItemsCommand(Command):
    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, bot: botlib.Bot, msg_content: str, **kwargs) -> None:
        room = kwargs.get("room")
        match = kwargs.get("match")
        if room is None or match is None:
            return

        # if not match.args():
        #     await handle_error(room, message)
        #     return

        await PollManager.list_items(bot, room, match)