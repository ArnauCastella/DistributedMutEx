import constants
from mutex.clocks import LamportClock
import json
from queue import Queue
from _thread import *


class RicartAgrawala:

    def __init__(self, connector, pid):
        self.id = pid
        self.connector = connector
        self.clock = LamportClock.LamportClock()
        self.my_ts = float('inf')
        self.num_okay = 0
        self.pending_q = Queue()
        self.started = False
        start_new_thread(self.handle_messages, ())

    def handle_messages(self):
        while True:
            if self.started:
                data = self.connector.receive_message()
                if data == "STOP":
                    self.started = False
                    continue
                data = json.loads(data)
                self.handle_msg(data['src'], data['tag'], data['ts'])

    def send_message(self, dest, tag, ts):
        data = {'dest': dest, 'src': self.id, 'tag': tag, 'ts': ts}
        self.connector.send_message(json.dumps(data))

    def request_cs(self):
        self.started = True
        self.clock.tick()
        self.my_ts = self.clock.get_clock()
        self.send_message(constants.BROADCAST, "REQUEST", self.my_ts)
        while self.num_okay < constants.NUM_LIGHTWEIGHTS - 1:
            pass
        self.num_okay = 0

    def release_cs(self):
        self.my_ts = float('inf')
        self.clock.tick()
        while not self.pending_q.empty():
            pid = self.pending_q.get()
            self.send_message(pid, "OKAY", self.clock.get_clock())
        self.started = False

    def handle_msg(self, src, tag, ts):
        self.clock.receive_action(ts)
        if tag == "REQUEST":
            if self.my_ts == float('inf') or ts < self.my_ts or (ts == self.my_ts and src < self.id):
                self.send_message(src, "OKAY", self.clock.get_clock())
            else:
                self.pending_q.put(src)
        elif tag == "OKAY":
            self.num_okay += 1
