from src.utils.insert_invisible_char import insert_invisible_char


class ItemEntry:
    def __init__(self, name, user_count: dict[str, int]) -> None:
        self.name: str = name
        self.user_count: dict[str, int] = user_count

    def add(self, user: str, count: int) -> None:
        if user not in self.user_count:
            self.user_count[user] = 0
        self.user_count[user] += count

    def get(self, user: str) -> int:
        if user not in self.user_count:
            return -1
        return self.user_count[user]

    def remove(self, user: str) -> None:
        if user not in self.user_count:
            return
        self.user_count.pop(user)

    def get_total_count(self) -> int:
        return sum(self.user_count.values())

    def format_users(self) -> str:
        return ', '.join([f"(`{insert_invisible_char(k)}` {v})" for k, v in self.user_count.items()])
