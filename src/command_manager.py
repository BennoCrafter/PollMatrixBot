import simplematrixbotlib
from src.commands.command import Command
from typing import Optional
from src.command_structure import CommandStructure
from src.utils.logging_config import setup_logger

logger = setup_logger(__name__)

class CommandManager:
    def __init__(self, commands: list[Command], prefix: str) -> None:
        self.commands = commands
        self.prefix = prefix

    def get_matching_command(self, match: simplematrixbotlib.MessageMatch) -> Optional[tuple[Command, CommandStructure]]:
        inp = match.event.body

        if inp is None:
            logger.warning("Received empty message")
            return

        command_structure = CommandStructure.from_string(inp, self.prefix, match)

        com = self.match_command(command_structure)
        if com is not None and command_structure is not None:
            return com, command_structure

    def match_command(self, command_structure: Optional[CommandStructure]) -> Optional[Command]:
        if command_structure is None:
            return None

        for command in self.commands:
            if command.matches(command_structure):
                return command
        return None
