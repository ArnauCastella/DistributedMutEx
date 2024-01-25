from mutex.clocks import DirectClock
import constants
from _thread import *
import json
from threading import Event


def is_greater(entry1, pid1, entry2, pid2):
    if entry2 == float('inf'):
        return False
    return (entry1 > entry2) or ((entry1 == entry2) and (pid1 > pid2))


class Lamport:

    def __init__(self, connector, pid):
        self.connector = connector
        self.id = pid
        self.clock = DirectClock.DirectClock(pid)
        self.queue = []
        self.num_okay = 0
        self.started_event = Event()
        for i in range(constants.NUM_LIGHTWEIGHTS):
            self.queue.append(float('inf'))
        start_new_thread(self.handle_messages, ())

    def handle_messages(self):
        while True:
            self.started_event.wait()
            data = self.connector.receive_message()
            if data == "STOP":
                self.started_event.clear()
                continue
            try:
                data = json.loads(data)
                self.handle_msg(data['src'], data['tag'], data['ts'])
            except json.JSONDecodeError as e:
                print(data)

    def send_message(self, dest, tag, ts):
        data = {'dest': dest, 'src': self.id, 'tag': tag, 'ts': ts}
        self.connector.send_message(json.dumps(data))

    def okay_cs(self):
        if self.num_okay < constants.NUM_LIGHTWEIGHTS - 1:
            return False
        for i in range(constants.NUM_LIGHTWEIGHTS):
            if is_greater(self.queue[self.id], self.id, self.queue[i], i):
                return False
            if is_greater(self.queue[self.id], self.id, self.clock.get_clock(i), i):
                return False
        return True

    def request_cs(self):
        self.started_event.set()
        self.clock.tick()
        self.queue[self.id] = self.clock.get_clock(self.id)
        self.send_message(constants.BROADCAST, "REQUEST", self.queue[self.id])
        while not self.okay_cs():
            pass

    def release_cs(self):
        self.started_event.clear()
        self.clock.tick()
        self.queue[self.id] = float('inf')
        self.send_message(constants.BROADCAST, "RELEASE", self.clock.get_clock(self.id))
        self.num_okay = 0

    def handle_msg(self, src, tag, ts):
        self.clock.receive_action(src, ts)
        if tag == "REQUEST":
            self.queue[src] = ts
            self.send_message(src, "ACK", self.clock.get_clock(self.id))
        elif tag == "ACK":
            self.num_okay += 1
        elif tag == "RELEASE":
            self.queue[src] = float('inf')
