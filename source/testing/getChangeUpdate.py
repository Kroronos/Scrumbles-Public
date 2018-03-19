import socket, time, threading

#this will connect to a remote server on port 5005
#the remote server will send an ack reply on EHLLO
#the remote server will senda change message if there is a change on the
#MySQL Database hosted on the remote server.

#to test, execute this script and then make some change to the database

TCP_IP = '173.230.136.241'
TCP_PORT = 5005
BUFF = 1024
MSG = b'EHLLO'


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

def keepAlive(socket):
    while True:
        try:
            socket.send(MSG)
            time.sleep(5)
        except:
            socket.close()
            return False

threading.Thread(target = keepAlive, args=(s,)).start()

def getMessages():
    for i in range(50):
        try:
            data = s.recv(BUFF)
            print("recieved :", data)
        except:
            s.close()
            return False

getMessages()
s.close()
