import requests
import time
import threading

def request(url, payload, headers):
    start   = time.time()
    res     = requests.post(url, data=payload, headers=headers)
    end   = time.time()
    print(res.text)
    print(end - start)

# url     = 'http://CLB-1395665709.us-east-2.elb.amazonaws.com:80/predict'
url     = 'http://test-345378476.us-east-2.elb.amazonaws.com:80/predict'
payload = '[6.0,  2.2, 4.0,  1.0 ]'
headers = {'Content-Type':'application/json'}
for i in range(1, 10000000):
    # from time import sleep
    time.sleep(0.2)
    threading.Thread(target=request, args=(url, payload, headers)).start()
