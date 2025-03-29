from dataclasses import dataclass
from typing import Optional
import simplematrixbotlib

@dataclass
class CommandStructure:
    command: str
    args_string: Optional[str]
    match: simplematrixbotlib.MessageMatch

    @classmethod
    def from_string(cls, input_text: str, prefix: str, match: simplematrixbotlib.MessageMatch) -> Optional['CommandStructure']:

        if not input_text.startswith(prefix):
            return None

        parts = input_text.split()
        if not parts:
            return None

        command = parts[0][len(prefix):] # remove prefix

        args_string = input_text[len(prefix) + len(command):].strip()
        if not args_string:
            args_string = None

        return cls(command, args_string, match)
