import numpy as np
import boto3

import socket
from _thread import *
import threading

import json

sqs = boto3.client('sqs')
inqueue_url = 'https://sqs.us-east-2.amazonaws.com/489788818582/in'
outqueue_url = 'https://sqs.us-east-2.amazonaws.com/489788818582/out'
ClientSockets = {} # size of dict is defined by the number of int
REQid = 0

def SendMSG(REQid, REQ):
    # Send message to SQS queue
    global inqueue_url
    response = sqs.send_message(
        QueueUrl=inqueue_url,
        DelaySeconds=0,
        MessageAttributes={
            'REQid': {
                'DataType': 'String',
                'StringValue': str(REQid)
            },
        },
        MessageBody=(
            REQ
        )
    )
    print(response)

def RecvMSG():
    global outqueue_url
    while True:
        # Receive message from SQS queue
        response = sqs.receive_message(
            QueueUrl=outqueue_url,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0, # don't prevent others to check this infomation.
            WaitTimeSeconds=20   # blocking instead of busy waiting
        )
        if 'Messages' not in response:
            continue
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']

        # Delete received message from queue
        sqs.delete_message(
            QueueUrl=outqueue_url,
            ReceiptHandle=receipt_handle
        )
        print('Received and deleted message: %s' % message['Body'])
        c = ClientSockets[message['REQid']] # potentially if this EC2 instance down, this registration won't hold!!!!!!!!!!!!!! Use a DB?
        c.send(message['Body'].encode('utf8'))
        c.close()


# print_lock = threading.Lock()
write_lock = threading.Lock()

# thread function
def PutREQ(c):
    global REQid
    data = c.recv(1024).decode('utf8')     # assume REQ less than 1024 bytes. fitting reqirement of SQS as well
    if not data:
        print('Bye')
        # print_lock.release()
        c.send(("nothing is read").encode('utf8'))
        return
    MSG = json.loads(data)
    print(MSG)
    write_lock.acquire()
    REQid = REQid+1
    ClientSockets[REQid]=c
    write_lock.release()
    SendMSG(REQid, MSG['REQ'])
    # c.close()


if __name__ == '__main__':
    start_new_thread(RecvMSG, ())
    host = ""
    port = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
    s.listen(5)
    print("socket is listening")
    while True:
        c, addr = s.accept()
        # print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        start_new_thread(PutREQ, (c,))
    s.close()
