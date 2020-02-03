# import requests
# Import socket module
import socket
import time
import threading

payload = '{"REQ":"[6.0,  2.2, 4.0,  1.0 ]"}'

def request(payload):
    host = '127.0.0.1'
    port = 50000
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    # while True:
    s.send(payload.encode('utf8'))
    data = s.recv(1024)
    print('Received from the server :',str(data.decode('utf8')))
    # ans = input('\nDo you want to continue(y/n) :')
    # if ans == 'y':
    #     continue
    # else:
    #     break
    s.close()

if __name__ == '__main__':
    for i in range(1, 10000000):
        # from time import sleep
        time.sleep(0.2)
        threading.Thread(target=request, args=(payload,)).start()
