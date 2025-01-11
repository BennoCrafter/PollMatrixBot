from src.utils.logging_config import setup_logger
from src.bot_instance import get_bot
from nio.events import Event
from src.utils.singleton import singleton

@singleton
class MessageReactor:
    def __init__(self, config):
        self.config = config
        self.bot = get_bot()
        self.reactions = config.get("reactions", {})
        self.enabled = self.reactions.get("enabled", True)
        self.reaction_emojis = config.get("types", {})
        self.logger = setup_logger(__name__)

    def is_reaction_enabled(self, reaction_type):
        return self.enabled and self.reactions.get("types", {}).get(reaction_type, {}).get("enabled", True)

    def get_reaction_emoji(self, reaction_type) -> str | None:
        return self.reactions.get("types", {}).get(reaction_type, {}).get("emoji", None)


    async def react(self, room_id: str, event: Event, reaction_type: str):
        if not self.is_reaction_enabled(reaction_type):
            return

        emoji = self.get_reaction_emoji(reaction_type)
        if emoji is None:
            return

        await self.bot.api.send_reaction(room_id, event, emoji)

    async def error(self, room_id: str, event: Event):
        await self.react(room_id, event, "error")

    async def success(self, room_id: str, event: Event):
        await self.react(room_id, event, "success")

    async def removed(self, room_id: str, event: Event):
        await self.react(room_id, event, "removed")
