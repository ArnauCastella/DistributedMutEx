from communication import Connector
import constants
import Heavyweight
import socket

if __name__ == '__main__':
    # Connect to socket created by ProcessA
    connector = Connector.Connector()
    connector.connect('localhost', constants.PA_PORT)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', constants.PB_PORT))
    server.listen()
    process = Heavyweight.Heavyweight(connector, False)
    process.connect_lightweights(server)
    process.start()

