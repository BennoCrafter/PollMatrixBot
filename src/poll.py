from src.item import Item

class Poll:
    def __init__(self, id, event, room, items):
        self.id = id
        self.event = event
        self.room = room
        self.items = items

    def add_response(self, item_name: str, user: str):
        i_names = [item.name for item in self.items]

        if item_name not in i_names:
            self.items.append(Item(item_name, 0, []))

        self.items[i_names.index(item_name)].add(user)

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
