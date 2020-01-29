import requests
import time

url     = 'http://ec2-18-216-227-29.us-east-2.compute.amazonaws.com:80/predict'
payload = '[6.0,  2.2, 4.0,  1.0 ]'
headers = {'Content-Type':'application/json'}
start   = time.time()
res     = requests.post(url, data=payload, headers=headers)
end   = time.time()
print(res.text)
print(end - start)
