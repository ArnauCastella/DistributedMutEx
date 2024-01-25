import constants


class DirectClock:

    def __init__(self, pid):
        self.id = pid
        self.clock = []
        for i in range(constants.NUM_LIGHTWEIGHTS):
            self.clock.append(0)
        self.clock[pid] = 1

    def tick(self):
        self.clock[self.id] += 1

    def get_clock(self, pid):
        return self.clock[pid]

    def receive_action(self, src, ts):
        self.clock[src] = max(self.clock[src], ts)
        self.clock[self.id] = max(self.clock[self.id], ts) + 1
