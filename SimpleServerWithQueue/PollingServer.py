import numpy as np
import boto3
import requests

import socket
from _thread import *
import threading

import json
import time

sqs = boto3.client('sqs')
elb = boto3.client('elbv2')
inqueue_url = 'https://sqs.us-east-2.amazonaws.com/489788818582/in'
outqueue_url = 'https://sqs.us-east-2.amazonaws.com/489788818582/out'
url     = 'http://ec2-3-134-94-199.us-east-2.compute.amazonaws.com:80/predict'
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
    # global url
    # global headers
    # global inqueue_url
    response = elb.describe_target_health(
        TargetGroupArn='arn:aws:elasticloadbalancing:us-east-2:489788818582:targetgroup/TestingScaling/63da8e21b92317bb',
    )
    for tar in response['TargetHealthDescriptions']:
        if tar['TargetHealth']['State'] == 'healthy':
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
                VisibilityTimeout=10, # prevent other threads to check this infomation.
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
            print(response)
            # SendMSG(message['MessageAttributes']['REQid'], "request(url, message['Body'], headers)")
            SendMSG(message['MessageAttributes']['REQid'], request(url, message['Body'], headers))
            break;



if __name__ == '__main__':
    while True:
        time.sleep(0.2) # don't make too much threads
        # RecvMSG()       #
        threading.Thread(target=RecvMSG, args=()).start()
