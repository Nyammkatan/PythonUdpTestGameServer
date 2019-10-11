import socket
from threading import Lock

class Server:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.bufferSize = 1024
        self.lock = Lock()

    def setBufferSize(self, bufferSize):
        self.bufferSize = bufferSize

    def listen(self):
        data, addr = self.sock.recvfrom(self.bufferSize)
        return data.decode("ascii"), addr

    def send(self, data, addr):
        with self.lock:
            self.sock.sendto(data.encode("ascii"), addr)