import serial
import json

ser = serial.Serial('/dev/ttyACM0',9600)


class Possition:
    x = 0
    y = 0
    limit = 25


class Node:
    front = False
    right = False
    left = False
    back = False
    directions = {'south': {'Right': 'right', "Left": 'left', 'front': 'front', 'back': 'back'},
                  'north': {'Right': 'left', "Left": 'right', 'front': 'back', 'back': 'front'},
                  'west': {'Right': 'back', "Left": 'front', 'front': 'right', 'back': 'left'},
                  'east': {'Right': 'front', "Left": 'back', 'front': 'left', 'back': 'right'}}


    #   north
    # west   east
    #   south
    # matches matrix walls to the ones that the car see: what wall in matrix is cars right wall
    def makeNode(self):
        a = self.directions[pos.direction]['back']
        exec('self.' + a + "=True")
        if m.frontDistance > pos.limit:
            a = self.directions[pos.direction]['front']
            exec('self.' + a + "=True")
        if m.leftDistance > pos.limit:
            a = self.directions[pos.direction]['Left']
            exec('self.' + a + "=True")
        if m.rightDistance > pos.limit:
            a = self.directions[pos.direction]['Right']
            exec('self.' + a + "=True")
        print(pos.x, pos.y, self.right, self.front, self.left)

    def getCarsRight(self):
        a = self.directions[pos.direction]['Right']
        ldic = locals()
        exec('result=self.' + a, globals(), ldic)
        result = ldic['result']
        return result
        
    #    back
    # right  left
    #    front
    # |_|
    # gives a visual representation of the matrix
    
    def __repr__(self):
        x = ""
        if self.right:
            x = x + " "
        else:
            x = x + "|"
        if self.front:
            if self.back:
                x = x + "  "
            else:
                x = x + "￣"
        else:
            if self.back:
                x = x + "__"
            else:
                x = x + "二"
        if self.left:
            x = x + " "
        else:
            x = x + "|"
        return x


class Possition:
    x = 0
    y = 0
    limit = 29
    oldFrontValue = 0  # !!!se allagh k sthn arxh
    oldLeftValue=0
    oldRightValue=0
    counting = 15
    movefinished = True
    referencedistance = 0
    prevNode = Node()
    loopFlag = False
    nodeChangedFlag=False
    oldDirection = 'south'
    direction = 'south'
    directions = {'north': {'Right': 'east', "Left": 'west', 'Opposite': 'south'},
                  'south': {'Right': 'west', "Left": 'east', 'Opposite': 'north'},
                  'west': {'Right': 'north', "Left": 'south', 'Opposite': 'east'},
                  'east': {'Right': 'south', "Left": 'north', 'Opposite': 'west'}}

    #    |
    #    v
    #   north
    # west   east
    #   south

    # changes the direction according to what direction it already was and which way it turned
    def setDirection(self, movement):
        self.direction = self.directions[self.direction][movement]

    # changes the coordinates everytime a Node changes
    def moveNode(self):
        if self.direction == 'south':
            self.y = self.y + 1
        elif self.direction == 'north':
            self.y = self.y - 1
        elif self.direction == 'west':
            self.x = self.x - 1
        elif self.direction == 'east':
            self.x = self.x + 1

    # returns the front difference between two jsons
    def findDifference(self):
        difference = self.oldFrontValue - m.frontDistance
        # if the node just got created or if it turned
        if self.oldFrontValue is 0 or (self.oldDirection is not self.direction): difference = 0
        print('dif', difference)
        return difference

    def howMuchMoved(self):
        self.counting = self.counting + self.findDifference()
        self.oldFrontValue = m.frontDistance
        self.oldLeftValue = m.leftDistance
        self.oldRightValue = m.rightDistance
        print('has moved:', self.counting)

    # we check if node changed then we change x,y , find out new walls/openings
    def checkifNodeChanged(self):
        self.nodeChangedFlag = False
        if self.counting >= 30 :
            flag = True
            self.loopFlag = False
            self.prevNode = maze[self.y][self.x]
            self.moveNode()
            maze[self.y][self.x].makeNode()
            self.counting = 15
            self.nodeChangedFlag=True


