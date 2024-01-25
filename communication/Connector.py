import socket


class Connector:
    def __init__(self, server_socket=None):
        self.server_socket = server_socket
        self.client_socket = None
        self.incoming = None
        self.out = None

    def accept_connection(self):
        try:
            self.client_socket, _ = self.server_socket.accept()
            self.out = self.client_socket.makefile(mode='w')
            self.incoming = self.client_socket.makefile(mode='r')
        except IOError as e:
            print("Error opening connection")
            print(e)

    def connect(self, ip, port):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip, port))
            self.out = self.client_socket.makefile(mode='w')
            self.incoming = self.client_socket.makefile(mode='r')
        except IOError as e:
            print(f"Error connecting to {ip}:{port}")
            print(e)

    def receive_message(self):
        try:
            return self.incoming.readline().strip()
        except IOError as e:
            print(e)

    def send_message(self, message):
        self.out.write(message + '\n')
        self.out.flush()
