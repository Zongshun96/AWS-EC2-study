#!/usr/bin/env python3
import socket                   # Import socket module
import subprocess
import os
import threading

def Working(conn, addr):
    start_time = time.time()

    data = conn.recv(1024)
    if data :
        print("got data")
        filename = "job" + str(count) + ".zip"
        dirname = "job" + str(count)
        try:
            os.makedirs(dirname)
        except FileExistsError:
            # directory already exists
            bashCommand3 = "rm -fr ./" + dirname
            print (bashCommand3)
            process3 = subprocess.Popen(bashCommand3.split(), stdout=subprocess.PIPE)
            # pass
        f = open(dirname+"/"+filename,'wb')
        while (data):
           f.write(data)
           data = conn.recv(1024)
           if data.decode('utf-8')=="t":
            break
        f.close()

        print('Done recv')

        bashCommand1 = "unzip " + dirname+"/"+filename +" -d ./" + dirname
        bashCommand2 = "bash ./" + dirname + "/run.sh"
        print (bashCommand1)
        print (bashCommand2)
        process1 = subprocess.Popen(bashCommand1.split(), stdout=subprocess.PIPE)
        process2 = subprocess.Popen(bashCommand2.split(), stdout=subprocess.PIPE)
        output, error = process1.communicate()
        output, error = process2.communicate()

        elapsed_time = time.time() - start_time

        if error :
            msg = 'error terminating, ' + error
            conn.send(msg.encode())
            conn.close()
            bashCommand3 = "rm -fr ./" + dirname
            print (bashCommand3)
            process3 = subprocess.Popen(bashCommand3.split(), stdout=subprocess.PIPE)
        else :
            msg = 'Thank you for connecting\n\nthe result is '
            conn.send(msg.encode()+output)
            conn.send("server response time: "+elapsed_time)
            conn.close()
            bashCommand3 = "rm -fr ./" + dirname
            print (bashCommand3)
            process3 = subprocess.Popen(bashCommand3.split(), stdout=subprocess.PIPE)
        count = count+1
        # max count

count = 0

port = 50000                    # Reserve a port for your service every new transfer wants a new port or you must wait.
s = socket.socket()             # Create a socket object
s.bind(('', port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print ('Server listening....')


while True:
    conn, addr = s.accept()     # Establish connection with client.
    print ('Got connection from', addr)
    threading.Thread(Working, (conn, addr)).start()
