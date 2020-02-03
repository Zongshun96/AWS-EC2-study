# import requests
# Import socket module
import socket
import time
import threading
import json

payload = '{"REQ":"[6.0,  2.2, 4.0,  1.0 ]"}'

def request(payload):
    host = '127.0.0.1'
    port = 50000
    t1   = time.time()
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    # while True:
    s.send(payload.encode('utf8'))
    data = s.recv(1024)
    # MSG = json.loads(data)
    print('Received from the server: ', data.decode('utf8'))
    t2   = time.time()
    print('turn around time: ', t2-t1)
    s.close()

if __name__ == '__main__':
    for i in range(1, 101):
        # from time import sleep
        time.sleep(0.2)
        threading.Thread(target=request, args=(payload,)).start()
