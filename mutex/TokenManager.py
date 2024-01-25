from _thread import *


class TokenManager:

    def __init__(self, connector, has_token):
        self.has_token = has_token
        self.connector = connector
        start_new_thread(self.manage_token, (connector,))

    def manage_token(self, connector):
        while True:
            msg = connector.receive_message()
            if msg == "RELEASE":
                self.has_token = True

    def request_token(self):
        while not self.has_token:
            pass

    def release_token(self):
        self.connector.send_message("RELEASE")
        self.has_token = False
