from nio.events.room_events import RoomMessageText
from src.commands.command import Command
import simplematrixbotlib as botlib
from src.utils.load_file import load_file
from src.poll import Poll
from src.poll_manager import PollManager
from pathlib import Path


class ReleaseNotesCommand(Command):
    """
    **Release Notes**
    **Release Notes**: Use the `!releasenotes` command to view the release notes for the current version.
    """

    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, message: botlib.MessageMatch, **kwargs) -> None:
        release_notes_folder = Path("./release_notes")
        release_notes_files = sorted(release_notes_folder.glob("v*.md"))
        latest_release_note = release_notes_files[-1] if release_notes_files else None

        if not latest_release_note:
            return

        with open(latest_release_note, 'r') as f:
            release_notes_content = f.read()

        await self.bot.api.send_markdown_message(message.room.room_id, release_notes_content)
