import string, sys, math

class Orbit:
    def __init__(self, input):
        self.orbit = {}

        for line in input.split("\n"):
            print("read -%s-" % line)
            (objA, objB) = line.split(")")
            if objA not in self.orbit:
                print("init", objA)
                self.orbit[objA] = Obj(objA)

            if objB not in self.orbit:
                print("init", objB)
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


class Obj:
    def __init__(self, name):
        self.childs = {}
        self.name = name

    def linkChild(self, obj):
        if obj.name not in self.childs:
            print("link %s -> %s" % (self.name, obj.name))
            self.childs[obj.name] = obj
    
    def countChildren(self):
        directs = 0
        indirects = 0
        for c in self.childs:
            (v1, v2) = self.childs[c].countChildren()
            directs += v1
            indirects += v2
        return (len(self.childs) + directs, indirects)


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
K)L"""]
    i = 0
    while i < len(tests):
        o = Orbit(tests[i])
        print(o.calcChecksum())
        i += 1

if len(sys.argv) == 1:
    with open(__file__.replace('.py', '.input.txt'), 'r') as f:
        lines = f.read()
        o = Orbit(lines)
        print(o.calcChecksum())