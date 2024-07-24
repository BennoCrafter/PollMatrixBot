class Poll:
    def __init__(self, id, result={})
        self.id = id
        self.result = result
    
    def add_response(self, rsp: str):
        if rsp not in self.result:
            self.result[rsp] = 0
        self.result[rsp] += 1
    
    
    
