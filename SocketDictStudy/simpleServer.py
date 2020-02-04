import socket
from _thread import *
import threading
import time

Sockets={}
count=0

def testing():
    global Sockets
    # time.sleep(10)
    while True:
        time.sleep(0.2)
        for i in range(0, count):
            c = Sockets[i]
            # print(Sockets)
            # data = c.recv(1024)
            print("!!!!!!")
            c.send(("nothing is read").encode('utf8'))
    # c.close()

if __name__ == '__main__':
    # start_new_thread(RecvMSG, ())
    host = ""
    port = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
    s.listen(5)
    print("socket is listening")
    start_new_thread(testing, ())
    while True:
        c, addr = s.accept()
        # start_new_thread(testing, (c,))
        Sockets[count] = c
        count = count + 1
        # print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        # start_new_thread(testing, ())
    s.close()
