import sys
import copy
import random

class Planes:
    def __init__(self, name, timeLeft, order):
        self.name = name
        self.timeLeft = timeLeft
        self.order = order

    def print(self):
        print(self.name + ' ' + str(self.timeLeft))

    def getTimeLeft(self):
        return self.timeLeft

    def getPlaneName(self):
        return self.name

    def decrement(self):
        self.timeLeft -= decrement

    def increment(self):
        self.timeLeft += increment

    def getOrder(self):
        return self.order

def incrementPlanes(list):
    for x in list:
        x.increment()


def decrementPlanes(list):
    for x in list:
        x.decrement()


def popMax(list):
    max = list[0]
    for x in list:
        if max.getTimeLeft() <= x.getTimeLeft():
            max = x
    list.remove(max)
    return max

def checkPlanes(land, comp):
    for plane in land:
        if plane.getTimeLeft() >= 11:
            comp.append(plane)
            land.remove(plane)

def crashed(list):
    for plane in list:
        if plane.getTimeLeft() < 0:
            print(plane.getPlaneName() + " has crashed. It's time was: " + str(plane.getTimeLeft()))
            sys.exit()

# i just keep popping the first element of airHeap until it isnt larger than
# the priority
def prioritize(air, land):
    while airHeap and air[0].getTimeLeft() <= priority:
        for j in range(len(land)):
            if land[j].getTimeLeft() > 4:
                planeA = air[0]
                del air[0]
                planeL = land[j]
                del land[j]
                air.append(planeL)
                land.append(planeA)


#START OF HEAPFUNCTIONS
def parent(parentPosition):
    return parentPosition / 2


def leftChild(leftPosition):
    return leftPosition * 2


def rightChild(rightPosition):
    return (rightPosition * 2) + 1


def Leaf(list, position):
    if position >= (len(list)) // 2 and position <= (len(list)):
        return True
    return False


def swap(list, position1, position2):
    temp = None
    temp = list[position1]
    list[position1] = list[position2]
    list[position2] = temp


def minHeapify(list, position):
    if not Leaf(list, position):
        if list[position].getTimeLeft() > list[leftChild(position)].getTimeLeft() or list[position].getTimeLeft() > list[rightChild(position)].getTimeLeft():
            if list[leftChild(position)].getTimeLeft() < list[rightChild(position)].getTimeLeft():
                swap(list, position, leftChild(position))
                minHeapify(list, leftChild(position))
            else:
                swap(list, position, rightChild(position))
                minHeapify(list, rightChild(position))


def insertElement(list, plane):
    list.append(plane)
    current = len(list)
    while list[current].getTimeLeft() < list[parentPosition(current)].getTimeLeft():
        swap(list, current, parentPosition(current))
        current = parentPosition(current)

def removeElement(list, plane):
    temp = list[0]
    list[0] = list[len(list) - 1]
    minHeapify(list, 0)
    return temp

