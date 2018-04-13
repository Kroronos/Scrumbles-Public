import logging,socket, time, threading


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
        self.keepAliveThread = threading.Thread(target=self.kickstartKeepAlive, name='KeepConnAlive')
        self.lock = threading.Lock()
        self.alive = True


    def __del__(self):
        self.stop()

    def kickstartKeepAlive(self):
        logging.info('Starting up keep alive')
        self.keepAlive()

    def keepAlive(self):

        while self.alive:
            try:
                self.socket.send(self.MSG)
                time.sleep(5)
            except:
                logging.error('Connection to %s Lost'%self.TCP_IP)

                self.socket.close()
                return False
        return False


    def getMessages(self):
        try:
            data = self.socket.recv(self.BUFF)
            
            if data == b'CHANGE':
                self.lock.acquire()
                self.isDBChanged = True
                self.lock.release()
                logging.info('Received Message from DB Server: %s' % data.decode() )
        except:
            logging.error('disconnected from host')
            self.socket.close()
            return False
        return True

    def start(self):
        logging.info('Socket thread %s started' % threading.get_ident())
        logging.info('Connecting to %s on port %s' % (self.TCP_IP,self.TCP_PORT))
        self.conn = self.socket.connect((self.TCP_IP, self.TCP_PORT))
        self.keepAliveThread.start()
        loop = True

        while loop:
            loop = self.getMessages()




    def stop(self):
        self.alive = False
        self.socket.close()
