# import requests
# Import socket module
import socket
import time
import threading
import json

payload = '{"REQ":"[6.0,  2.2, 4.0,  1.0 ]"}'

def request(payload):
    # host = '127.0.0.1'
    host = 'ec2-3-17-158-199.us-east-2.compute.amazonaws.com'
    port = 50000
    # t1   = time.time()
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))

    t1   = time.time()
    s.send(payload.encode('utf8'))
    data = s.recv(1024)
    # MSG = json.loads(data)
    t2   = time.time()
    print('Received from the server: ', data.decode('utf8'))

    print('turn around time: ', t2-t1)
    s.close()

if __name__ == '__main__':
    for i in range(1, 11):
        # from time import sleep
        time.sleep(0.2)
        threading.Thread(target=request, args=(payload,)).start()
        # request(payload)
