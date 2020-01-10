#!/usr/bin/env python3
import socket                   # Import socket module

s = socket.socket()             # Create a socket object
host = "ec2-3-15-172-38.us-east-2.compute.amazonaws.com"  #Ip address that the TCPServer  is there
port = 50000                     # Reserve a port for your service every new transfer wants a new port or you must wait.

s.connect((host, port))
# s.send("Hello server!")

filename = input("type in the zipped file name to run")
with open("./"+filename, 'rb') as f:
    print(filename)
    l = f.read(1024)
    while (l):
       s.send(l)
       print('Sent ')
       l = f.read(1024)
       print('read ')
    # conn.send("end\n")
    # f.close()

s.send("t".encode())
# f.close()
print('out f ')
ret = s.recv(1024);
print('got result: ', ret.decode('utf-8'))
s.close()
print('connection closed')
