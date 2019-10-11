import socket

class Server:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.bufferSize = 1024

    def setBufferSize(self, bufferSize):
        self.bufferSize = bufferSize

    def listen(self):
        try:
            data, addr = self.sock.recvfrom(self.bufferSize)
            return data.decode("ascii"), addr
        except:
            return None, None

    def send(self, data, addr):
        self.sock.sendto(data.encode("ascii"), addr)