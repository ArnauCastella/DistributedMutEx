

class LamportClock:

    def __init__(self):
        self.clock = 1

    def tick(self):
        self.clock += 1

    def get_clock(self):
        return self.clock

    def receive_action(self, ts):
        self.clock = max(self.clock, ts) + 1
