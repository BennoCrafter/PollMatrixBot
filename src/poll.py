class Poll:
    def __init__(self, id, event, room, result={}):
        self.id = id
        self.event = event
        self.room = room
        self.result = result

    def add_response(self, rsp: str):
        if rsp not in self.result:
            self.result[rsp] = 0
        self.result[rsp] += 1

    def formated(self) -> str:
        return "Poll Results:\n" + "\n".join([f"{rsp}: {self.result[rsp]}" for rsp in self.result])

    def formated_markdown(self) -> str:
        return "## Poll Results:\n" + "\n".join([f"- {rsp}: {self.result[rsp]}" for rsp in self.result])
