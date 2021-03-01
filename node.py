import json
import threading
from threading import Thread
from server import MyServer
from client import MyClient

class Node(threading.Thread):

    def __init__(self, dv, n, id):
        threading.Thread.__init__(self)
        self.ID = id
        self.Name = chr(id+65)
        self.N = n
        self.DV = dv
        self.lastDV = []
        self.Neighbors = []
        self.update = True
        self.lock = threading.Lock()

        # Neighbors are nonzero entries in original DV
        for i in range(self.N):
            if dv[i] != 0:
                self.Neighbors.append(chr(65+i))

        # Replace 0's with 999 except self
        for n, i in enumerate(self.DV):
            if i == 0 and n != self.ID:
                self.DV[n] = 999

        # create server socket and add to servers{}
        server = Thread(target = MyServer, args = (self.ID, self, ))
        server.start()


    def sendDV(self):
        self.update = False
        for n in self.Neighbors:
            self.lock.acquire()
            try:
                print("\nSending DV to node {}".format(n))
                client = Thread(target = MyClient, args = (ord(n)-65, self.DV, ))
                client.start()
                client.join()
            finally:
                self.lock.release()


    def updateDV(self, dv):
        # find neighbor n which sent this update
        for i in range(len(dv)):
            if dv[i] == 0:
                n = chr(i+65)
                break
        neighbor = dv[self.ID]
        # Error checking
        if n not in self.Neighbors or neighbor == 0:
            print("(ERROR)\tNode[{}] received update DV from invalid neighbor [{}]".format(self.Name, n))
            exit()
        # Begin Update
        self.lock.acquire()
        try:
            print("Node {} received DV from {}".format(self.Name, n))
            print("Updating DV matrix at node {}".format(self.Name))
            # Update estimated DV as needed
            for key in range(len(dv)):
                # Ignore path to self
                if key != self.ID:
                    # If new path or shorter path, update DV
                    if neighbor + dv[key] < self.DV[key]:
                        self.DV[key] = neighbor + dv[key]
            # End update
            print("New DV matrix at node {} = {}".format(self.Name, self.DV))
            # Updates if something changed
            if not self.DV == self.lastDV:
                self.update = True
                self.lastDV = self.DV.copy()
        finally:
            self.lock.release()


    def run(self):
        pass


    def roundStart(self, round):
        print("\n-------")
        print(f"Round {round}: {self.Name}")
        print("Current DV matrix = {}".format(self.DV))
        print("Updated from last DV matrix or the same? {}".format('Updated' if self.update else 'Same'))
        if self.update:
            self.sendDV()


    def reqUpdates(self):
        self.lock.acquire()
        try:
            ret = self.update
        finally:
            self.lock.release()
        return ret


    def __str__(self):
        return json.dumps(self.DV)
