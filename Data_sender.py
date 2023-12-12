# Server #
import socket

class Server:
    HOST = '0.0.0.0'
    PORT = 14550
    YOUR_DATA = "Hola, todo bien"
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.HOST, self.PORT))

    def accept(self):
        self.sock.listen()
        c, a = self.sock.accept()
        self.rpi = c
        self.send()

    def send(self):
        self.rpi.send(self.YOUR_DATA.encode())

s = Server()

while True:
	s.accept()
	

