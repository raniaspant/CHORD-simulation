from tkinter import *
import numpy as np


def lookup():

    if len(e5.get()) == 0:
        key = 1
    else:
        key = int(e5.get())
    if len(e6.get()) == 0:
        nodeStart = nodes[0]
    else:
        nodeStart = int(e6.get())
    # print(fingerTableSize)
    # print("asked to lookup : ", key)
    nextSuccessor = nodes[0]
    beginWith = nodes.index(nodeStart)
    nextSuccessor = nodes[beginWith]
    j = nodes.index(nodeStart) * M
    path = []
    entries = ""
    flag = 0
    print(fingerTableSize)
    prob = 0
    if key < nodes[beginWith]:
        while key < nextSuccessor and prob == 0:     # if the given key is smaller than the starting node
            path.append(nextSuccessor)
            i = 0
            foundEqual = 0
            while i < M:
                if key == fingerTableSize[j+i][0]:
                    foundEqual = 1
                    entries += "node " + str(int(nextSuccessor)) + " finger table entry : " + str(
                        int(fingerTableSize[j + i][0])) + "|" + str(int(fingerTableSize[j + i][1])) + "\n"
                    nextSuccessor = fingerTableSize[j + i][1]
                i += 1
            if foundEqual == 0:
                entries += "node " + str(int(nextSuccessor)) + " finger table entry : " + str(
                    int(fingerTableSize[j][0])) + "|" + str(int(fingerTableSize[j][1])) + "\n"
                nextSuccessor = fingerTableSize[j][1]
            if nextSuccessor == nodes[0]:       # a whole circle has been completed
                prob = 1
                j = nodes.index(nextSuccessor) * M
                break
            index = nodes.index(nextSuccessor)
            index *= M
            j = index
    prob = 0
    while key > nextSuccessor and prob == 0:

        path.append(nextSuccessor)
        # search from position 0, stop to position + M ( = entries of finger table) for each active node
        i = 0
        # print("NEXT TABLE index = ", j)
        maxTest = 0
        maxPos = -1
        while i < M:
            print(fingerTableSize[j+i][0])
            if fingerTableSize[j+i][0] > maxTest:
                maxTest = fingerTableSize[j+i][0]
                maxPos = j + i
            #print("MAX = ", maxTest)
            if fingerTableSize[j + i][0] == key:
                entries += "node " + str(int(nextSuccessor)) + " finger table entry : " + str(
                    int(fingerTableSize[j + i][0])) + "|" + str(int(fingerTableSize[j + i][1])) + "\n"
                nextSuccessor = fingerTableSize[j + i][1]
                if nextSuccessor == nodes[0]:
                    prob = 1
                    break
                index = nodes.index(nextSuccessor)
                index *= M
                j = index
                break  # get out of the loop
            if fingerTableSize[j + i][0] > key:
                entries += "node " + str(int(nextSuccessor)) + " finger table entry : " + str(
                    int(fingerTableSize[j + i - 1][0])) + "|" + str(int(fingerTableSize[j + i - 1][1])) + "\n"
                nextSuccessor = fingerTableSize[j + i - 1][1]
                if nextSuccessor == nodes[0]:
                    prob = 1
                    break
                index = nodes.index(nextSuccessor)
                index *= M
                j = index
                break  # get out of the loop
            if i == M - 1:
                if key > fingerTableSize[j + i][0]:
                    entries += "node " + str(int(nextSuccessor)) + " finger table entry : " + str(
                        int(fingerTableSize[maxPos][0])) + "|" + str(int(fingerTableSize[maxPos][1])) + "\n"
                    nextSuccessor = fingerTableSize[maxPos][1]
                    if nextSuccessor == nodes[0]:
                        prob = 1
                        break
                    index = nodes.index(nextSuccessor)
                    index *= M
                    j = index
                    break
            i += 1

    path.append(nextSuccessor)
    if flag == 1:
        path.append(nodes[0])
        entries += "final node reached = " + str(int(nodes[0])) + "\n"
    else:
        entries += "final node reached = " + str(int(nextSuccessor)) + "\n"
    var = "Path followed : "
    i = 0
    for item in path:
        if i == 0:
            var += "node " + str(int(item))
        else:
            var += " -> node " + str(int(item))
        i += 1
    #print(var)
    #print(entries)
    Label(master, text=var).grid(row=15, column=10)
    Label(master, text=entries).grid(row=16, column=10)


