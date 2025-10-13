from src.utils.get_sender_name import get_sender_name
from src.utils.insert_invisible_char import insert_invisible_char


class User:
    def __init__(self, username: str):
        self.username: str = username
        self.has_payed: bool = False

    async def display_name(self) -> str:
        return await get_sender_name(self.username)

    async def formatted_display_name(self) -> str:
        return insert_invisible_char(await get_sender_name(self.username))
