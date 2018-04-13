import logging,socket, time, threading, select


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
        print('Remote Update __del__ called')
        self.stop()

    def kickstartKeepAlive(self):
        logging.info('Starting up keep alive')
        self.keepAlive()

    def keepAlive(self):
        print('keep alive called')
        while self.alive:
            print('%s <keepAlive> thread alive'%threading.get_ident())
            try:
                print('sending message')
                self.socket.send(self.MSG)
                time.sleep(5)
                print('message sent')
            except:
                logging.error('Connection to %s Lost'%self.TCP_IP)

                self.socket.close()
                self.isAlive = False
                return False
        return False


    def getMessages(self):
        #read_list = [self.socket]
        try:
            #read,write,error = select.select(read_list,[],[],1)
            print('%s <listener Thread> alive'%threading.get_ident())

            data = self.socket.recv(self.BUFF)
            print(data.decode())            
            if data == b'CHANGE':
                self.lock.acquire(timeout=2)
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
        self.socket.setblocking(False)
        self.socket.settimeout(6)
        self.keepAliveThread.start()
        loop = True

        while loop:
            loop = self.getMessages()




    def stop(self):
        print('remoteUpdate stop called')
        self.alive = False
        print('self alive is:',self.alive)
        print('closing socke')
        self.socket.close()
        print('deleting socket')
        del self.socket
        print('socket should be deleted')
        del self.keepAliveThread
