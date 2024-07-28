from src.item import ItemEntry
from src.utils.insert_invisible_char import insert_invisible_char


class Poll:
    def __init__(self, id: int, name: str, room, item_entries: list[ItemEntry]) -> None:
        self.id: int = id
        self.name: str = name
        self.room = room
        self.item_entries: list[ItemEntry] = item_entries

    def add_response(self, item_name: str, user: str) -> None:
        item_entry = self.get_item(item_name)
        if item_entry:
            item_entry.add(user, 1)
        else:
            self.item_entries.append(ItemEntry(item_name, {user: 1}))

    def get_item(self, item_name: str) -> ItemEntry | None:
        for item_entry in self.item_entries:
            if self.equals(item_entry.name, item_name):
                return item_entry
        return None

    def remove_item(self, item_entry: ItemEntry) -> None:
        self.item_entries.remove(item_entry)

    def equals(self, item_name1: str, item_name2: str) -> bool:
        return item_name1.lower() == item_name2.lower()


    def formated_markdown(self) -> str:
        r = f"## Shopping list {self.name}:\n"
        for item_entry in self.item_entries:
            r += f"- {item_entry.get_total_count()}x {item_entry.name} {item_entry.format_users()}\n"
        return r
