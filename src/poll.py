from src.item import Item
from src.utils.insert_invisible_char import insert_invisible_char


class Poll:
    def __init__(self, id: int, name: str, room, items: list[Item]) -> None:
        self.id: int = id
        self.name: str = name
        self.room = room
        self.items: list[Item] = items

    def add_response(self, item_name: str, user: str) -> None:
        item = self.get_item(item_name)
        if item:
            item.add(user)
        else:
            self.items.append(Item(item_name, 1, [user]))

    def get_item(self, item_name: str) -> Item | None:
        for item in self.items:
            if self.compare(item.name, item_name):
                return item
        return None

    def remove_item(self, item: Item) -> None:
        self.items.remove(item)

    def compare(self, item_name1: str, item_name2: str) -> bool:
        return item_name1.lower() == item_name2.lower()

    def formated(self) -> str:
        r = "Poll Results:\n"
        for item in self.items:
            r += f"{item.name}: {item.count}\n"
        return r

    def formated_markdown(self) -> str:
        r = f"## Shopping list {self.name}:\n"
        for item in self.items:
            r += f"- {item.count}x {item.name} ({', '.join(f"```{insert_invisible_char(u)}```" for u in item.users)})\n"
        return r
