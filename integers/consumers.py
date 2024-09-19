from random import randint
import json
import time
import socket
from channels.generic.websocket import WebsocketConsumer
from threading import Thread

class WSConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flag = False
        self.readdata = ""
        self.HOST = "192.168.128.3"
        self.PORT = 5005
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))

    def readSocket(self):
        while True:
            try:
                data = self.s.recv(1024)
                if data:
                    print("read", time.time())
                    self.send(json.dumps({"message": data.decode()}))
            except socket.error as e:
                print(f"Socket error: {e}")
                break

    def receive(self, text_data):
        print("hold")
        self.s.send((text_data + "\r\n").encode('utf-8'))
        print("sent", (text_data + "\r\n").encode('utf-8'))

    def connect(self):
        self.accept()
        self.s.send(b'SEC\r\n')
        time.sleep(10)
        self.s.send(b'SEC\r\n')
        Thread(target=self.readSocket, daemon=True).start()
    


    


