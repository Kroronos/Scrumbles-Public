import socket, time, threading

#this will connect to a remote server on port 5005
#the remote server will send an ack reply on EHLLO
#the remote server will senda change message if there is a change on the
#MySQL Database hosted on the remote server.

#to test, execute this script and then make some change to the database

class RemoteUpdate:
    def __init__(self):
        self.TCP_IP = '173.230.136.241'
        self.TCP_PORT = 5005
        self.BUFF = 1024
        self.MSG = b'EHLLO'
        self.isDBChanged = False

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.keepAliveThread = threading.Thread(target = self.keepAlive, args=())
        self.alive = True

    def __del__(self):

        self.stop()
    def keepAlive(self):
        while self.alive:
            try:
                self.socket.send(self.MSG)
                time.sleep(5)
            except:
                self.socket.close()
                return False
        return False


    def getMessages(self):
        try:
            data = self.socket.recv(self.BUFF)
            
            if data == b'CHANGE':
                self.isDBChanged = True
        except:
            self.socket.close()
            return False
        return True
    def start(self):
        self.conn = self.socket.connect((self.TCP_IP, self.TCP_PORT))
        self.keepAliveThread.start()
        loop = True

        while loop:
            loop = self.getMessages()




    def stop(self):
        self.alive = False
        self.socket.close()

