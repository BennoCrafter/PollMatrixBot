from abc import ABC, abstractmethod
from src.command_structure import CommandStructure
from src.globals_instance import get_bot, get_openAI_client, get_config
from src.poll_manager import PollManager


class Command(ABC):
    def __init__(self, trigger_names: list[str]) -> None:
        self.trigger_names = trigger_names

        # constants
        self.config = get_config()
        self.bot = get_bot()
        self.openAI_client = get_openAI_client()
        self.poll_manager = PollManager()
        self.prefix = self.config.get("command_prefix", "!")

    def matches(self, command_structure: CommandStructure) -> bool:
        if command_structure.command in self.trigger_names:
            return True
        return False

    def load(self) -> None:
        """Function which gets called before command initialization"""
        ...

    @abstractmethod
    async def execute(self, structure: CommandStructure, **kwargs) -> None:
        raise NotImplementedError("execute must be implemented by subclasses")
