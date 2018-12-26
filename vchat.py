from socket import *
import cv2
import threading
import time
import struct
import pickle
import zlib

class Video_Server(threading.Thread):
    def __init__(self, port, version) :
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = ('', port)
        if version == 4:
            self.sock = socket(AF_INET ,SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6 ,SOCK_STREAM)
    def __del__(self):
        self.sock.close()
        try:
            cv2.destroyALLWindows()
        except:
            pass
        # TODO
    def run(self):
        print("server starts...")
        self.sock.bind(self.ADDR)
        self.sock.listen(1)
        conn, addr = self.sock.accept()
        print("remote client success connected...")
        data = "".encode("utf-8")
        payload_size = struct.calcsize("L")
        cv2.namedWindow('Remote',cv2.WINDOW_NORMAL)
        while True:
            while len(data) < payload_size:
                data += conn.recv(81920)
            packed_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L",packed_size)[0]
            while len(data) < msg_size:
                data += conn.recv(81920)
            zframe_data = data[:msg_size]
            data = data[msg_size:]
            # frame_data = zlib.decompress(zframe_data)
            frame = pickle.loads(zframe_data)
            # print(str(frame))
            cv2.imshow('Remote',frame)
            # if cv2.waitkey(1) & 0xff ==27:
            #     break
            if cv2.waitKey(1) == ord('q'):
                break
        # TODO
 
class Video_Client(threading.Thread):
    def __init__(self ,ip, port, version):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = (ip, port)
        self.fx = 0.5
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
            sframe = cv2.resize(frame,(0,0),fx=self.fx,fy=self.fx)
            data = pickle.dumps(frame)
            # zdata = zlib.compress(data,zlib.Z_BEST_COMPRESSION)
            try:
                self.sock.sendall(struct.pack("L", len(data)) + data)
            except:
                break
            # for i in range(1):
            #     self.cap.read(1)
        # TODO