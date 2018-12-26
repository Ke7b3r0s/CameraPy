import sys
import time
import argparse
from vchat import Video_Client,Video_Server

parser = argparse.ArgumentParser

# parser.add_argument('--host',type=str,default='127.0.0.1')
# parser.add_argument('--port',type=int,default=10087)
# parser.add_argument('-v','--version',type=int,default=4)

# args = parser.parse_args()

# IP = args.host
# PORT = args.port
# VERSION = args.version
IP = '127.0.0.1'
PORT = 10087
VERSION = 4

if __name__ == '__main__':
    vclient = Video_Client(IP,PORT,VERSION)
    vserver = Video_Server(PORT,VERSION)
    vclient.start()
    time.sleep(1)
    vserver.start()
    while True:
        time.sleep(1)
        if not vserver.isAlive() or not vclient.isAlive():
            print ("Connection Failed!")
            sys.exit(0)