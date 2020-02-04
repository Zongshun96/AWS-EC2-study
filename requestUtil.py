import requests
url='http://ec2-3-134-94-199.us-east-2.compute.amazonaws.com:80/predict'
headers = {'Content-Type':'application/json'}
payload = '[6.0,  2.2, 4.0,  1.0 ]'
def request():
    # start   = time.time()
    res     = requests.post(url, data=payload, headers=headers)
    # end   = time.time()
    # print(res.text)
    temp = res.json()
    print(temp['body'])
    # print(end - start)
    # return temp.attributes

if __name__ == '__main__':
    request()
