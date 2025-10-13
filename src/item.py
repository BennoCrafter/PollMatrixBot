from src.user import User
from typing import Optional


class ItemEntry:
    def __init__(self, name: str, user_counts: list[tuple[User, int]]) -> None:
        self.name: str = name
        self.user_counts: list[tuple[User, int]] = user_counts

    def add(self, user: User, count: int) -> None:
        for i, (u, c) in enumerate(self.user_counts):
            if u == user:
                self.user_counts[i] = (u, c + count)
                return
        self.user_counts.append((user, count))

    def decrease(self, user: User, count: int) -> None:
        for i, (u, c) in enumerate(self.user_counts):
            if u == user:
                self.user_counts[i] = (u, c - count)
                # if count of user <= 0 remove user
                if self.user_counts[i][1] <= 0:
                    self.user_counts.pop(i)
                return

    def get_count_for_user(self, user: User) -> int:
        for u, c in self.user_counts:
            if u == user:
                return c
        return -1

    def remove(self, user: User) -> None:
        for i, (u, c) in enumerate(self.user_counts):
            if u == user:
                self.user_counts.pop(i)
                return

    def get_total_count(self) -> int:
        return sum(c for _, c in self.user_counts)

    def contains_user(self, user: User) -> bool:
        return any(u == user for u, _ in self.user_counts)

    async def format_users(self) -> str:
        return ", ".join(
            [
                f"`{await user.formatted_display_name()}` {quantity}"
                for user, quantity in self.user_counts
            ]
        )