class Metrics:
    rightDistance = 0
    frontDistance = 0
    leftDistance = 0
    code = 0  # code0:forward()    1:turnR()   2:turnL()   3:turnAround()   3:break()
    codedict = {"forward": 0, "turnR": 1, "turnL": 2, "turnAround": 3, "break": 4}
    labelRD = "rightDistance"
    labelFD = "frontDistance"
    labelLD = "leftDistance"

    def fromDict(self, d):
        self.leftDistance = d[self.labelLD]
        self.frontDistance = d[self.labelFD]
        self.rightDistance = d[self.labelRD]

    def toDict(self):
        dict = {}
        dict[self.labelRD] = self.rightDistance
        dict[self.labelFD] = self.frontDistance
        dict[self.labelLD] = self.leftDistance
        return dict

    def codeToDict(self):
        dict = {}
        dict["code"] = self.code
        return dict

    def toString(self):
        return (self.labelRD + " " + str(self.rightDistance) + " " + self.labelFD + " " +
                str(self.frontDistance) + " " + self.labelLD + " " + str(self.leftDistance))

def readJson(myjson):
        x1=myjson.split('{')
        x2=x1[1].split('}')
        x="{"+x2[0]+"}"
        dict = json.loads(x)
        m.fromDict(dict)


def createJson():
    dict = m.codeToDict()
    y = json.dumps(dict)
    return y

def ignoreMetrics():
    flag=False
    if (abs(m.frontDistance-pos.oldFrontValue)>25):
        flag=True
    if (abs(m.leftDistance-pos.oldLeftValue)>25):
        flag=True
    if (abs(m.rightDistance-pos.oldRightValue)>25):
        flag=True
    return flag


#   north
# west   east
#   south
def checkforLoop():
    flag = False
    if pos.prevNode is not []:
        if (pos.prevNode.getCarsRight() is False) and (maze[pos.y][pos.x].getCarsRight() is True):
            print("loop")
            flag = True
    return flag


def moveFinished(lim=0):
    flag = False
    print(m.code)
    # ean perpathse toul 25 ek diesxhse ena node
    if m.code is m.codedict["forward"]:
        if pos.nodeChangedFlag is True:
            flag = True
    # ean h palia de3ia timh plhsiazei to mprostino meros
    if m.code is m.codedict["turnR"]:
        if lim - m.frontDistance < 10:
            flag = True
    # ean h palia aristerh timh plhsiazei to mprostino meros
    if m.code is m.codedict["turnL"]:
        if lim - m.frontDistance < 10:
            flag = True
    # ean h de3ia plhsiazei thn palia aristerh timh
    if m.code is m.codedict["turnAround"]:
        if lim - m.rightDistance < 3:
            flag = True
    print('movedf', flag)
    return flag

# movement logic: where to go      changes direction if needs to      and checks if node is changed
def move():
    pos.howMuchMoved()
    if pos.movefinished is True:
        pos.oldDirection = pos.direction
        if m.rightDistance > pos.limit:
            pos.referencedistance = m.rightDistance
            if pos.nodeChangedFlag is True:
                #you just changed node so you must turn
                if checkforLoop() is True:
                    m.code = m.codedict["turnR"]
                    pos.setDirection('Right')
                else:
                    #you have already turned go ahead
                    m.code = m.codedict["forward"]
        elif m.frontDistance > pos.limit:
            m.code = m.codedict["forward"]
            pos.movefinished = False
        elif m.leftDistance > pos.limit:
            pos.referencedistance = m.leftDistance
            print('lim', pos.referencedistance)
            m.code = m.codedict["turnL"]
            pos.setDirection('Left')
            pos.movefinished = False
        else:
            m.code = m.codedict["turnAround"]
            pos.referencedistance = m.leftDistance
            pos.setDirection('Opposite')
    pos.movefinished = moveFinished(pos.referencedistance)
    pos.checkifNodeChanged()



m=Metrics()
pos = Possition()
h, l = 10, 5
maze = [[[] for x in range(h)] for y in range(l)]
for y in range(l):
    for x in range(h):
        maze[y][x]=Node()

while True:
        try:
                ser.flush()
                read_serial=ser.readline()
                ser.write("a".encode())
                print("print",read_serial)
                read_serial = read_serial.decode('utf-8')
                readJson(read_serial)
                if (ignoreMetrics() is True):
                    print('ignore')
                    continue                
                move()
                y=createJson()
                ser.write(str(y).encode())
                f = open('output.txt', 'w', encoding=('utf-8'))
                for j in maze:
                    print(j)
                    f.write(str(j))
                    f.write('\n\n')
                f.close()
        except:
                pass
