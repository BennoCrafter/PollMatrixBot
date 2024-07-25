class Item:
    def __init__(self, name, count, users) -> None:
        self.name = name
        self.count = count
        self.users = users

    def add(self, user, count=1):
        self.users.append(user)
        self.count += count