def sequence():
    # print("X0: %s\nc: %s\nm: %s\nα: %s\n" % (e1.get(), e2.get(), e3.get(), e4.get()))
    x = 1
    c = 0
    m = 32
    a = 5

    if len(e1.get()) == 0:
        x = 1
    else:
        x = int(e1.get())
    if len(e2.get()) == 0:
        c = 0
    else:
        c = int(e2.get())
    if len(e3.get()) == 0:
        m = 32
    else:
        m = int(e3.get())
    if len(e4.get()) == 0:
        a = 5
    else:
        a = int(e4.get())

    allX = []
    while True:
        x = (a * x + c) % m
        if x in allX:
            break
        allX.append(x)

    print(sorted(allX))
    toPrint = str(allX).strip('[]')
    Label(master, text="Active Nodes : " + toPrint).grid(row=8, column=10)
    # this creates a new label to the GUI with the sequence obtained
    # now time for the finger tables. One for each element of the sequence.
    global nodes
    nodes = sorted(allX)                          # uncomment this for proper use
    # nodes = [8, 14, 21, 32, 38, 42, 48, 51, 56]  # use this for debug
    global M
    M = len(str(int(bin(nodes[-1])[2:])))
    global maxNodes
    maxNodes = np.power(2, M)   # number of nodes stored (not only active) in CHORD
    print(maxNodes)
    # each active node has a 2D matrix with 1st column being start and 2nd column being successor.
    global fingerTableSize
    fingerTableSize = np.array([0, 0])
    # throw to garbage the first row
    # each list entry is the finger table of each node
    k = 0
    for item in nodes:  # for each node
        i = 0
        table = np.zeros(shape=(M, 2))
        a1 = 0
        while True:
            if i == M:
                break
            entry = item + np.power(2, i)
            if entry > nodes[-1]:
                if entry >= maxNodes:
                    entry = entry - maxNodes
            flag = 1
            j = 0
            if entry > nodes[0]:
                while entry > nodes[j] and j < len(nodes) - 1:
                    j += 1
            if j == len(nodes) - 1 and entry > nodes[j]:         # go to nodes[0] 'cause we passed the largest node
                j = 0
            initEntry = entry
            while flag == 1:
                if entry < nodes[j]:
                    entry += 1
                else:
                    table[a1][0] = initEntry
                    table[a1][1] = nodes[j]
                    newrow = [table[a1][0], table[a1][1]]
                    fingerTableSize = np.vstack([fingerTableSize, newrow])
                    a1 += 1
                    flag = 0
            i += 1
        # Label(master, text="Node "+ str(nodes[j]) + " finger table").grid(row=9, column=10 + k)
        var = ""

        var = "Node " + str(item) + " finger table\n"
        print(var)
        Label(master, text=var).grid(row=12, column=5 + k)
        var = ""
        for c in range(0, M):
            var += ("| " + str(int(table[c][0])) + "\t\t" + str(int(table[c][1])) + " | \n")
        print(var)
        Label(master, text=var).grid(row=13, column=5 + k)
        k += 1

    # at this point fingerTableSize has all the finger tables of all active nodes
    # start counting from position 1 instead of 0 since the first row is garbage we used to help append rows later on.
    fingerTableSize = np.delete(fingerTableSize, 0, axis=0)

master = Tk()
master.geometry("500x500")

Label(master, text="Seed X0").grid(row=0, column=2)
Label(master, text="Increment c").grid(row=1, column=2)
Label(master, text="Modulus m").grid(row=2, column=2)
Label(master, text="Multiplier α").grid(row=3, column=2)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)
e5 = Entry(master)
e6 = Entry(master)

e1.grid(row=0, column=10)
e2.grid(row=1, column=10)
e3.grid(row=2, column=10)
e4.grid(row=3, column=10)
e5.grid(row=7, column=3)
e6.grid(row=7, column=6)

Button(master, text='Quit', command=master.quit).grid(row=5, column=10, sticky=W, pady=4)
Button(master, text='Calculate Sequence and Show Finger Tables', command=sequence).grid(row=6, column=10, sticky=W, pady=4)
Button(master, text='Lookup', command=lookup).grid(row=7, column=10, sticky=W, pady=4)


mainloop()


