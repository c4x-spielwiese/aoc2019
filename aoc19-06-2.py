import string, sys, math

class Orbit:
    def __init__(self, input):
        self.orbit = {}
        for line in input.split("\n"):
            (objA, objB) = line.split(")")
            if objA not in self.orbit:
                self.orbit[objA] = Obj(objA)
            if objB not in self.orbit:
                self.orbit[objB] = Obj(objB)            
            self.orbit[objA].linkChild(self.orbit[objB])
    
    def calcChecksum(self):
        direct = 0
        indirect = 0
        for obj in self.orbit:
            (v1, v2) = self.orbit[obj].countChildren()
            direct += v1
            indirect += v2
        return direct + indirect

    def calcTransfer(self, s, e):
        startObj = self.orbit[s].father
        steps = 0
        while True:
            stepsToChild = startObj.findChild(e)
            if stepsToChild > -1:
                steps += stepsToChild
                return steps
            elif startObj.father is not None:
                steps += 1
                startObj = startObj.father
            else:
                return -1

class Obj:
    def __init__(self, name):
        self.childs = {}
        self.father = None
        self.name = name        

    def linkChild(self, obj):
        if obj.name not in self.childs:
            self.childs[obj.name] = obj
        obj.father = self
    
    def countChildren(self):
        directs = 0
        indirects = 0
        for c in self.childs:
            (v1, v2) = self.childs[c].countChildren()
            directs += v1
            indirects += v2
        return (len(self.childs) + directs, indirects)

    def findChild(self, name, d=0):  
        if name in self.childs:
            return d                
        for x in self.childs:
            r = self.childs[x].findChild(name, d + 1)
            if r > -1:
                return r
        return -1

if len(sys.argv) > 1 and sys.argv[1] == "test":
    print("test mode:")
    tests = [ """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""]
    i = 0
    while i < len(tests):
        o = Orbit(tests[i])
        print(o.calcChecksum())
        print(o.calcTransfer("YOU", "SAN"))
        i += 1

if len(sys.argv) == 1:
    with open(__file__.replace('.py', '.input.txt'), 'r') as f:
        lines = f.read()
        o = Orbit(lines)
        print(o.calcTransfer("YOU", "SAN"))