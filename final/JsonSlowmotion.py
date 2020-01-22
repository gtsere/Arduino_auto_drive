import json



class Node:
    front = False
    back = False
    right = False
    left = False
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

def ignoreMetrics():
    flag=False
    if (abs(m.frontDistance-pos.oldFrontValue)>25):
        flag=True
    if (abs(m.leftDistance-pos.oldLeftValue)>25):
        flag=True
    if (abs(m.rightDistance-pos.oldRightValue)>25):
        flag=True
    return flag

def readJson(myjson):
    x1 = myjson.split("{")
    x2 = x1[1].split("}")
    x = "{" + x2[0] + "}"
    dict = json.loads(x)
    m.fromDict(dict)


def createJson():
    dict = m.codeToDict()
    y = json.dumps(dict)
    print(y)
    return y


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

    # elif (pos.loopFlag is True):
    #     m.code = m.codedict["forward"]
    # elif(m.code is m.codedict['turnAround']):
    #     m.code = m.codedict["forward"]
    print('direction:', pos.direction)


def main():
    # read_serial = ["{\"frontDistance\":120,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":122,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":117,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":116,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":117,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":115,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":115,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":113,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":112,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":115,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":111,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":110,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":108,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":107,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":108,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":105,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":104,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":104,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":102,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":103,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":102,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":101,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":100,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":99,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":99,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":97,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":95,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":96,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":95,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":94,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":93,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":95,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":94,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":92,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":90,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":89,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":90,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":89,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":87,\"rightDistance\":4,\"leftDistance\":4}'"
    #                "{\"frontDistance\":86,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":85,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":85,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":83,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":82,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":81,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":80,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":75,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":78,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":74,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":72,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":70,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":65,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":64,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":60,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":57,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":54,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":52,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":50,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":52,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":52,\"rightDistance\":4,\"leftDistance\":42}'",
    #                "{\"frontDistance\":51,\"rightDistance\":4,\"leftDistance\":42}'",
    #                "{\"frontDistance\":4,\"rightDistance\":4,\"leftDistance\":42}'",
    #                ]
    """read_serial = ["{\"frontDistance\":70,\"rightDistance\":4,\"leftDistance\":70}'",
                   "{\"frontDistance\":65,\"rightDistance\":4,\"leftDistance\":70}'",
                   "{\"frontDistance\":60,\"rightDistance\":4,\"leftDistance\":70}'",
                   "{\"frontDistance\":55,\"rightDistance\":4,\"leftDistance\":70}'",
                   "{\"frontDistance\":45,\"rightDistance\":4,\"leftDistance\":70}'",
                   "{\"frontDistance\":40,\"rightDistance\":4,\"leftDistance\":4}'",
                   "{\"frontDistance\":10,\"rightDistance\":4,\"leftDistance\":45}'",
                   "{\"frontDistance\":35,\"rightDistance\":4,\"leftDistance\":45}'",
                   "{\"frontDistance\":5,\"rightDistance\":45,\"leftDistance\":4}'",
                   "{\"frontDistance\":34,\"rightDistance\":45,\"leftDistance\":4}'",
                   "{\"frontDistance\":4,\"rightDistance\":45,\"leftDistance\":4}'",

                   ]"""
    # read_serial = ["{\"frontDistance\":65,\"rightDistance\":4,\"leftDistance\":65}'",
    #                "{\"frontDistance\":35,\"rightDistance\":4,\"leftDistance\":4}'",
    #                "{\"frontDistance\":5,\"rightDistance\":4,\"leftDistance\":35}'"
    #                ]
    '''read_serial = ["{\"frontDistance\":65,\"rightDistance\":5,\"leftDistance\":35}'",
                   "{\"frontDistance\":35,\"rightDistance\":5,\"leftDistance\":5}'",
                   "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":35}'",
                   "{\"frontDistance\":35,\"rightDistance\":5,\"leftDistance\":1000}'",
                   "{\"frontDistance\":5,\"rightDistance\":35,\"leftDistance\":5}'",
                   "{\"frontDistance\":35,\"rightDistance\":35,\"leftDistance\":5}'",
                   "{\"frontDistance\":5,\"rightDistance\":35,\"leftDistance\":5}'",
                   "{\"frontDistance\":35,\"rightDistance\":35,\"leftDistance\":5}'",
                   "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":35}'",
                   "{\"frontDistance\":35,\"rightDistance\":5,\"leftDistance\":35}'",
                   "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":35}'",
                   "{\"frontDistance\":125,\"rightDistance\":5,\"leftDistance\":35}'",
                   "{\"frontDistance\":95,\"rightDistance\":5,\"leftDistance\":5}'",
                   "{\"frontDistance\":65,\"rightDistance\":5,\"leftDistance\":5}'",
                   "{\"frontDistance\":35,\"rightDistance\":5,\"leftDistance\":125}'",
                   "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":5}'",
                   "{\"frontDistance\":125,\"rightDistance\":5,\"leftDistance\":5}'",
                   "{\"frontDistance\":95,\"rightDistance\":125,\"leftDistance\":5}'",
                   "{\"frontDistance\":125,\"rightDistance\":35,\"leftDistance\":95}'",
                   "{\"frontDistance\":95,\"rightDistance\":5,\"leftDistance\":125}'",
                   "{\"frontDistance\":65,\"rightDistance\":5,\"leftDistance\":5}'",
                   "{\"frontDistance\":35,\"rightDistance\":5,\"leftDistance\":5}'",
                   "{\"frontDistance\":5,\"rightDistance\":125,\"leftDistance\":5}'",
                   ]'''
    read_serial = [
        "{\"frontDistance\":65,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":14000,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":45,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":25,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":15,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":30,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":28,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":25,\"rightDistance\":5,\"leftDistance\":95}'",
        "{\"frontDistance\":20,\"rightDistance\":5,\"leftDistance\":95}'",
        "{\"frontDistance\":16,\"rightDistance\":5,\"leftDistance\":95}'",
        "{\"frontDistance\":10,\"rightDistance\":5,\"leftDistance\":95}'",
        "{\"frontDistance\":8,\"rightDistance\":5,\"leftDistance\":95}'",
        "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":95}'",
        "{\"frontDistance\":10,\"rightDistance\":5,\"leftDistance\":85}'",
        "{\"frontDistance\":20,\"rightDistance\":5,\"leftDistance\":75}'",
        "{\"frontDistance\":25,\"rightDistance\":5,\"leftDistance\":85}'",
        "{\"frontDistance\":35,\"rightDistance\":5,\"leftDistance\":90}'",
        "{\"frontDistance\":45,\"rightDistance\":5,\"leftDistance\":105}'",
        "{\"frontDistance\":65,\"rightDistance\":5,\"leftDistance\":105}'",
        "{\"frontDistance\":80,\"rightDistance\":5,\"leftDistance\":105}'",
        "{\"frontDistance\":95,\"rightDistance\":5,\"leftDistance\":1005}'",
        "{\"frontDistance\":85,\"rightDistance\":5,\"leftDistance\":1005}'",
        "{\"frontDistance\":75,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":60,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":65,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":55,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":45,\"rightDistance\":25,\"leftDistance\":25}'",
        "{\"frontDistance\":25,\"rightDistance\":25,\"leftDistance\":25}'",
        "{\"frontDistance\":35,\"rightDistance\":45,\"leftDistance\":35}'",
        "{\"frontDistance\":35,\"rightDistance\":65,\"leftDistance\":35}'",
        "{\"frontDistance\":5,\"rightDistance\":35,\"leftDistance\":5}'",
        "{\"frontDistance\":35,\"rightDistance\":35,\"leftDistance\":5}'",
        "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":35}'",
        "{\"frontDistance\":35,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":5,\"rightDistance\":35,\"leftDistance\":5}'",
        "{\"frontDistance\":35,\"rightDistance\":35,\"leftDistance\":5}'",
        "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":35}'",
        "{\"frontDistance\":7,\"rightDistance\":7,\"leftDistance\":28}'",
        "{\"frontDistance\":9,\"rightDistance\":9,\"leftDistance\":20}'",
        "{\"frontDistance\":12,\"rightDistance\":12,\"leftDistance\":25}'",
        "{\"frontDistance\":25,\"rightDistance\":10,\"leftDistance\":30}'",
        "{\"frontDistance\":29,\"rightDistance\":8,\"leftDistance\":33}'",
        "{\"frontDistance\":32,\"rightDistance\":5,\"leftDistance\":35}'",
        "{\"frontDistance\":35,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":35}'",
        "{\"frontDistance\":65,\"rightDistance\":5,\"leftDistance\":35}'",
        "{\"frontDistance\":35,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":35}'",
        "{\"frontDistance\":35,\"rightDistance\":5,\"leftDistance\":65}'",
        "{\"frontDistance\":5,\"rightDistance\":65,\"leftDistance\":5}'",
        "{\"frontDistance\":65,\"rightDistance\":35,\"leftDistance\":5}'",
        "{\"frontDistance\":35,\"rightDistance\":35,\"leftDistance\":65}'",
        "{\"frontDistance\":35,\"rightDistance\":35,\"leftDistance\":65}'",
        "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":95,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":65,\"rightDistance\":35,\"leftDistance\":35}'",
        "{\"frontDistance\":35,\"rightDistance\":35,\"leftDistance\":35}'",
        "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":65,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":35,\"rightDistance\":35,\"leftDistance\":35}'",
        "{\"frontDistance\":35,\"rightDistance\":35,\"leftDistance\":35}'",
        "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":65,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":35,\"rightDistance\":35,\"leftDistance\":35}'",
        "{\"frontDistance\":35,\"rightDistance\":35,\"leftDistance\":35}'",
        "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":35}'",
        "{\"frontDistance\":35,\"rightDistance\":65,\"leftDistance\":5}'",
        "{\"frontDistance\":65,\"rightDistance\":35,\"leftDistance\":5}'",
        "{\"frontDistance\":35,\"rightDistance\":5,\"leftDistance\":5}'",
        "{\"frontDistance\":5,\"rightDistance\":35,\"leftDistance\":5}'",
        "{\"frontDistance\":35,\"rightDistance\":65,\"leftDistance\":5}'",
        "{\"frontDistance\":5,\"rightDistance\":35,\"leftDistance\":5}'",
        "{\"frontDistance\":35,\"rightDistance\":35,\"leftDistance\":5}'",
        # "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":35}'",########
        # "{\"frontDistance\":35,\"rightDistance\":5,\"leftDistance\":35}'",
        # "{\"frontDistance\":5,\"rightDistance\":35,\"leftDistance\":5}'",
        # "{\"frontDistance\":35,\"rightDistance\":35,\"leftDistance\":5}'",
        # "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":35}'",
        # "{\"frontDistance\":65,\"rightDistance\":5,\"leftDistance\":35}'",
        # "{\"frontDistance\":35,\"rightDistance\":35,\"leftDistance\":65}'",
        # "{\"frontDistance\":35,\"rightDistance\":35,\"leftDistance\":35}'",
        # "{\"frontDistance\":5,\"rightDistance\":5,\"leftDistance\":35}'",
        # "{\"frontDistance\":1005,\"rightDistance\":5,\"leftDistance\":95}'",
        # "{\"frontDistance\":105,\"rightDistance\":5,\"leftDistance\":5}'",
    ]
    readJson(read_serial[0])
    maze[pos.x][pos.y].makeNode()

    for i in read_serial:
        readJson(i)
        print(m.toString())
        if (ignoreMetrics() is True):
            print('ignore')
            continue
        move()
        createJson()
        print('#####################')
        f = open('output.txt', 'w', encoding=('utf-8'))
        for j in maze:
            print(j)
            f.write(str(j))
            f.write('\n\n')
        f.close()





############################################################################
m = Metrics()
pos = Possition()
h, l = 10, 5
maze = [[[] for x in range(h)] for y in range(l)]
for y in range(l):
    for x in range(h):
        maze[y][x] = Node()
main()
