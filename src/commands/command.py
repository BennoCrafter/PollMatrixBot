from abc import ABC, abstractmethod
import simplematrixbotlib as botlib
from src.utils.load_config import load_config
from src.bot_instance import get_bot
from src.poll_manager import PollManager
from nio.events.room_events import RoomMessageText
from src.utils.logging_config import setup_logger


class Command(ABC):
    def __init__(self, trigger_names: list[str]) -> None:
        self.trigger_names = trigger_names

        # constants
        self.config = load_config("assets/config.yaml")
        self.bot = get_bot()
        self.poll_manager = PollManager()
        self.logger = setup_logger(__name__)


    def is_valid(self, match: botlib.MessageMatch) -> bool:
        command = match.event.body[len(match._prefix):].split()[0]
        return command in self.trigger_names

    def load(self) -> None:
        ...

    @abstractmethod
    async def execute(self, message: botlib.MessageMatch, **kwargs) -> None:
        raise NotImplementedError("execute must be implemented by subclasses")
