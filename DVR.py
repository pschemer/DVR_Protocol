#!/usr/bin/python3
import os
import threading
from node import Node

network = []
N = 5
threads = {}

"""
    TWO TASKS:
    (1) read the network topology from network.txt input file.
    (2) create N threads (one for each node).
"""
def network_init():
    # (1) read the network topology from network.txt input file.
    filepath = 'network.txt'
    try:
        with open(filepath) as fileIn:
            for line in fileIn:
                network.append([int(s) for s in line.split()])
    except:
        # problem with file or network contains non-integer
        print("Problem with file: {}".format(filepath))
        exit()

    # set N based on input / check input is NxN
    N = len(network)
    for i in range(N):
        if len(network[i]) != N:
            print("Network input must be in format NxN")
            exit()

    # (2) create N threads (one for each node).
    threadID = 0
    for i in range(N):
        # Create thread for Node i, pass link weights of neighbors
        thread = Node(network[i], N, threadID)
        threads[threadID] = thread
        threadID += 1
        thread.run()

network_init()

"""
    OUTPUT
"""

round = 0
roundLock = threading.Lock()
exitFlag = 0
updates = []
for j in range(len(threads)):
   updates.append(threads[j].reqUpdates())

while not exitFlag:
    for j in range(len(threads)):
        roundLock.acquire()
        try:
            round += 1
            threads[j].roundStart(round)
        finally:
            roundLock.release()
        for j in range(len(threads)):
            updates[j] = threads[j].reqUpdates()
        if not any(updates):
            exitFlag = 1
            break;

print("\nFinal output:")
for j in range(len(threads)):
    print("Node {} DV = {}".format(threads[j].Name, threads[j].DV))
print(f"Number of rounds till convergance = {round}")

# fin
os._exit(0)
