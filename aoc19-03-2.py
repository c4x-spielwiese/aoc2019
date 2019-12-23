import string, sys, math

def getStart(m):
    #return math.floor(len(m) / 2), math.floor(len(m) / 2)
    return 7000, 2000 # y, x --> optimized for puzzle input to fit in 32bit memory :| TODO: need better solution ;) 

def initField(width, height):
    m = []
    for y in range(0, height):
        m.append([])
        for x in range(0, width):
            m[y].append(0)
    return m

def countSteps(m, line, key):
    y, x = getStart(m)
    results = []
    steps = 0
    for i in range(0, len(line)):
        cmd = line[i][0:1]
        num = int(line[i][1:])
        for j in range (0, num):
            if m[y][x] == key:                 
                return steps
            if cmd == 'R':
                x += 1
            elif cmd == 'L':
                x -= 1
            elif cmd == 'U':
                y += 1
            elif cmd == 'D':
                y -= 1          
            steps += 1  
        # dont forget the last point
        if m[y][x] == key: 
            return steps
    return results

def findLowestSteps(m, line, line2, key):
    y, x = getStart(m)
    results = []
    steps = 0
    for i in range(0, len(line)):
        cmd = line[i][0:1]
        num = int(line[i][1:])
        for j in range (0, num):
            if m[y][x] == key:                 
                print("-found %i at y=%i x=%i after s=%i" % (key, y, x, steps))
                m[y][x] = 9
                results.append(steps + countSteps(m, line2, 9))
                m[y][x] = key
            if cmd == 'R':
                x += 1
            elif cmd == 'L':
                x -= 1
            elif cmd == 'U':
                y += 1
            elif cmd == 'D':
                y -= 1          
            steps += 1  
        # dont forget the last point
        if m[y][x] == key: 
            print("--found %i at y=%i x=%i s=%i" % (key, y, x, steps))
            m[y][x] = 9
            results.append(steps + countSteps(m, line2, 9))
            m[y][x] = key
        print("after %s steps=%i" % (line[i], steps))
    return results

def addLine(m, line, key):
    y, x = getStart(m)
    try:
        for i in range(0, len(line)):
            cmd = line[i][0:1]
            num = int(line[i][1:])
            for j in range (0, num):
                m[y][x] = m[y][x] + key # just add the new key on top
                if cmd == 'R':
                    x += 1
                elif cmd == 'L':
                    x -= 1
                elif cmd == 'U':
                    y += 1
                elif cmd == 'D':
                    y -= 1
            # dont forget the last point            
            m[y][x] = m[y][x] + key # just add the new key on top
    except IndexError:
        sys.stderr.write("Index out of range at i=%s %s - y=%i / x=%i -- j=%i end=%i left=%i\n" % (i, cmd, y, x, j, num, num - j))
        sys.exit(-1)
        pass
    return m

def printField(m):
    print('########################################')
    for y in range(0, len(m)):
        for x in range(0, len(m[0])):        
            if m[y][x] == 10:
                sys.stdout.write('.')
            elif m[y][x] > 0:
                sys.stdout.write(str(m[y][x]))
            else:
                sys.stdout.write(' ')
        sys.stdout.write('\n')
    print('########################################')

def manDist(p1X, p1Y, p2X, p2Y):
    return abs(p1X - p2X) + abs(p1Y - p2Y) 

def findIntersect(m):     
    sY, sX = getStart(m)
    minD = len(m) + len(m)
    for y in range(0, len(m)):
        for x in range(0, len(m)):
            if m[y][x] == 5:
                d = manDist(x, y, sX, sY)
                print("found x at %i|%i with d=%i" %(y, x, d))
                if minD > d: 
                    minD = d
    return minD


def calcDist(line1, line2, size):
    m = initField(size, size)    
    sY, sX = getStart(m)

    line1 = line1.split(",")
    line2 = line2.split(",")
    print(line1)
    print(line2)

    

    addLine(m, line1, 2)
    addLine(m, line2, 3)
    m[sY][sX] = 1 # ignore the starting point
    #printField(m)
    m2 = m.copy()

    res = findLowestSteps(m, line1, line2, 5)
    res.sort()

    print(res)

    return res[0]
    #return min(sum1, sum2)

if len(sys.argv) > 1 and sys.argv[1] == "test":
    print("test mode:")
    tests = [                
                "R8,U5,L5,D3", "U7,R6,D4,L4", 20, 6,
                "R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 500, 610
            ]
    i = 0
    while i < len(tests):
        res = calcDist(tests[i], tests[i+1], tests[i+2])
        print("test %i %i => %s" % (i, res, "OK" if res == tests[i+3] else "ERR!"))        
        i += 4

else:
    with open(__file__.replace('.py', '.input.txt'), 'r') as f:
        line1 = f.readline().strip()
        line2 = f.readline().strip()
        print(calcDist(line1, line2, 15000))