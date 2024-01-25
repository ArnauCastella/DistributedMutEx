import time
from communication import Connector
from mutex import Lamport
from mutex import RicartAgrawala


class Lightweight:
    def __init__(self, port, pid):
        self.connector = Connector.Connector()
        self.connector.connect('localhost', port)
        if pid.startswith('A'):
            self.mutex = Lamport.Lamport(self.connector, int(pid[1])-1)
        else:
            self.mutex = RicartAgrawala.RicartAgrawala(self.connector, int(pid[1])-1)
        self.id = pid

    def wait_heavyweight(self):
        while True:
            if self.connector.receive_message() == "START":
                break

    def notify_heavyweight(self):
        self.connector.send_message("DONE")

    def start(self):
        while True:
            print("Waiting heavyweight")
            self.wait_heavyweight()
            print("Requesting CS")
            self.mutex.request_cs()
            for i in range(10):
                print(f"I'm lightweight process {self.id}")
                time.sleep(1)
            print("Releasing CS")
            self.mutex.release_cs()
            self.notify_heavyweight()

"""
while (1) {
    waitHeavyWeight();
    requestCS();
    for (int i=0; i<10; i++){
        printf("I'm lightweight process %s\n", myID);
        waitSecond();
    }
    releaseCS();
    notifyHeavyWeight();
}
"""