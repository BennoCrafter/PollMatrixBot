from typing import Optional
from src.utils.get_sender_name import get_sender_name
from src.utils.insert_invisible_char import insert_invisible_char


class User:
    def __init__(self, username: str):
        self.username: str = username
        self.has_payed: bool = False
        # event id where user got mentioned to pay
        self.pay_reminder_mention_event_id: Optional[str] = None
        # has payed reaction event id
        self.pay_reaction_event_id: Optional[str] = None
        # event id where user got bashed after trying to avoid paying
        self.pay_bash_event_id: Optional[str] = None

    async def display_name(self) -> str:
        return await get_sender_name(self.username)

    async def formatted_display_name(self) -> str:
        return insert_invisible_char(await get_sender_name(self.username))
