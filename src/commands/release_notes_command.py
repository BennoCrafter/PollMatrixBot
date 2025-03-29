from src.commands.command import Command
from pathlib import Path
from src.command_structure import CommandStructure


class ReleaseNotesCommand(Command):
    """
    **Release Notes**: Use the `!releasenotes` command to view the release notes for the current version.
    """

    def __init__(self, trigger_names: list[str]) -> None:
        super().__init__(trigger_names)

    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        release_notes_folder = Path("./release_notes")
        release_notes_files = sorted(release_notes_folder.glob("v*.md"))
        latest_release_note = release_notes_files[-1] if release_notes_files else None

        if not latest_release_note:
            return

        with open(latest_release_note, 'r') as f:
            release_notes_content = f.read()

        await self.bot.api.send_markdown_message(structure.match.room.room_id, release_notes_content)
