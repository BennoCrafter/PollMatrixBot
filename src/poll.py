from src.item import Item

class Poll:
    def __init__(self, id, event, room, items):
        self.id = id
        self.event = event
        self.room = room
        self.items = items

    def add_response(self, item_name: str, user: str):
        item = self.get_item(item_name)
        if item:
            item.add(user)
        else:
            self.items.append(Item(item_name, 1, [user]))

    def get_item(self, item_name: str) -> Item:
        i_names = [item.name for item in self.items]
        return self.items[i_names.index(item_name)]

    def formated(self) -> str:
        r = "Poll Results:\n"
        for item in self.items:
            r += f"{item.name}: {item.count}\n"
        return r

    def formated_markdown(self) -> str:
        r = "## Poll Results:\n"
        for item in self.items:
            r += f"- {item.count}x {item.name} ({', '.join(item.users)})\n"
        return r
