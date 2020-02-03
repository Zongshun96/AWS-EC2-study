import numpy as np
import boto3
import requests

import socket
from _thread import *
import threading

import json
import time

sqs = boto3.client('sqs')
inqueue_url = 'https://sqs.us-east-2.amazonaws.com/489788818582/in'
outqueue_url = 'https://sqs.us-east-2.amazonaws.com/489788818582/out'
url     = 'http://test-345378476.us-east-2.elb.amazonaws.com:80/predict'
# payload = '[6.0,  2.2, 4.0,  1.0 ]'
headers = {'Content-Type':'application/json'}
# ClientSockets = {} # size of dict is defined by the number of int

def request(url, payload, headers):
    # start   = time.time()
    res     = requests.post(url, data=payload, headers=headers)
    # end   = time.time()
    print(res.text)
    # print(end - start)
    return res.text


def SendMSG(REQid, reply):
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=outqueue_url,
        DelaySeconds=0,
        MessageAttributes={
            'REQid': REQid
        },
        MessageBody=(
            reply
        )
    )
    print(response['MessageId'])

def RecvMSG():
    # print("!!!!!!!")
    global url
    global headers
    global inqueue_url
    # print("!!!!!!!")
    # while True:
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=inqueue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,  # larger number wait longer. Sth to config !!!!!!!!!!!!!
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0, # don't prevent others to check this infomation.
        WaitTimeSeconds=20   # blocking instead of busy waiting !!!!!!
    )
    # print("????")
    if 'Messages' not in response:
        return
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    print(message)
    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=inqueue_url,
        ReceiptHandle=receipt_handle
    )
    print('Received and deleted message: %s' % message['Body'])
    print(message['MessageAttributes']['REQid']['StringValue'])
    SendMSG(message['MessageAttributes']['REQid'], request(url, message['Body'], headers))
    # c = ClientSockets[message['REQid']]
    # c.send(message['Body'])
    # c.close()


# print_lock = threading.Lock()
# write_lock = threading.Lock()

# thread function
# def PutREQ(c):



if __name__ == '__main__':
    while True:
        time.sleep(0.2)
        start_new_thread(RecvMSG, ())
    # RecvMSG()
    # s.close()
