import constants
from mutex import TokenManager
from communication import Connector
from _thread import *
import json
import time


class Heavyweight:

    def __init__(self, connector, has_token):
        self.lightweight_list = {}
        self.connector = connector
        self.token = TokenManager.TokenManager(connector, has_token)
        self.lw_done = 0

    def manage_connection(self, connector):
        while True:
            data = connector.receive_message()
            if data == "DONE":
                self.lw_done += 1
            else:
                data_json = json.loads(data)
                print(data_json)
                if data_json['dest'] == constants.BROADCAST:
                    for _, client in self.lightweight_list.items():
                        if client != connector:
                            client.send_message(data)
                else:
                    self.lightweight_list[data_json['dest']].send_message(data)

    def connect_lightweights(self, server):
        for i in range(constants.NUM_LIGHTWEIGHTS):
            connector = Connector.Connector(server)
            connector.accept_connection()
            self.lightweight_list[i] = connector

            start_new_thread(self.manage_connection, (connector,))

    def start(self):
        while True:
            self.token.request_token()
            print("Token obtained")
            for _, connector in self.lightweight_list.items():
                connector.send_message("START")
            self.lw_done = 0
            while self.lw_done < constants.NUM_LIGHTWEIGHTS:
                pass
            for _, connector in self.lightweight_list.items():
                connector.send_message("STOP")
            self.token.release_token()
            print("Token released")


"""
while (1) {
    while (!token) listenHeavyweight();
    for (int i=0; i<NUM_LIGHTWEIGHTS; i++) {
        sendActionToLightweight();
    }
    while (answersfromLightweigth < NUM_LIGHTWEIGHTS) {
        listenLightweight();
    }
    token=0;
    sendTokenToHeavyweight();
}
"""