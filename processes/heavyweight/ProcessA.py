import socket
from communication import Connector
import constants
import Heavyweight

if __name__ == '__main__':
    # Create the socket ProcessB will connect to
    # Used to transfer token
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind(('localhost', constants.PA_PORT))
    socket.listen()
    connector = Connector.Connector(socket)
    connector.accept_connection()

    process = Heavyweight.Heavyweight(connector, True)
    process.connect_lightweights(socket)
    process.start()



