
from src.commands.command import Command
import simplematrixbotlib as botlib
from src.utils.load_file import load_file
from src.poll import Poll
from src.poll_manager import PollManager


class ClosePollCommand(Command):
    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, bot: botlib.Bot, msg_content: str, **kwargs) -> None:
        room = kwargs.get("room")
        if room is None:
            return

        # if not match.args():
        #     await handle_error(room, message)
        #     return

        await PollManager.close_poll(bot, room.room_id)
