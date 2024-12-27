from abc import ABC, abstractmethod
import simplematrixbotlib as botlib
from src.utils.load_config import load_config


class Command(ABC):
    def __init__(self, trigger_names: list[str]) -> None:
        self.trigger_names = trigger_names

        self.config = load_config("assets/config.yaml")

    def is_valid(self, match: botlib.MessageMatch) -> bool:
        command = match.event.body[len(match._prefix):].split()[0]
        return command in self.trigger_names

    @abstractmethod
    async def execute(self, bot: botlib.Bot, msg_content: str, **kwargs) -> None:
        raise NotImplementedError("execute must be implemented by subclasses")
