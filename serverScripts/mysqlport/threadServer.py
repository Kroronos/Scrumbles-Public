import socket, threading, time, select, os
import collections


class dbMonitor:
    def __init__(self):
        self.isDBAltered = {}
        self.lock = threading.Lock()
    def newThread(self,tid):
        self.lock.acquire()
        self.isDBAltered[tid] = [time.time(), False]
        self.lock.release()
    def threadDone(self,tid):
        self.lock.acquire()
        self.isDBAltered.pop(tid,None)
        self.lock.release()

    def altered(self,tid):
        self.lock.acquire()
        self.isDBAltered[tid][1] = True
        self.lock.release()
    def reset(self,tid):
        self.lock.acquire()
        self.isDBAltered[tid][1] = False
        self.lock.release()

    def postChange(self):
        for tid in self.isDBAltered:
            self.isDBAltered[tid][1] = True

    def isAnyThreadChanged(self):
        rv = False
        for tid in self.isDBAltered:
            if self.isDBAltered[tid][1] is True:
                return True
        return False
    def __str__(self):
        return str(self.isDBAltered)


class ThreadedServer(object):
    def __init__(self, port,dbMon):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(0)
        self.sock.bind((socket.gethostname(), self.port))
        self.dbMon = dbMon
        self.lock = threading.Lock()
        self.cv = threading.Condition()
        self.thresh = 0.0001

    def condition_pred(self):
        for tid in self.dbMon.isDBAltered:
            if  time.time() - self.dbMon.isDBAltered[tid][0] < self.thresh:
                return False
            else:
                return True

    


    def listen(self):
        self.sock.listen(100)
        read_list = [self.sock]
        while True:
            read,write,error = select.select(read_list,[],[],1)
            for s in read:
                if s is self.sock:
                    self.lock.acquire()
                    client, address = s.accept()
                    client.settimeout(60)
                    threading.Thread(target = self.listenToClient, args = (client,address)).start()
                    self.lock.release()
    def listenToClient(self, client, address):
        self.dbMon.newThread(threading.get_ident())
        read_list = [client]
        size = 1024
        while True:
            response = b'Ack'
            if self.dbMon.isAnyThreadChanged():
                with self.cv:
                    self.cv.wait_for(self.condition_pred)
                    response = b'CHANGE'
                    try:
                        client.send(response)
                        self.cv.notifyAll()
                    except:
                        client.close()
                        return False
                    self.dbMon.reset(threading.get_ident())


            read,writqcxe,error = select.select(read_list,[],[],1)
            for s in read:
                if s is client:
                    try:
                        data = s.recv(size)
                        if data != b'':
                    
                             s.send(response)
                        else:
                            raise error('Client disconnected')
                    except:
                        client.close()
                        self.dbMon.threadDone(threading.get_ident())
                        return False

        
