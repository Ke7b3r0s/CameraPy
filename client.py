from socket import *
import cv2
import threading
import time
import struct
import pickle

class Video_Client(threading.Thread):
    def __init__(self ,ip, port, version):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = (ip, port)
        if version == 4:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6, SOCK_STREAM)
        self.cap = cv2.VideoCapture(0)
    def __del__(self) :
        self.sock.close()
        self.cap.release()
        # TODO
    def run(self):
        print("client starts...")
        while True:
            try:
                self.sock.connect(self.ADDR)
                break
            except:
                time.sleep(3)
                continue
        print("client connected...")
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            data = pickle.dumps(frame)
            try:
                self.sock.sendall(struct.pack("L", len(data)) + data)
            except:
                break

IP = "192.168.0.185"
PORT = 10087
VERSION = 4

if __name__ == "__main__":
     vclient = Video_Client(IP,PORT,VERSION)
     vclient.run()