def buildMinHeap(list):
    for position in range(len(list) // 2, 0, -1):
        minHeapify(list, position)

#END OF HEAPFUNCTIONS

#THIS IS TO GENERATE PLANES
def generatePlanes(amnt=100):
    file = open('PlanesName.txt', 'w')

    for i in range(1, int(amnt) + 1):
        #converts i into a string to concatenate to Plane
        Plane = 'Plane' + str(i)
        timeLeft = random.randint(1, maxTimeLeft)
        finalObj = Plane + ' ' + str(timeLeft) + '\n'
        file.write(finalObj)

    file.close()


#START OF MAIN
#reading from config file
#to set the config file variables
config = open('config.txt', 'r')
fig = config.readlines()
for i in fig:
    if i[0] != '#':
        temp = i.split()
        if temp[0] == "priority":
            #temp[0] is name and temp[1] is the equal
            priority = int(temp[2])
            print('Config File Prioritizing Planes By: ' + str(priority))
        if temp[0] == "landingStripSize":
            landingStripSize = int(temp[2])
            print('Config File Landing Strip Size: ' + str(landingStripSize))
        if temp[0] == "increment":
            increment = int(temp[2])
            print('Config File Incrementing Planes By: ' + str(increment))
        if temp[0] == "decrement":
            decrement = int(temp[2])
            print('Config File Decrementing Planes By: ' + str(decrement))
        if temp[0] == "timeLeft":
            maxTimeLeft = int(temp[2])
            print('Config File Time Left on Planes: ' + str(maxTimeLeft))

user_in = None
while user_in != '0' and user_in != '1':
    user_in = input("Do you want to Generate new Planes? '0' for No, '1' for Yes: ")
    if user_in is '1':
        numOfPlanes = input('Enter amount of planes you would like to generate: ')
        print('GENERATING ' + numOfPlanes + ' PLANES...')
        generatePlanes(numOfPlanes)
    elif user_in is '0':
        print('Generating default number of Planes: 100')
        generatePlanes()
    else:
        print('***INVALID USERINPUT***')


file = open('PlanesName.txt', 'r')
#this stores the return of readlines which is a list
list = file.readlines()

#Using this to store the Plane Objects extracted from list
planeObjects = []

for i in range(len(list)):
    index = 1
    #removes trailing '\n' char from readlines
    list[i] = list[i].strip('\n')
    temp = list[i].split()
    #i just hard coded this because I know what the txt file contains
    #only two strings, name and timeLeft
    planeObjects.append(Planes(temp[0], int(temp[1]), i))


config.close()
#this will be used as the landindstrip can only have 4 or less
landingStrip = []

#got to turn this into a heap
airHeap = []

#this is where planes go when they reach 11
complete = []

#this list will be used as a check at the end
orig = copy.deepcopy(planeObjects)

# index = 0

for planeLanding in planeObjects:
    if(len(landingStrip) < landingStripSize):
        landingStrip.append(planeLanding)
    #if landingStrip is full
    else:
        if planeLanding.getTimeLeft() <= priority:
            alreadyLandedPlane = popMax(landingStrip)
            landingStrip.append(planeLanding)
            airHeap.append(alreadyLandedPlane)
        #if plane's time left > 2
        else:
            airHeap.append(planeLanding)
    incrementPlanes(landingStrip)
    checkPlanes(landingStrip, complete)
    if airHeap:
        decrementPlanes(airHeap)
        prioritize(airHeap, landingStrip)
        crashed(airHeap)
        if len(airHeap) > 2:
            #this gets called at the end of every iteration
            buildMinHeap(airHeap)
    #this is to keep track of the planes
    # if landingStrip:
    #     print('PLANES IN LANDINGSTRIP')
    #     for planes in landingStrip:
    #         planes.print()
    #
    # if airHeap:
    #     print('PLANES IN AIRHEAP')
    #     for planes in airHeap:
    #         planes.print()
    #
    # if complete:
    #     print('PLANES IN COMPLETED')
    #     complete.sort(key=lambda x: x.getOrder())
    #     for planes in complete:
    #         planes.print()
    #
    # print('THIS IS END OF ROUND: ' + str(index))
    # print('--------------------------')
    # index += 1

while airHeap:
    for planeLanding in airHeap:
        if(len(landingStrip) < landingStripSize):
            landingStrip.append(planeLanding)
        #if landingStrip is full
        else:
            if planeLanding.getTimeLeft() <= priority:
                alreadyLandedPlane = popMax(landingStrip)
                landingStrip.append(planeLanding)
                airHeap.append(alreadyLandedPlane)
            #if plane's time left > 2
            else:
                airHeap.append(planeLanding)
        incrementPlanes(landingStrip)
        checkPlanes(landingStrip, complete)
        if airHeap:
            decrementPlanes(airHeap)
            prioritize(airHeap, landingStrip)
            crashed(airHeap)
            if len(airHeap) > 2:
                buildMinHeap(airHeap)

        #this is to keep track of the planes
#         if landingStrip:
#             print('PLANES IN LANDINGSTRIP')
#             for planes in landingStrip:
#                 planes.print()
#
#         if airHeap:
#             print('PLANES IN AIRHEAP')
#             for planes in airHeap:
#                 planes.print()
#
#         if complete:
#             complete.sort(key=lambda x: x.getOrder())
#             print('PLANES IN COMPLETED')
#             for planes in complete:
#                 planes.print()
#
#         print('THIS IS END OF ROUND: ' + str(index))
#         print('--------------------------')
#         index += 1
#
# #this menas that the only planes left are the ones in the landingStrip
if len(landingStrip) <= landingStripSize and not airHeap:
    while landingStrip:
        incrementPlanes(landingStrip)
        checkPlanes(landingStrip, complete)
        # if landingStrip:
        #     print('PLANES IN LANDINGSTRIP')
        #     for planes in landingStrip:
        #         planes.print()

for plane in complete:
    if plane.getTimeLeft() < 11:
        print('FAAAAAILED')
        sys.exit()

if len(orig) == len(complete):
    print('*****SUCCESS*****')
    print(str(len(orig)) + ' Planes were written to "checkPlanes.txt" with their original countnerpart.')

#this writes to output file
output = open('OutPutPlanes.txt', 'w')
output.write('ORIGINAL STATUS ||  FINAL STATUS\n')
for origPlane,completedPlane in zip(orig, complete):
    output.write(origPlane.getPlaneName() + ' ' + str(origPlane.getTimeLeft()) + ' ' + '    ----->  ' + completedPlane.getPlaneName() + ' ' + str(completedPlane.getTimeLeft()) + '\n')

#closes file because no longer need it
file.close()
output.close()
